import streamlit as st
from langchain_community.llms.fake import FakeListLLM
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
class ChatLLM:
    def __init__(self):
        self._initialize_llm()
        self.prompt_template = PromptTemplate(
            input_variables=["history", "input"],
            template="""
            You are a helpful and friendly chatbot.

            Current conversation:
            {history}
            Human: {input}
            AI:"""
        )

    def _initialize_llm(self):
        """Initializes a persistent FakeListLLM instance in Streamlit session state."""
        if "llm" not in st.session_state:
            print("Creating new LLM instance")
            responses = [
                "Hello there!", 
                "I am a friendly chatbot designed to help you.",
                "How can I assist you today?", 
                "My name is Gemini. What's your name?",
                "That's a lovely name!",
                "I don't have feelings, but I appreciate you asking!",
                "Goodbye! It was nice chatting with you."
            ]
            st.session_state.llm = FakeListLLM(responses=responses)
        self.llm = st.session_state.llm

    def generate_response(self, user_input, chat_history):
        """
        Generates a response from the LLM based on user input and chat history.
        """
        memory = ConversationBufferMemory(memory_key="history")
        for message in chat_history:
            if message['role'] == 'user':
                memory.chat_memory.add_user_message(message['content'])
            elif message['role'] == 'assistant':
                memory.chat_memory.add_ai_message(message['content'])

        conversation = ConversationChain(
            prompt=self.prompt_template,
            llm=self.llm,
            verbose=True,
            memory=memory
        )
        response = conversation.predict(input=user_input)
        return response