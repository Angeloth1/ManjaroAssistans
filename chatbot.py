from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import os
from datetime import datetime, timedelta
import pickle

def create_chatbot():
    chatbot = ChatBot('ManjaroAssistan')
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train("chatterbot.corpus.english")

    return chatbot

def create_chat_prompt(user_input):
    return f"You: {user_input}\nManjaroAssistan:"

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
        888                                888                                 d8b          888                      
        888                                888                                 Y8P          888                      
        888                                888                                              888                      
        888      .d88b.   .d8888b  8888b.  888       8888b.  .d8888b  .d8888b  888 .d8888b  888888  8888b.  88888b.  
        888     d88""88b d88P"        "88b 888          "88b 88K      88K      888 88K      888        "88b 888 "88b 
        888     888  888 888      .d888888 888      .d888888 "Y8888b. "Y8888b. 888 "Y8888b. 888    .d888888 888  888 
        888     Y88..88P Y88b.    888  888 888      888  888      X88      X88 888      X88 Y88b.  888  888 888  888 
        88888888 "Y88P"   "Y8888P "Y888888 888      "Y888888  88888P'  88888P' 888  88888P'  "Y888 "Y888888 888  888 
                                                                                                             
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
                save_chat_history(chat_history)

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
                        break

                    elif chat_options.upper() == "D":
                        delete_chat_history(chat_history, chat_idx)
                        break

                except (ValueError, IndexError):
                    print("Invalid input. Please enter a valid input.")

        elif choice == "3":
            print("Exiting Manjaro Assistans. Goodbye")
            break

if __name__ == "__main__": 
    chatbot = create_chatbot()
    chat_menu(chatbot)
