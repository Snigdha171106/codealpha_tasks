import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime

from chatbot import get_response


def get_time():
    return datetime.now().strftime("%I:%M %p")


def send_message(event=None):

    user_text = entry.get().strip()

    if not user_text:
        return

    timestamp = get_time()

    chat_area.config(state=tk.NORMAL)

    chat_area.insert(
        tk.END,
        f"\n[{timestamp}]\nYou: {user_text}\n",
        "user"
    )

    response = get_response(user_text)

    chat_area.insert(
        tk.END,
        f"Bot: {response}\n",
        "bot"
    )

    chat_area.config(state=tk.DISABLED)

    chat_area.yview(tk.END)

    entry.delete(0, tk.END)


def clear_chat():

    chat_area.config(state=tk.NORMAL)

    chat_area.delete("1.0", tk.END)

    chat_area.insert(
        tk.END,
        "Bot: Hello! Welcome to the FAQ Chatbot.\n"
        "Ask me about orders, shipping, refunds, payments, accounts, or support.\n\n"
    )

    chat_area.config(state=tk.DISABLED)


def save_chat():

    content = chat_area.get("1.0", tk.END)

    with open(
        "chat_history.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(content)

    messagebox.showinfo(
        "Saved",
        "Chat saved as chat_history.txt"
    )


# -------------------- MAIN WINDOW --------------------

root = tk.Tk()

root.title("FAQ Chatbot Assistant")

root.geometry("800x600")

root.configure(bg="#1e1e1e")


# -------------------- TITLE --------------------

title = tk.Label(
    root,
    text="🤖 FAQ Chatbot Assistant",
    font=("Arial", 18, "bold"),
    bg="#1e1e1e",
    fg="white"
)

title.pack(pady=10)


# -------------------- CHAT AREA --------------------

chat_area = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    font=("Arial", 11),
    bg="#252526",
    fg="white"
)

chat_area.pack(
    padx=15,
    pady=10,
    fill=tk.BOTH,
    expand=True
)

chat_area.tag_config(
    "user",
    foreground="#4FC3F7"
)

chat_area.tag_config(
    "bot",
    foreground="#81C784"
)

chat_area.insert(
    tk.END,
    "Bot: Hello! Welcome to the FAQ Chatbot.\n"
    "Ask me about orders, shipping, refunds, payments, accounts, or support.\n\n"
)

chat_area.config(state=tk.DISABLED)


# -------------------- INPUT FRAME --------------------

input_frame = tk.Frame(
    root,
    bg="#1e1e1e"
)

input_frame.pack(
    fill=tk.X,
    padx=10,
    pady=5
)


entry = tk.Entry(
    input_frame,
    font=("Arial", 12)
)

entry.pack(
    side=tk.LEFT,
    fill=tk.X,
    expand=True,
    padx=(0, 10)
)


send_button = tk.Button(
    input_frame,
    text="Send",
    font=("Arial", 11, "bold"),
    command=send_message
)

send_button.pack(
    side=tk.RIGHT
)


# -------------------- ACTION BUTTONS --------------------

button_frame = tk.Frame(
    root,
    bg="#1e1e1e"
)

button_frame.pack(
    pady=5
)


clear_button = tk.Button(
    button_frame,
    text="Clear Chat",
    command=clear_chat
)

clear_button.pack(
    side=tk.LEFT,
    padx=5
)


save_button = tk.Button(
    button_frame,
    text="Save Chat",
    command=save_chat
)

save_button.pack(
    side=tk.LEFT,
    padx=5
)


# -------------------- ENTER KEY SUPPORT --------------------

root.bind(
    "<Return>",
    send_message
)


root.mainloop()