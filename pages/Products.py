import streamlit as st
from utils.database import get_data
import random
import time

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_vertexai import ChatVertexAI
from utils.template import system

gemini = ChatVertexAI(
  model_name="gemini-pro",
  temperature="0.9",
  max_output_tokens="1048",
  streaming=True,
  convert_system_message_to_human=True,
)

# def display_prod(prod_list: list):

#   for prod in prod_list:
#     if prod['description']:
#       st.sidebar.write(prod['title'])

prod_list = get_data()

st.markdown("# SneakAi 🎈")

st.sidebar.markdown("# SneakAi 🎈")

st.markdown('#### Select a product and enter a prompt to create content about the product')

list_option = st.sidebar.selectbox(
  "Product",
  [prod['title'] for prod in prod_list],
  placeholder='Select a product',
)
st.sidebar.write(list_option)

if 'gemini_model' not in st.session_state:
  st.session_state['gemini_model'] = 'gemini-pro'

if 'messages' not in st.session_state:
  st.session_state.messages = []

for message in st.session_state.messages:
  with st.chat_message(message['role']):
    st.markdown(message['content'])


if prompt := st.chat_input("Enter a prompt..."):
  
  for prod in prod_list:
      if prod['title'] == list_option:
        content_data = f"""
          'title':{ prod['title']},
          'description': {prod['description']},
          'brand': {prod['brand']},
          'gender': {prod['gender']},
          'age_group': {prod['age_group']},
          'base_price': {prod['base_price']},
          'labels': {prod['labels']}
        """
        break
  if len(st.session_state.messages) <= 1:
    template = f"{prompt}: \n {content_data}"
    st.session_state.messages.append({"role": 'user', 'content': template})
    chat = ChatPromptTemplate.from_messages([("system", system),("human", template)]).format_messages()
    # system_prompt = ChatPromptTemplate.from_template(system)
  else:
    chat = prompt
    st.session_state.messages.append({"role": 'user', 'content': chat})
  
  with st.chat_message('user'):
    st.markdown(prompt)

  with st.chat_message('assistant'):
    response = gemini.invoke(
      chat
    )
    st.session_state.messages.append({'role': "assistant", "content": response.content})
    st.markdown(response.content)



# display_prod(prod_list=prod_list)

# Do something with the items (e.g., display them)
# st.write(items)