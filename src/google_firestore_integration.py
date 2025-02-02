from google.cloud import firestore

def get_prompts(credentials):
    """
    Retrieves default prompts from Google Firestore database.
    
    Args:
        credentials: Google Cloud credentials object for authentication
        
    Returns:
        list: A list of dictionaries containing prompt documents, where each dictionary
             includes the document ID and all fields from the Firestore document.
             Example: [{'id': 'doc1', 'user': 'default', 'prompt_text': '...'}]
    """
    # Initialize a Firestore client with the provided credentials
    db = firestore.Client(credentials=credentials)
    
    # Get a reference to the 'Prompts' collection in Firestore
    collection_ref = db.collection(u'Prompts')
    
    # Create a query to filter documents where 'user' field equals 'default'
    query = collection_ref.where('user', '==', 'default')
    
    # Execute the query and get a stream of matching documents
    docs = query.stream()
    
    # Create a list of dictionaries containing document data
    # For each document:
    # - doc.id gets the document's unique identifier
    # - doc.to_dict() converts the document data to a Python dictionary
    # - **doc.to_dict() unpacks the dictionary to merge with the id
    results = [{'id': doc.id, **doc.to_dict()} for doc in docs]
    
    return results

def get_one_prompt(credentials, user, prompt_name):
    db = firestore.Client(credentials=credentials)
    
    # Get a reference to the 'Prompts' collection in Firestore
    collection_ref = db.collection(u'Prompts')
    
    # Create a query to filter documents where 'user' field equals 'default'
    query = collection_ref.where('prompt_name', '==', prompt_name)
    
    # Execute the query and get a stream of matching documents
    docs = query.stream()
    
    # Create a list of dictionaries containing document data
    # For each document:
    # - doc.id gets the document's unique identifier
    # - doc.to_dict() converts the document data to a Python dictionary
    # - **doc.to_dict() unpacks the dictionary to merge with the id
    results = [{'id': doc.id, **doc.to_dict()} for doc in docs]
    prompt_value = results[0].get("prompt_value")
   
    
    return prompt_value