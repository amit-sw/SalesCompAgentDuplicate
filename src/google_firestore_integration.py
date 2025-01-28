from google.cloud import firestore

def get_prompts(credentials):
    db = firestore.Client(credentials=credentials)
    collection_ref = db.collection(u'Prompts')
    query = collection_ref.where('user', '==', 'default')
    docs = query.stream()
    
    # Collect document IDs that match the query
    results = [{'id': doc.id, **doc.to_dict()} for doc in docs]
    return results