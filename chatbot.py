from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import os
from datetime import datetime, timedelta
import pickle

def create_chatbot():
    chatbot = ChatBot('ManjaroAssistan')
    trainer = ChatterBotCorpusTrainer(chatbot)

    # You can train the chatbot with additional data if needed
    # trainer.train("chatterbot.corpus.english")

    return chatbot

def read_api_key():
    api_key_file = os.path.join(os.path.dirname(__file__), 'apikey.txt')
    with open(api_key_file, 'r') as f:
        return f.read().strip()

def create_chat_prompt(user_input):
    return f"You:{user_input}\nManjaroAssistan:"

def save_chat_history(chat_history):
    with open('chat_history.pkl', 'wb') as f:
        pickle.dump(chat_history, f)

def load_chat_history():
    if os.path.exists('chat_history.pkl'):
        with open('chat_history.pkl', 'rb') as f:
            return pickle.load(f)
    return []

def print_chat_history(chat_history):
    print("Chat History:")
    for idx, (name, _) in enumerate(chat_history):
        print(f"{idx + 1}: {name}")
    print()

def delete_chat_history(chat_history, idx):
    if 0 <= idx < len(chat_history):
        _, chat_data = chat_history.pop(idx)
        print(f"Chat '{_}' deleted.")
        save_chat_history(chat_history)

def chat_menu(chatbot):
    chat_history = load_chat_history()

    while True:
        print("""
  __  __            _                  _          _    _             
 |  \/  |__ _ _ _  (_)__ _ _ _ ___    /_\   _____(_)__| |_ __ _ _ _  
 | |\/| / _` | ' \ | / _` | '_/ _ \  / _ \ (_-<_-< (_-<  _/ _` | ' \ 
 |_|  |_\__,_|_||_|/ \__,_|_| \___/ /_/ \_\/__/__/_/__/\__\__,_|_||_|
                 |__/                                                

 +-+-+-+-+-+-+-+ +-+-+ +-+-+-+-+-+-+-+-+-+-+
 |p|o|w|e|r|e|d| |b|y| |c|h|a|t|t|e|r|b|o|t|
 +-+-+-+-+-+-+-+ +-+-+ +-+-+-+-+-+-+-+-+-+-+

""")
        print("1. New Chat")
        print("2. Chat History")
        print("3. Exit")

        if chat_history is None:
            chat_history = []

        while True:
            choice = input("Select an option (1/2/3): ")
            if int(choice) in {1, 2, 3}:
                break
            else:
                print("Sorry wrong input please type:\n[1] for a new chat, [2] for chat history, or [3] to exit.")

        if choice == "1":
            chat_name = input("Enter a name for your new chat: ")
            chat_history.append((chat_name, []))
            chat_history[-1][1].append((choice, []))
            save_chat_history(chat_history)

            while True:
                user_input = input("You: ")
                if user_input == "goodbye":
                    print("ManjaroAssistan: goodbye.")
                    break

                prompt = create_chat_prompt(user_input)
                bot_response = chatbot.get_response(user_input)
                print(f"ManjaroAssistan: {bot_response}")
                chat_history[-1][1].append((user_input, str(bot_response)))

        elif choice == "2":
            print_chat_history(chat_history)
            chat_idx = input("Enter the index of the chat you want to continue|read|delete (0 to go back): ")

            if int(chat_idx) == 0:
                continue

            while True:
                try:
                    chat_idx = int(chat_idx) - 1
                    chat_name, chat_data = chat_history[chat_idx]
                    print(f"\nChat '{chat_name}' (Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
                    for user_msg, bot_msg in chat_data:
                        print(f"You: {user_msg}\nManjaroAssistan: {bot_msg}")

                    chat_options = input("Options: (C)ontinue, (D)elete, (0)Back: ")

                    if chat_options.upper() == "C":
                        continue

                    elif chat_options.upper() == "D":
                        delete_chat_history(chat_history, chat_idx)

                except (ValueError, IndexError):
                    print("Invalid input. Please enter a valid input.")

        elif choice == "3":
            print("Exiting Manjaro Assistans. Goodbye")

if __name__ == "__main__":
    api_key = read_api_key()
    chatbot = create_chatbot()
    chat_menu(chatbot)
