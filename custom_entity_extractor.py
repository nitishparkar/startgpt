from langchain.llms import OpenAI
from langchain.memory import ConversationEntityMemory
from pprint import pprint


ENTITY_EXTRACTION_TEMPLATE = """You are an AI assistant reading the transcript of a conversation between humans. Extract all of the proper nouns from the last line of conversation. As a guideline, a proper noun is generally capitalized. You should definitely extract all names.

The conversation history is provided just in case of a coreference (e.g. "What do you know about him" where "him" is defined in a previous line) -- ignore items mentioned there that are not in the last line.

Return the output as a single comma-separated list, or NONE if there is nothing of note to return (e.g. the user is just issuing a greeting or having a simple conversation).

Conversation history (for reference only):
{history}
Last line of conversation (for extraction):
{input}

Output:"""


ENTITY_SUMMARIZATION_TEMPLATE = """You are an AI assistant helping a human keep track of facts about relevant people, and tasks. Update the summary of the provided entity in the "Entity" section based on the last line of conversation. If you are writing the summary for the first time, return a single sentence.
The update should only include facts that are relayed in the last line of conversation about the provided entity, and should only contain facts about the provided entity.

If there is no new information about the provided entity or the information is not worth noting (not an important or relevant fact to remember long-term), return the existing summary unchanged.

Full conversation history (for context):
{history}

Entity to summarize:
{entity}

Existing summary of {entity}:
{summary}

Last line of conversation:
{input}
Updated summary:"""


class CustomEntityExtractor:
    def __init__(self, messages) -> None:
        llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0)

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
