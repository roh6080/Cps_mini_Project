import os
from datetime import datetime
from cryptography.fernet import Fernet

# --- Password Setup ---
PASSWORD = "147852369"  # Replace with your desired password
key = Fernet.generate_key()  # Generates encryption key (use same key to encrypt/decrypt)
cipher_suite = Fernet(key)

# --- Function to Verify Password ---
def verify_password():
    attempts = 3
    while attempts > 0:
        user_password = input("Enter your password: ")
        if user_password == PASSWORD:
            print("Access granted!")
            return True
        else:
            attempts -= 1
            print(f"Incorrect password. {attempts} attempts remaining.")
    print("Access denied. Exiting program.")
    return False

# --- Function to Save Entry ---
def save_entry():
    # Get today's date
    today = datetime.now().strftime("%Y-%m-%d")
    file_name = f"{today}.txt"
    
    # Get user input
    print("\nWrite your diary entry below (type 'DONE' to save):")
    lines = []
    while True:
        line = input()
        if line.upper() == "DONE":
            break
        lines.append(line)
    entry = "\n".join(lines)
    
    # Encrypt the entry
    encrypted_entry = cipher_suite.encrypt(entry.encode())
    
    # Save to file
    with open(file_name, "wb") as file:
        file.write(encrypted_entry)
    print(f"Your entry has been saved as {file_name}.")

# --- Function to Read Entry ---
def read_entry():
    today = datetime.now().strftime("%Y-%m-%d")
    file_name = f"{today}.txt"
    
    if not os.path.exists(file_name):
        print(f"No entry found for today ({today}).")
        return
    
    # Read and decrypt the entry
    with open(file_name, "rb") as file:
        encrypted_entry = file.read()
    decrypted_entry = cipher_suite.decrypt(encrypted_entry).decode()
    
    print(f"\nToday's Diary Entry ({today}):\n")
    print(decrypted_entry)

# --- Main Program ---
if verify_password():
    while True:
        print("\n--- Virtual Diary ---")
        print("1. Write a new entry")
        print("2. Read today's entry")
        print("3. Exit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            save_entry()
        elif choice == "2":
            read_entry()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")
