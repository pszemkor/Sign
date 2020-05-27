from recognize_gesture import start_recognizing
from database import set_up_database

if __name__ == "__main__":
    set_up_database()
    start_recognizing()
