from langchain_google_vertexai import ChatVertexAI
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from utils.template import template
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains  import LLMChain
from langchain_core.messages import SystemMessage
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


@st.cache_resource
def _init_gemini():
  gemini = ChatVertexAI(
    model_name="gemini-pro",
    temperature="0.9",
    max_output_tokens="1048",
    streaming=True,
    convert_system_message_to_human=True,
  )
  return gemini

if 'gemini_model' not in st.session_state:
  st.session_state['gemini_model'] = 'gemini-pro'

msgs = StreamlitChatMessageHistory(key="langchain_messages")

view_message = st.sidebar.expander("View messages in session state")

prompt = ChatPromptTemplate.from_messages([
  SystemMessage(template),
  MessagesPlaceholder(
    variable_name="chat_history"
  ),
  (
    'user', '{prompt}'
  )])

gemini = prompt | _init_gemini()

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, max_output_tokens=1000)

gemini_chain = RunnableWithMessageHistory(
  gemini,
  lambda session_id:  msgs,
  input_messages_key="prompt",
  history_messages_key="chat_history",
  verbose=True,
  output_parser= StrOutputParser(),
)

