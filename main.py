import re
import tkinter as tk
from tkinter import filedialog, simpledialog, ttk
import gzip
import sv_ttk
from tkinter import messagebox as mb

# dictionary to map minecraft color codes to tkinter tag names and their corresponding colors
color_map = {
    "0": ("black", "#000000"),
    "1": ("dark_blue", "#0000AA"),
    "2": ("dark_green", "#00AA00"),
    "3": ("dark_aqua", "#00AAAA"),
    "4": ("dark_red", "#AA0000"),
    "5": ("dark_purple", "#AA00AA"),
    "6": ("gold", "#FFAA00"),
    "7": ("gray", "#AAAAAA"),
    "8": ("dark_gray", "#555555"),
    "9": ("blue", "#5555FF"),
    "a": ("green", "#55FF55"),
    "b": ("aqua", "#55FFFF"),
    "c": ("red", "#FF5555"),
    "d": ("light_purple", "#FF55FF"),
    "e": ("yellow", "#FFFF55"),
    "f": ("white", "#FFFFFF"),
}

background_color = "#1e1e1e"


# function to parse the log
def parse_log(log):
    chat_lines = []
    for line in log.split("\n"):
        if "[CHAT]" in line:
            chat_line = line.split("[CHAT] ")[1]
            chat_lines.append("§f" + chat_line)
    if not chat_lines:
        chat_lines.append(
            "§cNo chat messages found. Please select a different log file."
        )
    return chat_lines


# function to apply color tags to chat text
def apply_color_tags(text_widget, chat_lines):
    text_widget.config(state=tk.NORMAL)
    text_widget.delete(1.0, tk.END)

    current_tag = "white"  
    for line in chat_lines:
        parts = re.split(r"(§.)", line)
        for part in parts:
            if part.startswith("§") and len(part) > 1:
                color_code = part[1]
                if color_code in color_map:
                    current_tag = color_map[color_code][0]
            else:
                text_widget.insert(tk.END, part, current_tag)
        text_widget.insert(tk.END, "\n")

    text_widget.config(state=tk.DISABLED)


# function to open a file dialog and load the log
def load_log():
    global chat_lines
    file_path = filedialog.askopenfilename(
        filetypes=[("GZipped Log Files", "*.log.gz")]
    )
    if file_path:
        with gzip.open(file_path, "rt") as file:
            log = file.read()
        chat_lines = parse_log(log)
        apply_color_tags(chat_display, chat_lines)
        file_name = file_path.split("/")[-1]
        root.title(f"Minecraft Chat Log Viewer - {file_name}")


# function to filter chat lines by prefix
def filter_chat(prefix):
    try:

        filtered_lines = [line for line in chat_lines if line.startswith(f"§f{prefix}")]
        apply_color_tags(chat_display, filtered_lines)
    except NameError:
        mb.showinfo(title="Information", message="No chat log loaded.")

# function to reset chat display to original chat lines
def reset_filters():
    try:
        apply_color_tags(chat_display, chat_lines)
    except NameError:
        mb.showinfo(title="Information", message="No chat log loaded.")


# search variables
search_term = None
search_positions = []
current_search_index = 0


# function to search for a text string
def search_text():
    global search_term, search_positions, current_search_index
    search_term = simpledialog.askstring("Search", "Enter text to search:")
    if search_term:
        search_positions = []
        start_pos = "1.0"
        while True:
            start_pos = chat_display.search(search_term, start_pos, stopindex=tk.END)
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(search_term)}c"
            search_positions.append((start_pos, end_pos))
            start_pos = end_pos
        current_search_index = 0
        if search_positions:
            highlight_search_result()
        else:
            mb.showinfo(title="Information", message="No search results found.")


# function to highlight the current search result
def highlight_search_result():
    chat_display.tag_remove("highlight", "1.0", tk.END)
    if search_positions:
        start_pos, end_pos = search_positions[current_search_index]
        chat_display.tag_add("highlight", start_pos, end_pos)
        chat_display.tag_config("highlight", background="yellow", foreground="black")
        chat_display.see(start_pos)


# function to navigate to the next search result
def next_search_result(event):
    global current_search_index
    if search_positions:
        current_search_index = (current_search_index + 1) % len(search_positions)
        highlight_search_result()


# setting up the tkinter gui
root = tk.Tk()
root.title("Minecraft Chat Log Viewer")

chat_display = tk.Text(
    root,
    wrap=tk.WORD,
    font=("Minecraftia", 12),
    background=background_color,
    foreground="white",
    insertbackground="black",
    state=tk.DISABLED,
)
chat_display.pack(expand=True, fill="both")

# adding color tags to the text widget
for code, (tag_name, color) in color_map.items():
    chat_display.tag_config(tag_name, foreground=color)

button_frame = ttk.Frame(root)
button_frame.pack(fill=tk.X)

load_button = ttk.Button(button_frame, text="Load Chat Log", command=load_log)
load_button.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

party_filter_button = ttk.Button(
    button_frame,
    text="Filter Party Messages",
    command=lambda: filter_chat("§9Party §8>"),
)
party_filter_button.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

search_button = ttk.Button(button_frame, text="Search", command=search_text)
search_button.grid(row=0, column=2, padx=5, pady=5)

guild_filter_button = ttk.Button(
    button_frame, text="Filter Guild Messages", command=lambda: filter_chat("§2Guild >") or filter_chat("Guild >")
)
guild_filter_button.grid(row=0, column=3, padx=5, pady=5, sticky=tk.E)

reset_button = ttk.Button(button_frame, text="Reset Filters", command=reset_filters)
reset_button.grid(row=0, column=10, padx=5, pady=5, sticky=tk.E)

button_frame.columnconfigure(2, weight=1)  # make the search button column expand

# bind the Enter key to navigate through search results
root.bind("<Return>", next_search_result)

sv_ttk.set_theme("dark")

root.mainloop()
