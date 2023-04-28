from conversation_chain import ConversationChain


class Chats:
  def __init__(self):
    self.topics_chains = {}

  def post_message(self, topic, message):
    # if topic not in self.topics_chains:
    #   print("creating topic " + topic)
    #   chain = ConversationChain(topic).llm_chain
    #   self.topics_chains[topic] = chain

    # chain = self.topics_chains[topic]
    # return chain.run(message)

    chain = ConversationChain(topic).llm_chain
    return chain.run(message)
