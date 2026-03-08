# 🔐 Secure Password Manager

A desktop password manager built using Python and Tkinter that securely stores user credentials using encryption.

---

## 📌 Features

- Master password authentication
- AES-based encryption for storing passwords
- Password generator
- Copy password to clipboard
- Clipboard auto-clear security
- Search stored passwords
- Delete stored passwords
- Password strength indicator
- Auto lock after inactivity
- Modern dashboard UI

---

## 🛠 Technologies Used

- Python
- Tkinter (GUI)
- Cryptography Library
- PyInstaller
- JSON (for data storage)

---

## 🔐 Security Features

- Master password protected vault
- SHA256 hashing for authentication
- Fernet (AES-based) encryption
- Clipboard auto-clear after 30 seconds
- Password masking in table
- Auto lock after inactivity

---

## 📂 Project Structure

password_manager
│
├── login.py
├── gui_password_manager.py
├── encryption.py
├── database.json
├── master.key
└── secret.key

---

## ▶️ How to Run

1. Install Python
2. Install dependencies

pip install cryptography pyperclip

3. Run the application

python login.py

---

## 📦 Build EXE

pyinstaller --onefile --windowed login.py

---

## 👨‍💻 Author

Sonam Yadav