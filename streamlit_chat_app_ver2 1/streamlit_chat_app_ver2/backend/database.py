import sqlite3
from datetime import datetime

class ChatDatabase:
    def __init__(self, db_name='chat_history.db'):
            self.db_name = db_name
            self._init_db()
        
    def _connect(self):
            return sqlite3.connect(self.db_name)

    def _init_db(self):
        """Initializes the database and creates tables if they don't exist."""
        conn = self._connect()
        cursor = conn.cursor()
        
        # Create conversations table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create messages table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (conversation_id) REFERENCES conversations (id)
        )
        ''')
        
        conn.commit()
        conn.close()

    def create_conversation(self):
        """Creates a new conversation and returns its ID."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO conversations DEFAULT VALUES')
        conversation_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return conversation_id

    def add_message(self,conversation_id, role, content):
        """Adds a message to a specific conversation."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)',
                    (conversation_id, role, content))
        conn.commit()
        conn.close()

    def get_conversations(self):
        """Retrieves all conversations from the database."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('SELECT id, created_at FROM conversations ORDER BY created_at DESC')
        conversations = cursor.fetchall()
        conn.close()
        return conversations

    def get_messages(self,conversation_id):
        """Retrieves all messages for a specific conversation."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('SELECT role, content FROM messages WHERE conversation_id = ? ORDER BY timestamp ASC',
                    (conversation_id,))
        messages = cursor.fetchall()
        conn.close()
        return messages

    def delete_conversation(self,conversation_id):
        """Deletes a conversation and all its messages from the database."""
        conn = self._connect()
        cursor = conn.cursor()
        
        # Delete messages associated with the conversation
        cursor.execute('DELETE FROM messages WHERE conversation_id = ?', (conversation_id,))
        
        # Delete the conversation itself
        cursor.execute('DELETE FROM conversations WHERE id = ?', (conversation_id,))
        
        conn.commit()
        conn.close()
    
    def view_table(self, table_name):
            """Prints the contents of a given table."""
            try:
                conn = self._connect()
                cursor = conn.cursor()

                print(f"\n--- Contents of table: {table_name} ---")

                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = [col[1] for col in cursor.fetchall()]
                print(f"Columns: {columns}")
                print("-" * 40)

                cursor.execute(f"SELECT * FROM {table_name};")
                rows = cursor.fetchall()

                if not rows:
                    print("Table is empty.")
                else:
                    for row in rows:
                        print(row)

            except sqlite3.Error as e:
                print(f"An error occurred: {e}")
            finally:
                if conn:
                    conn.close()

