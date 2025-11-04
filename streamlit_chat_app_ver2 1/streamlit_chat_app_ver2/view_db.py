from backend.database import ChatDatabase

if __name__ == "__main__":
    db = ChatDatabase()
    print(f"Inspecting database: {db.db_name}")
    db.view_table("conversations")
    db.view_table("messages")
