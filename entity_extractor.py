from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationEntityMemory
from pprint import pprint


class EntityExtractor:
    def __init__(self, messages) -> None:
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        memory = ConversationEntityMemory(llm=llm)

        for message in messages:
            msg = "%s at %s posted: %s" % (
                message["user"], message["timestamp"], message["message"])
            print(msg)
            memory.save_context({"input": msg}, {"ouput": ""})

        print(memory.load_memory_variables(
            {"input": 'What is the project called?'}))
        print(memory.load_memory_variables(
            {"input": 'What is Akshay Working on?'}))

        print('-----')
        pprint(memory.entity_store.store)
