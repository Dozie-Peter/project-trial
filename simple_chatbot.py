import nltk
import sqlite3
import hashlib
import email
from nltk.chat.util import Chat, reflections

conn = sqlite3.connect('Database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT
    )
''')
conn.commit()


# Define patterns and responses for the chatbot
pairs = [
    (r'hi|hello|hey', ['Hi there!', 'Hello!', 'Hey!']),
    (r'how are you', ['I am fine, thank you!', 'I\'m doing well, thanks. How about you?']),
    (r'what is your name', ['I am a chatbot.', 'You can call me a chatbot.']),
    (r'quit', ['Bye! Take care.', 'Goodbye.']),
]

# Combine NLTK chat pairs with responses from the database
cursor.execute("SELECT user_input, bot_response FROM chat_pairs")
rows = cursor.fetchall()
for row in rows:
    user_input = row[0]
    bot_response = [row[1]]
    pairs.append((user_input, bot_response))
 
# Create a chatbot
chatbot = Chat(pairs, reflections)
 
# Function to handle user input and get bot response
def get_bot_response(user_input):
    response = chatbot.respond(user_input)
    if not response:
        response = "I'm sorry, I don't understand."
    return response
 
# Function to register a new user
def register_user(username, password, email):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, hashed_password, email))
    conn.commit()

# Function to authenticate a user
def authenticate_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
    return cursor.fetchone() is not None
 
# Function to prompt the user for login
def login_prompt():
    while True:
        print("Bot: Do you have an account or are you a new user?")
        print("1. I have an account")
        print("2. I am a new user")
        print("3. Exit")
        choice = input("Enter your choice (1, 2 or 3): ")
 
        if choice == '1':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
 
            if authenticate_user(username, password):
                print("Bot: Login successful.")
                return username
            else:
                print("Bot: Invalid username or password. Please try again.")
 
        elif choice == '2':
            username = input("Enter a new username: ")
            password = input("Enter a password: ")
            email = input("Enter a email: ")
 
            # Check if the username already exists
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            if cursor.fetchone() is not None:
                print("Bot: Username already exists. Please choose another one.")
            else:
                register_user(username, password, email)
                print("Bot: Registration successful. You can now log in.")
                return username
        elif choice == '3':
            print("Bot: Goodbye!")
            break
            exit()
 
        else:
            print("Bot: Invalid choice. Please enter 1, 2 or 3.")
 
# Main loop for interacting with the user
def main():
    print("Bot: Welcome! Please log in or register.")
    logged_in_user = login_prompt()
 
    while True:
        user_input = input(f"{logged_in_user}: ")
 
        if user_input.lower() in ['bye', 'exit', 'quit']:
            print("Bot: Goodbye!")
            break
 
        bot_response = get_bot_response(user_input)
        print("Bot:", bot_response)
 
# Run the main loop
main()
 
# Close the database connection
conn.close()