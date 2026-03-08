import json
import getpass
import random
import string
from encryption import load_key, encrypt_password, decrypt_password

key = load_key()


def generate_password():
    length = 12
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))

    print("\nGenerated Strong Password:", password)


def save_password():
    website = input("Enter website: ")
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    encrypted = encrypt_password(password, key)

    data = {
        "website": website,
        "username": username,
        "password": encrypted.decode()
    }

    with open("database.json", "a") as file:
        json.dump(data, file)
        file.write("\n")

    print("Password saved securely!")


def view_passwords():
    try:
        with open("database.json", "r") as file:
            for line in file:
                data = json.loads(line)
                decrypted = decrypt_password(data["password"].encode(), key)

                print("\nWebsite:", data["website"])
                print("Username:", data["username"])
                print("Password:", decrypted)

    except FileNotFoundError:
        print("No passwords stored yet.")


def search_password():
    website_search = input("Enter website to search: ")

    try:
        with open("database.json", "r") as file:
            found = False

            for line in file:
                data = json.loads(line)

                if data["website"] == website_search:
                    decrypted = decrypt_password(data["password"].encode(), key)

                    print("\nWebsite:", data["website"])
                    print("Username:", data["username"])
                    print("Password:", decrypted)

                    found = True
                    break

            if not found:
                print("Website not found!")

    except FileNotFoundError:
        print("No passwords stored yet.")


while True:
    print("\n1. Save Password")
    print("2. View Passwords")
    print("3. Generate Strong Password")
    print("4. Search Password")
    print("5. Exit")

    choice = input("Choose option: ")

    if choice == "1":
        save_password()

    elif choice == "2":
        view_passwords()

    elif choice == "3":
        generate_password()

    elif choice == "4":
        search_password()

    elif choice == "5":
        break

    else:
        print("Invalid choice")