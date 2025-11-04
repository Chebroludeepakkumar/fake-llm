import streamlit as st
from backend.database import ChatDatabase  # assuming you renamed your DB functions into a class

class SidebarManager:
    def __init__(self):
        self.db = ChatDatabase()

    def show(self):
        """Displays the sidebar with chat history and a new chat button."""
        with st.sidebar:
            st.title("Chat History")

            if st.button("➕ New Chat"):
                st.session_state.conversation_id = None
                st.session_state.messages = []
                st.rerun()

            st.write("---")

            conversations = self.db.get_conversations()
            total = len(conversations)

            for index, conv in enumerate(conversations):
                conv_id = conv[0]
                conv_date = conv[1]

                col1, col2 = st.columns([0.8, 0.2])

                with col1:
                    if st.button(f"Chat {total - index} on {conv_date}", key=f"conv_{conv_id}", use_container_width=True):
                        st.session_state.conversation_id = conv_id
                        st.rerun()

                with col2:
                    if st.button("🗑️", key=f"delete_{conv_id}"):
                        self.db.delete_conversation(conv_id)
                        if st.session_state.get("conversation_id") == conv_id:
                            st.session_state.conversation_id = None
                            st.session_state.messages = []
                        st.rerun()