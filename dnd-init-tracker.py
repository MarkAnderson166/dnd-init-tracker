# ------------------------------------------------------------
# --------- Mark Anderson ------------------------------------
# ------------------------------------------------------------

import tkinter as tk
from tkinter import ttk
from random import randint
import json
import os
from tkinter import messagebox


class MainApplication(tk.Tk):

  def __init__(self):
    super().__init__()
    self.title("Initiative Tracker")
    self.geometry("350x670")
    self.minsize(350, 670)
    self.attributes('-topmost', True)
    self.configure(bg='#222')
    self.create_widgets()
    self.turn_index = 0
    self.highlight_tag = "highlight"
    self.load()

  def create_widgets(self):
    button_values = [1, 5, 10, 15, 20, 25]
    padding = 3
    width = 4
    fontsize = 22

    # Configure resizing for rows and columns
    for i in range(14):  # rows 0 to 13
      self.grid_rowconfigure(i, weight=1, minsize=30)
    for i in range(3):  # columns 0 to 2
      self.grid_columnconfigure(i, weight=20, minsize=50)

    self.style = ttk.Style()
    self.style.theme_use("clam")
    self.style.configure('TButton', background='#522', foreground='#bbb', relief='flat',
                         font=("Arial", fontsize - 4), width=width)
    self.style.map('TButton', background=[('active', '#555')])

    self.style.configure("Custom.TEntry", fieldbackground="#000", foreground="#aaa",
                         bordercolor="#312", lightcolor="#000", darkcolor="#000",
                         borderwidth=4, relief="flat")
    self.style.map("Custom.TEntry", fieldbackground=[('focus', '#353')])

    self.style.configure("Selected.TEntry", fieldbackground="#444", foreground="#fff")
    self.style.configure("Turn.TEntry", fieldbackground="#262", foreground="#fff")
    self.style.configure("Highlighted.TEntry", fieldbackground="#353", foreground="#fff",
                         bordercolor="#312", relief="flat", padding=0)

    self.text_boxes = []

    for i in range(14):
      entry = ttk.Entry(self, width=12, font=("Arial", fontsize), style="Custom.TEntry")
      entry.grid(row=i, column=2, padx=padding, pady=padding, sticky='nsew')
      setattr(self, f'text_box{i+1}', entry)
      self.text_boxes.append(entry)
      entry.bind("<Button-1>", lambda e, ent=entry: self.set_current_textbox(ent))

    self.sort_button = ttk.Button(self, text="Sort", width=width,
                                  command=self.sort_textbox_entries, style="TButton")
    self.sort_button.grid(row=0, column=0, columnspan=2, padx=padding, pady=padding, sticky="nsew")

    for i, value in enumerate(button_values):
      row = i // 2
      col = i % 2
      button = ttk.Button(self, text=str(value), width=width,
                          command=lambda v=value: self.update_textbox(v), style="TButton")
      button.grid(row=row + 2, column=col, padx=padding, pady=padding, sticky="nsew")

    self.up_button = ttk.Button(self, text="+", command=lambda v=-7: self.update_textbox(v), style="TButton")
    self.up_button.grid(row=5, column=1, rowspan=2, padx=padding, pady=padding, sticky="nsew")

    self.down_button = ttk.Button(self, text="-", command=lambda v=-8: self.update_textbox(v), style="TButton")
    self.down_button.grid(row=5, column=0, rowspan=2, padx=padding, pady=padding, sticky="nsew")

    self.roll_button = ttk.Button(self, text="Roll", command=lambda v=-9: self.update_textbox(v), style="TButton")
    self.roll_button.grid(row=7, column=0, padx=padding, pady=padding, columnspan=2, sticky="nsew")

    self.move_up_button = ttk.Button(self, text="^", command=self.move_entry_up, style="TButton")
    self.move_up_button.grid(row=9, column=0, sticky="nsew", padx=padding, pady=padding)

    self.move_down_button = ttk.Button(self, text="v", command=self.move_entry_down, style="TButton")
    self.move_down_button.grid(row=9, column=1, sticky="nsew", padx=padding, pady=padding)

    self.strip_button = ttk.Button(self, text="Strip", width=width, command=self.strip_numbers, style="TButton")
    self.strip_button.grid(row=10, column=0, columnspan=2, padx=padding, pady=padding, sticky="nsew")

    self.next_button = ttk.Button(self, text="Next", width=width, command=self.move_next, style="TButton")
    self.next_button.grid(row=12, column=0, rowspan=2, columnspan=2, padx=padding, pady=padding, sticky="nsew")

    self.selected_value = None
    self.current_entry = None

  def set_current_textbox(self, textbox):
    for entry in self.text_boxes:
      entry.configure(style="Custom.TEntry")
    textbox.configure(style="Selected.TEntry")
    self.current_entry = textbox
    self.selected_value = None

  def update_textbox(self, value):
    if not self.current_entry:
      return
    current_value, name = self.get_current_value()
    if value == -9:
      value = randint(1, 20)
    elif value == -8:
      value = current_value - 1
    elif value == -7:
      value = current_value + 1
    new = f"{value:>2}: {name}"
    self.current_entry.delete(0, tk.END)
    self.current_entry.insert(0, new)
    self.save()

  def get_current_value(self):
    value = 0
    name = ""
    if self.current_entry:
      text = self.current_entry.get().strip()
      if ":" in text:
        parts = text.split(":", 1)
        try:
          value = int(parts[0].strip())
        except ValueError:
          value = 0
        name = parts[1].strip()
      else:
        parts = text.split()
        if parts:
          try:
            value = int(parts[0])
            name = " ".join(parts[1:]).strip()
          except ValueError:
            name = text
    return value, name

  def sort_textbox_entries(self):
    entries = []
    for entry in self.text_boxes:
      text = entry.get().strip()
      if text:
        try:
          number_part = int(text.split(":")[0]) if ":" in text else 0
          entries.append((number_part, text))
        except ValueError:
          continue

    entries.sort(key=lambda x: x[0], reverse=True)

    for i, (num, value) in enumerate(entries):
      self.text_boxes[i].delete(0, tk.END)
      if ":" in value:
        name = value.split(":", 1)[1].strip()
      else:
        parts = value.split()
        name = " ".join(parts).strip()
      formatted = f"{num:>2}: {name}"
      self.text_boxes[i].insert(0, formatted)

    for j in range(len(entries), len(self.text_boxes)):
      self.text_boxes[j].delete(0, tk.END)

    for entry in self.text_boxes:
      entry.configure(style="Custom.TEntry")

    for i, entry in enumerate(self.text_boxes):
      if entry.get().strip():
        entry.configure(style="Turn.TEntry")
        self.turn_index = i
        break
    else:
      self.turn_index = None

    self.current_entry = None
    self.selected_value = None
    self.save()

  def move_next(self):
    non_empty = [i for i, e in enumerate(self.text_boxes) if e.get().strip()]
    if not non_empty:
      return
    if self.turn_index is None or self.turn_index not in non_empty:
      self.turn_index = non_empty[0]
    else:
      idx = non_empty.index(self.turn_index)
      self.turn_index = non_empty[(idx + 1) % len(non_empty)]

    for entry in self.text_boxes:
      entry.configure(style="Custom.TEntry")

    self.text_boxes[self.turn_index].configure(style="Turn.TEntry")
    self.current_entry = None
    self.selected_value = None
    self.save()

  def update_highlighted_box(self):
    for i, entry in enumerate(self.text_boxes):
      if i == self.turn_index:
        entry.configure(style="Highlighted.TEntry")
      else:
        entry.configure(style="Custom.TEntry")

  def save(self):
    data = {
      "entries": [entry.get() for entry in self.text_boxes],
      "turn_index": self.turn_index
    }
    with open("names.txt", "w") as f:
      json.dump(data, f)

  def load(self):
    if not os.path.exists("names.txt"):
      return
    with open("names.txt", "r") as f:
      try:
        data = json.load(f)
      except json.JSONDecodeError:
        return
    entries = data.get("entries", [])
    for entry, text in zip(self.text_boxes, entries):
      entry.delete(0, tk.END)
      entry.insert(0, text)
    self.turn_index = data.get("turn_index", 0)
    self.update_highlighted_box()

  def strip_numbers(self):
    confirm = messagebox.askyesno("Confirm", "Strip all rolls?")
    if not confirm:
      return
    for entry in self.text_boxes:
      text = entry.get().strip()
      if ":" in text:
        parts = text.split(":", 1)
        name = parts[1].strip()
        entry.delete(0, tk.END)
        entry.insert(0, name)
    self.save()

  def move_entry_up(self):
    if not self.current_entry:
      return
    index = None
    for i, entry in enumerate(self.text_boxes):
      if entry == self.current_entry:
        index = i
        break
    if index is not None and index > 0:
      current_text = self.text_boxes[index].get()
      above_text = self.text_boxes[index - 1].get()
      self.text_boxes[index].delete(0, tk.END)
      self.text_boxes[index].insert(0, above_text)
      self.text_boxes[index - 1].delete(0, tk.END)
      self.text_boxes[index - 1].insert(0, current_text)
      self.set_current_textbox(self.text_boxes[index - 1])
      self.save()

  def move_entry_down(self):
    if not self.current_entry:
      return
    index = None
    for i, entry in enumerate(self.text_boxes):
      if entry == self.current_entry:
        index = i
        break
    if index is not None and index < len(self.text_boxes) - 1:
      current_text = self.text_boxes[index].get()
      below_text = self.text_boxes[index + 1].get()
      self.text_boxes[index].delete(0, tk.END)
      self.text_boxes[index].insert(0, below_text)
      self.text_boxes[index + 1].delete(0, tk.END)
      self.text_boxes[index + 1].insert(0, current_text)
      self.set_current_textbox(self.text_boxes[index + 1])
      self.save()


if __name__ == "__main__":
  app = MainApplication()
  app.mainloop()
