import tkinter as tk
from tkinter import messagebox
import hashlib
import os

MASTER_FILE = "master.key"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def set_master_password(password):
    with open(MASTER_FILE, "w") as f:
        f.write(hash_password(password))


def verify_password(password):
    with open(MASTER_FILE, "r") as f:
        stored = f.read()

    return stored == hash_password(password)


def login():
    password = password_entry.get()

    if verify_password(password):
        window.destroy()
        import gui_password_manager
    else:
        messagebox.showerror("Error", "Wrong Password")


def setup_master():
    password = password_entry.get()

    if password == "":
        messagebox.showerror("Error", "Password cannot be empty")
        return

    set_master_password(password)

    messagebox.showinfo("Success", "Master Password Set")

    window.destroy()

    import gui_password_manager


# ---------- UI ----------
window = tk.Tk()
window.title("Secure Password Manager Login")
window.geometry("350x200")
window.configure(bg="#2b2b2b")

frame = tk.Frame(window, bg="#2b2b2b")
frame.pack(expand=True)

title = tk.Label(
    frame,
    text="🔐 Password Manager",
    font=("Arial", 16),
    fg="white",
    bg="#2b2b2b"
)
title.pack(pady=10)

tk.Label(frame, text="Master Password", fg="white", bg="#2b2b2b").pack()

password_entry = tk.Entry(frame, show="*", width=25)
password_entry.pack(pady=5)

if os.path.exists(MASTER_FILE):

    tk.Button(
        frame,
        text="Login",
        width=15,
        command=login
    ).pack(pady=10)

else:

    tk.Button(
        frame,
        text="Set Master Password",
        width=20,
        command=setup_master
    ).pack(pady=10)

window.mainloop()