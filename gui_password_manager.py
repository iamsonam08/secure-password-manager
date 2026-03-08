import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
import string
import pyperclip
import time
import threading

from encryption import load_key, encrypt_password, decrypt_password

key = load_key()

real_passwords = {}
last_activity = time.time()


# ---------- PASSWORD GENERATOR ----------
def generate_password():

    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(12))

    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)


# ---------- PASSWORD STRENGTH ----------
def check_strength(event=None):

    password = password_entry.get()

    if len(password) < 6:
        strength_label.config(text="Weak", fg="red")

    elif len(password) < 10:
        strength_label.config(text="Medium", fg="orange")

    else:
        strength_label.config(text="Strong", fg="green")


# ---------- SHOW / HIDE PASSWORD ----------
def toggle_password():

    if password_entry.cget("show") == "":
        password_entry.config(show="*")
    else:
        password_entry.config(show="")


# ---------- SAVE PASSWORD ----------
def save_password():

    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if website == "" or username == "" or password == "":
        messagebox.showerror("Error", "All fields required")
        return

    encrypted = encrypt_password(password, key)

    data = {
        "website": website,
        "username": username,
        "password": encrypted.decode()
    }

    with open("database.json", "a") as file:
        json.dump(data, file)
        file.write("\n")

    load_passwords()

    messagebox.showinfo("Success", "Password Saved")

    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)


# ---------- LOAD PASSWORDS ----------
def load_passwords():

    real_passwords.clear()

    for row in table.get_children():
        table.delete(row)

    try:
        with open("database.json", "r") as file:

            for line in file:

                data = json.loads(line)

                decrypted = decrypt_password(data["password"].encode(), key)

                row_id = table.insert("", tk.END, values=(
                    data["website"],
                    data["username"],
                    "********"
                ))

                real_passwords[row_id] = decrypted

    except:
        pass


# ---------- COPY PASSWORD ----------
def copy_password():

    selected = table.focus()

    if not selected:
        messagebox.showerror("Error", "Select a row first")
        return

    password = real_passwords.get(selected)

    pyperclip.copy(password)

    messagebox.showinfo(
        "Copied",
        "Password copied to clipboard (will clear in 30 seconds)"
    )

    threading.Thread(target=clear_clipboard, daemon=True).start()


# ---------- CLEAR CLIPBOARD ----------
def clear_clipboard():

    time.sleep(30)

    pyperclip.copy("")

    messagebox.showinfo("Security", "Clipboard cleared automatically")


# ---------- DELETE PASSWORD ----------
def delete_password():

    selected = table.focus()

    if not selected:
        messagebox.showerror("Error", "Select a row first")
        return

    values = table.item(selected, "values")
    website = values[0]

    new_lines = []

    with open("database.json", "r") as file:

        for line in file:

            data = json.loads(line)

            if data["website"] != website:
                new_lines.append(line)

    with open("database.json", "w") as file:

        for line in new_lines:
            file.write(line)

    load_passwords()

    messagebox.showinfo("Deleted", "Password removed")


# ---------- SEARCH ----------
def search_password():

    keyword = search_entry.get().lower()

    real_passwords.clear()

    for row in table.get_children():
        table.delete(row)

    with open("database.json", "r") as file:

        for line in file:

            data = json.loads(line)

            if keyword in data["website"].lower():

                decrypted = decrypt_password(data["password"].encode(), key)

                row_id = table.insert("", tk.END, values=(
                    data["website"],
                    data["username"],
                    "********"
                ))

                real_passwords[row_id] = decrypted


# ---------- AUTO LOCK ----------
def update_activity(event=None):
    global last_activity
    last_activity = time.time()


def check_inactivity():
    global last_activity

    if time.time() - last_activity > 120:
        messagebox.showinfo("Locked", "Application locked due to inactivity")
        window.destroy()
        import login

    window.after(5000, check_inactivity)


# ---------- WINDOW ----------
window = tk.Tk()
window.title("Secure Password Manager")
window.geometry("1000x600")
window.configure(bg="#0f172a")

window.bind_all("<Key>", update_activity)
window.bind_all("<Motion>", update_activity)

check_inactivity()


# ---------- HEADER ----------
header = tk.Frame(window, bg="#1e40af", height=60)
header.pack(fill="x")

title = tk.Label(
    header,
    text="🔐 Secure Password Manager",
    font=("Segoe UI", 20, "bold"),
    fg="white",
    bg="#1e40af"
)

title.pack(pady=12)


# ---------- SIDEBAR ----------
sidebar = tk.Frame(window, bg="#020617", width=180)
sidebar.pack(side="left", fill="y")

tk.Label(
    sidebar,
    text="Dashboard",
    bg="#020617",
    fg="white",
    font=("Segoe UI", 14)
).pack(pady=20)

btn_style = {"width": 18, "font": ("Segoe UI", 10), "bd": 0}

tk.Button(sidebar, text="🔑 Generate", bg="#2563eb", fg="white",
          command=generate_password, **btn_style).pack(pady=6)

tk.Button(sidebar, text="💾 Save", bg="#22c55e", fg="white",
          command=save_password, **btn_style).pack(pady=6)

tk.Button(sidebar, text="📋 Copy", bg="#06b6d4", fg="white",
          command=copy_password, **btn_style).pack(pady=6)

tk.Button(sidebar, text="🗑 Delete", bg="#ef4444", fg="white",
          command=delete_password, **btn_style).pack(pady=6)


# ---------- MAIN ----------
main = tk.Frame(window, bg="#0f172a")
main.pack(fill="both", expand=True, padx=20, pady=10)


# ---------- INPUT CARD ----------
card = tk.Frame(main, bg="#1e293b", padx=40, pady=30)
card.pack(pady=10)

label_style = {"bg": "#1e293b", "fg": "white", "font": ("Segoe UI", 11)}

tk.Label(card, text="Website", **label_style).grid(row=0, column=0, pady=5)
website_entry = tk.Entry(card, width=35)
website_entry.grid(row=0, column=1)

tk.Label(card, text="Username", **label_style).grid(row=1, column=0, pady=5)
username_entry = tk.Entry(card, width=35)
username_entry.grid(row=1, column=1)

tk.Label(card, text="Password", **label_style).grid(row=2, column=0, pady=5)
password_entry = tk.Entry(card, width=35, show="*")
password_entry.grid(row=2, column=1)

password_entry.bind("<KeyRelease>", check_strength)

tk.Button(card, text="👁", bg="#3b82f6", fg="white",
          command=toggle_password).grid(row=2, column=2)

strength_label = tk.Label(card, text="", bg="#1e293b", fg="white")
strength_label.grid(row=3, column=1)


# ---------- SEARCH ----------
search_frame = tk.Frame(main, bg="#0f172a")
search_frame.pack(pady=10)

search_entry = tk.Entry(search_frame, width=35)
search_entry.grid(row=0, column=0)

tk.Button(search_frame, text="Search",
          bg="#2563eb", fg="white",
          command=search_password).grid(row=0, column=1, padx=5)


# ---------- TABLE ----------
style = ttk.Style()
style.theme_use("default")

style.configure(
    "Treeview",
    background="#e0f2fe",
    foreground="black",
    rowheight=30,
    fieldbackground="#e0f2fe"
)

table = ttk.Treeview(
    main,
    columns=("Website", "Username", "Password"),
    show="headings"
)

table.heading("Website", text="Website")
table.heading("Username", text="Username")
table.heading("Password", text="Password")

table.column("Website", width=250)
table.column("Username", width=250)
table.column("Password", width=250)

table.pack(fill="both", expand=True)

load_passwords()

window.mainloop()