import streamlit as st
from backend.database import ChatDatabase
from backend.llm import ChatLLM
from frontend.sidebar import SidebarManager

class ChatApp:
    def __init__(self):
        self.db = ChatDatabase()
        self.llm = ChatLLM()
        self.sidebar = SidebarManager()
        self._initialize_session_state()

    def _initialize_session_state(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "conversation_id" not in st.session_state:
            st.session_state.conversation_id = None
        if "conversation_loaded" not in st.session_state:
            st.session_state.conversation_loaded = None

    def load_conversation(self):
        """Loads messages from the selected conversation."""
        if st.session_state.conversation_loaded != st.session_state.conversation_id:
            if st.session_state.conversation_id:
                st.session_state.messages = []
                db_messages = self.db.get_messages(st.session_state.conversation_id)
                for role, content in db_messages:
                    st.session_state.messages.append({"role": role, "content": content})
            else:
                st.session_state.messages = []
            st.session_state.conversation_loaded = st.session_state.conversation_id

    def display_messages(self):
        """Displays chat messages from history."""
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def handle_user_input(self):
        """Handles user input and generates bot response."""
        if prompt := st.chat_input("What is up?"):
            with st.chat_message("user"):
                st.markdown(prompt)

            is_new_chat = st.session_state.conversation_id is None

            if is_new_chat:
                st.session_state.conversation_id = self.db.create_conversation()
                st.session_state.conversation_loaded = st.session_state.conversation_id

            st.session_state.messages.append({"role": "user", "content": prompt})
            self.db.add_message(st.session_state.conversation_id, "user", prompt)

            with st.spinner("Thinking..."):
                response = self.llm.generate_response(prompt, st.session_state.messages)

                with st.chat_message("assistant"):
                    st.markdown(response)

                st.session_state.messages.append({"role": "assistant", "content": response})
                self.db.add_message(st.session_state.conversation_id, "assistant", response)

            if is_new_chat:
                st.rerun()

    def run(self):
        st.title("Streamlit Chat App with Memory")
        self.sidebar.show()
        self.load_conversation()
        self.display_messages()
        self.handle_user_input()

# Run the app
if __name__ == "__main__":
    app = ChatApp()
    app.run()
