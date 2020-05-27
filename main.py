from recognize_gesture import start_recognizing
from database.database import set_up_database

if __name__ == "__main__":
    set_up_database()
    print("test utility")
    start_recognizing()
