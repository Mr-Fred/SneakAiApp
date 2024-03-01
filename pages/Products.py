import streamlit as st
from utils.mongodb import get_data
from utils.template import template
from utils.llmchain import gemini_chain, msgs

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
add_prod_data_to_prompt = st.sidebar.checkbox(
  list_option,
  help='Check the box, to incluse the product data in prompt',
  key='add_prod_data_to_prompt',
)

if 'gemini_model' not in st.session_state:
  st.session_state['gemini_model'] = 'gemini-pro'

# if len(msgs.messages) == 0:
#   msgs.add_ai_message("Hi, how can i help you today?")
for message in msgs.messages:
  with st.chat_message(message.type):
    st.write(message.content)

if prompt := st.chat_input("Enter a prompt..."):
  
  for prod in prod_list:
      if prod['title'] == list_option and add_prod_data_to_prompt:
        content_data = f"""          
          'title': {prod['title']},
          'description': {prod['description']},
          'brand': {prod['brand']},
          'gender': {prod['gender']},
          'age_group': {prod['age_group']},
          'base_price': {prod['base_price']},
          'labels': {prod['labels']}
      """
        break
  if add_prod_data_to_prompt:
    user_input = f"{prompt} \n {content_data}"
    # st.session_state.langchain_messages.append({"role": 'user', 'content': user_input})
    with st.chat_message('user'):
      st.markdown(user_input)
    config = {"configurable": {'session_id': "any"}}

    with st.chat_message('assistant'):
      response = gemini_chain.invoke(
        {'prompt': user_input},
        config=config
      )
      # st.session_state.messages.append({'role': "assistant", "content": response.content})
      st.markdown(response.content)
  else:
    # st.session_state.langchain_messages.append({"role": 'user', 'content': prompt})
    with st.chat_message('user'):
      st.markdown(prompt)
    config = {"configurable": {'session_id': "any"}}
    with st.chat_message('assistant'):
      response = gemini_chain.invoke(
        {'prompt': prompt},
        config=config
      )
      # st.session_state.messages.append({'role': "assistant", "content": response.content})
      st.markdown(response.content)

# display_prod(prod_list=prod_list)

# Do something with the items (e.g., display them)
# st.write(items)