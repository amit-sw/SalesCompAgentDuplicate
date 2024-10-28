import os
import PyPDF2
import hashlib
import numpy as np

import streamlit as st
from streamlit.logger import get_logger

from pinecone import Pinecone
from openai import OpenAI

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader

from pathlib import Path

# Add parent directory to system path for importing utils
import sys
sys.path.append("..")
from src.utils import show_navigation
show_navigation()

# Initialize logger
LOGGER = get_logger(__name__)

# Get API keys and configuration from Streamlit secrets
PINECONE_API_KEY=st.secrets['PINECONE_API_KEY']
PINECONE_API_ENV=st.secrets['PINECONE_API_ENV']
PINECONE_INDEX_NAME=st.secrets['PINECONE_INDEX_NAME']

# Initialize OpenAI client
client=OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

# Convert PDF file to text string
def pdf_to_text(uploaded_file):
    pdfReader = PyPDF2.PdfReader(uploaded_file)
    count = len(pdfReader.pages)
    text=""
    for i in range(count):
        page = pdfReader.pages[i]
        text=text+page.extract_text()
    return text

# Convert Markdown file to text string
def md_to_text(uploaded_file):
    # Read markdown file content directly as text
    return uploaded_file.getvalue().decode('utf-8')

# Create embeddings for text and store in Pinecone
def embed(text,filename):
    pc = Pinecone(api_key=st.secrets['PINECONE_API_KEY'])
    index = pc.Index(PINECONE_INDEX_NAME)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000,chunk_overlap  = 200,length_function = len,is_separator_regex = False)
    docs=text_splitter.create_documents([text])
    
    # Process each chunk
    for idx,d in enumerate(docs):
        # Create unique hash for the chunk
        hash=hashlib.md5(d.page_content.encode('utf-8')).hexdigest()
        # Generate embedding using OpenAI
        embedding=client.embeddings.create(model="text-embedding-ada-002", input=d.page_content).data[0].embedding
        # Create metadata for the chunk
        metadata={"hash":hash,"text":d.page_content,"index":idx,"model":"text-embedding-ada-003","docname":filename}
        # Store in Pinecone
        index.upsert([(hash,embedding,metadata)])
    return


# Direct Text Input section    
st.markdown("# Upload text directly")
uploaded_text = st.text_area("Enter Text","")
if st.button('Process and Upload Text'):
    embedding = embed(uploaded_text,"Anonymous")
#
# Accept a PDF or Markdown file using Streamlit and add to Pinecone

# File upload section for PDF and Markdown file
st.markdown("# Upload file: PDF or Markdown")
uploaded_file = st.file_uploader("Upload file", type=["pdf", "md"])
if uploaded_file is not None:
    if st.button('Process and Upload File'):
        # Determine file type and process accordingly
        file_extension = Path(uploaded_file.name).suffix.lower()
        if file_extension == '.pdf':
            file_text = pdf_to_text(uploaded_file)
        else:  # .md file
            file_text = md_to_text(uploaded_file)
        embedding = embed(file_text, uploaded_file.name)


#
#st.markdown("# Upload file: PDF")
#uploaded_file=st.file_uploader("Upload PDF file",type="pdf")
#if uploaded_file is not None:
#    if st.button('Process and Upload File'):
#        pdf_text = pdf_to_text(uploaded_file)
#        embedding = embed(pdf_text,uploaded_file.name)
        