import streamlit as st
from pymongo import MongoClient
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

def get_data() -> list:

  conn = st.connection('mongodb', type=MongoDBConnection)

  # Get the collection object
  db = conn._instance.get_database('snkrApp_db')
  collection = db.get_collection('sneakers')

  # Find and return items
  items = collection.find(limit=5)
  items = list(items)
  return items
