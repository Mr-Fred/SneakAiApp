from langchain_google_vertexai import ChatVertexAI
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from utils.template import system, human
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.agents import AgentExecutor, create_json_chat_agent
from langchain_community.tools import DuckDuckGoSearchRun


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
memory = ConversationBufferMemory(chat_memory=msgs,memory_key="chat_history",
                                  return_messages=True, output_key='output', max_output_tokens=1000)

# view_message = st.sidebar.expander("View messages in session state")

prompt = ChatPromptTemplate.from_messages([
  SystemMessage(system),
  MessagesPlaceholder(
    variable_name="chat_history", optional=True
  ),
  (
    'human', human
  ),
  MessagesPlaceholder("agent_scratchpad"),])

tools = [DuckDuckGoSearchRun(name="search engine")]

gemini_agent = create_json_chat_agent(llm=_init_gemini(), prompt=prompt, tools=tools)

gemini_executor = AgentExecutor.from_agent_and_tools(
  agent=gemini_agent,
  tools=tools,
  memory=memory,
  return_intermediate_steps=True,
  handle_parsing_errors=True,
)

