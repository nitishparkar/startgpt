from pprint import pprint
import asyncio
from flask import Flask, request
from langchain.memory.motorhead_memory import MotorheadMemory
from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI


class ConversationChain:
  def __init__(self, topic):
    memory = MotorheadMemory(
        session_id=topic, url="http://localhost:8080", memory_key="chat_history", timeout=10)

    print('Initializing memory')
    asyncio.run(memory.init())  # loads previous state from Motörhead
    print('Done initializing memory')
    pprint(vars(memory))

    template = """You are a chatbot having a conversation with a human. Answer the question based on the context below. If the question cannot be answered using the information provided answer with "I don't know"
    """

    if memory.context is not None:
      template += f"""{memory.context}
      """

    template += """{chat_history}
    Human: {human_input}
    AI:"""

    prompt = PromptTemplate(
        input_variables=["chat_history", "human_input"], template=template)
    llm_chain = LLMChain(llm=ChatOpenAI(model_name="gpt-3.5-turbo"),
                         prompt=prompt, verbose=True, memory=memory)
    self.llm_chain = llm_chain

  def llm_chain(self):
    return self.llm_chain
