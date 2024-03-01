import streamlit as st
from pymongo import MongoClient, errors, ASCENDING
from streamlit.connections import BaseConnection

class MongoDBConnection(BaseConnection[MongoClient]):
  
  def __init__(self, connection_name: str) -> None:
    super().__init__(connection_name)
    self._connect()
  
  def _connect(self, kwargs=[None]):

    if 'uri' in kwargs:
      return MongoClient(kwargs['uri'])
    else:
      print('Connecting...')
      client = MongoClient(st.secrets.mongo.uri)
      print('connected')
      return client
    
  def cursor(self) -> BaseConnection:
    return self._instance.cursor()


conn = st.connection('mongodb', type=MongoDBConnection)

@st.cache_data
def get_data() -> list:
  # Get the collection object
  db = conn._instance.get_database('snkrApp_db')
  collection = db.get_collection('sneakers')

  # Create the index only once for efficiency
  if not collection.index_information().get('title_brand_gender_index'):
    try:
      collection.create_index([('title', ASCENDING), ('brand', ASCENDING), ('gender', ASCENDING)])
      print("Index created successfully!")
    except errors.OperationFailure as e:
      print(f"Index creation failed: {e}")

  # Find and return items
  items = collection.find({'description': {'$ne': None}})
  items = list(items)
  return items


