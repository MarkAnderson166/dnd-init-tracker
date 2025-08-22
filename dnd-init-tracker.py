# ------------------------------------------------------------
# --------- Mark Anderson ------------------------------------
# ------------------------------------------------------------

import tkinter as tk
from tkinter import ttk
from random import *
from time import time, sleep

# button functions

button_1_label = 'Wildfire\n(combat)'
red_list_combat = ['Heroic', 'Terrified', 'Bloodthirsty',
                  'Hesitant', 'Desperate', 'Paralyzed',
                  'Ruthless', 'Aggressive', 'Shaken',
                  'Victorious', 'Wounded']
def button_1_func():
  text_box('Wildfire (combat): %s' % choice(red_list_combat) )
  tksleep(3)
  canvas.after(6000,dice(4,5))


button_2_label = 'Wildfire\n(social)'
red_list_social = ['Relaxed', 'Anxious', 'Bored',
                  'Frustrated', 'Playful', 'Optimistic',
                  'Indifferent', 'Grateful', 'Impatient',
                  'Distrustful', 'Enthusiastic', 'Curious']
def button_2_func():
  text_box('Wildfire (social): %s' % choice(red_list_social) )
  #dice(2,4,1)


def text_box(text):
  canvas.delete('text_box_entry')
  text_box_array.append(text)
  y_offset = HEIGHT-35

  if len(text_box_array) > 7:
      text_box_array.pop(0)
      y_offset = HEIGHT-35

  shade = 250
  for line in reversed(text_box_array):
      y_offset = y_offset-20
      shade -= 25
      rgb = "#%02x%02x%02x" % ((shade),(shade),(shade))

      canvas.create_text(10, y_offset, anchor="nw",font="Times 13",
                         text= line, fill=rgb, tags='text_box_entry')


def dice(number,dice,plus=0):
  result = plus
  arr = []
  for i in range(number):
    roll = randint(1,dice)
    arr.append(roll)
    result = result+roll
  if plus:
    arr.append(plus)
    text_box('%sd%s+%s = %s = %s'%(number, dice, plus, arr, result))
  else:
    text_box('%sd%s = %s = %s'%(number, dice, arr, result))
  return result


def open_notes():
  try:
    text_file = open("names.txt", "r")
    notes = text_file.read()
    notes_box.insert("end-1c", notes)
    text_file.close()

    text_file = open("names.txt", "r")
    names = text_file.read()

      #remove last sessions initiative rolls
    for name in names:
      name = name.translate(translation_table)
      names_box.insert("end-1c", name)
    text_file.close()
  except:
    pass

def save():
  text_file = open("names.txt", "w")
  text_file.write(notes_box.get(1.0, "end-1c"))
  text_file.close()
  text_box('Notes saved')

  text_file = open("names.txt", "w")
  text_file.write(names_box.get(1.0, "end-1c"))
  text_file.close()
  text_box('Names saved')

def save_and_quit():
  save()
  quit()


def tksleep(t):
    'emulating time.sleep(seconds)'
    ms = int(t*1000)
    root = tk._get_default_root('sleep')
    var = tk.IntVar(root)
    root.after(ms, var.set, 1)
    root.wait_variable(var)


def move_turn_arrow():

  pointer = ''
  int_rolls = int_roll_box.get(1.0, "end-1c")
  pad = len(int_rolls.split('\n'))
  players = len(names_box.get(1.0, "end-1c").split('\n'))

  if any(char.isdigit() for char in int_rolls) and not pad == players:
    text_box('Error: you must set before next')

  else:

    for i in range(pad):
      pointer = ' \n%s' % pointer
    pointer = pointer+ '>>'
    if pad == players-1: pointer = '>>'

    int_roll_box.delete("1.0","end-1c")
    int_roll_box.insert("end-1c", pointer)


def sort_initiative():

  int_roll = int_roll_box.get(1.0, "end-1c").split('\n')
  players = names_box.get(1.0, "end-1c").split('\n')

  while('' in int_roll):int_roll.remove('')
  while('' in players):players.remove('')

  if len(int_roll) != len(players):
    text_box('Error: 1 roll per character is required')

  elif '>>' in int_roll:
    text_box('Error: >> in roll column')


  else:
    int_roll_box.delete("1.0","end-1c")
    int_roll_box.insert("end-1c", '>>')

    names_box.delete("1.0","end-1c")
    players_sorted = []
    for i in range(len(players)):
      name = players[i].translate(translation_table)
      roll = int_roll[i]
      if len(roll) == 1:
        roll = '0%s'%roll
      name = '%s - %s\n' % (roll, name)
      players_sorted.append(name)

    players_sorted = sorted(players_sorted, key=lambda s: int(s[:2]),reverse=1)
    for name in players_sorted:
      names_box.insert("end-1c", name)


#  GUI

WIDTH = 320
HEIGHT = 850

root = tk.Tk()
root.title("DnD Sidebar")
root.attributes('-topmost',True)
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.configure(bg='#111')
canvas.pack()
text_box_array = []
translation_table = str.maketrans('', '', '0123456789 -')


notes_frame = tk.Frame(canvas, width=WIDTH-165, height=HEIGHT-175, bg='#111')
canvas.create_window(5, 5, window=notes_frame, anchor="nw")
notes_box = tk.Text(notes_frame, bg='#312', foreground="light grey",
                  insertbackground='white', font=("Arial", 14),
                  bd=0, relief='ridge')
notes_box.place(x=5, y=5)

turn_frame = tk.Frame(canvas, width=30, height=HEIGHT-460, bg='#111')
canvas.create_window(WIDTH-160, 5, window=turn_frame, anchor="nw")
int_roll_box = tk.Text(turn_frame, bg='#131', foreground="light grey",
                  insertbackground='white', font=("Arial", 14),
                  bd=0, relief='ridge')
int_roll_box.place(x=5, y=5)

turn_frame = tk.Frame(canvas, width=125, height=HEIGHT-460, bg='#111')
canvas.create_window(WIDTH-130, 5, window=turn_frame, anchor="nw")
names_box = tk.Text(turn_frame, bg='#311', foreground="light grey",
                  insertbackground='white', font=("Arial", 14),
                  bd=0, relief='ridge')
names_box.place(x=5, y=5)


  # buttons

style = ttk.Style()
style.theme_use("clam")
style.configure('TButton', background='#444', foreground='#fff', relief='flat')
style.map('TButton', background=[('active', '#555')])

btnO_X = WIDTH-155
btnO_Y = HEIGHT-450
btnS_X = 150
btnS_Y1 = 75
btnS_Y2 = 30


# turn tracker buttons
btn=ttk.Button(root, text="Next", style="TButton",
                      command=move_turn_arrow).place(
                      x = btnO_X, y = btnO_Y,
                      width = btnS_X, height = btnS_Y1)

btn=ttk.Button(root, text="Set Initiative", style="TButton",
                      command=sort_initiative).place(
                      x = btnO_X, y = btnO_Y + btnS_Y1 + 5,
                      width = btnS_X, height = btnS_Y2)

# main 2 buttons
btn=ttk.Button(root, text=button_1_label, style="TButton",
                      command=button_1_func).place(
                      x = btnO_X, y = btnO_Y + btnS_Y1 + btnS_Y2 + 5*2,
                      width = btnS_X, height = btnS_Y1)

btn=ttk.Button(root, text=button_2_label, style="TButton",
                      command=button_2_func).place(
                      x = btnO_X, y = btnO_Y + btnS_Y1*2 + btnS_Y2 + 5*3,
                      width = btnS_X, height = btnS_Y1)

# bottom buttons
btn=ttk.Button(root, text="Save", style="TButton",
                      command=save).place(
                      x = 8, y = HEIGHT - btnS_Y2 - 5,
                      width = btnS_X, height = btnS_Y2)

btn=ttk.Button(root, text="Exit", style="TButton",
                      command=save_and_quit).place(
                      x = btnO_X, y = HEIGHT - btnS_Y2 - 5,
                      width = btnS_X, height = btnS_Y2)


  # -- mouse
def click(event):
  text_box('mouse click at %s , %s ' % (event.x, event.y))
canvas.bind('<Button-1>', click)

open_notes()
root.mainloop()


'''

import tkinter as tk
from random import randint

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Main Application")
        self.geometry("500x400")

        self.create_widgets()

    def create_widgets(self):
        # Create text boxes for the main window
        self.text_box1 = tk.Entry(self, width=30, font=("Arial", 14))
        self.text_box1.grid(row=0, column=0, padx=20, pady=10)

        self.text_box2 = tk.Entry(self, width=30, font=("Arial", 14))
        self.text_box2.grid(row=1, column=0, padx=20, pady=10)

        self.text_box3 = tk.Entry(self, width=30, font=("Arial", 14))
        self.text_box3.grid(row=2, column=0, padx=20, pady=10)

        self.text_box4 = tk.Entry(self, width=30, font=("Arial", 14))
        self.text_box4.grid(row=3, column=0, padx=20, pady=10)

        # Create number pad buttons
        button_values = [1, 5, 10, 15, 20, 25]
        for i, value in enumerate(button_values):
            button = tk.Button(self, text=str(value), width=5, height=2, command=lambda v=value: self.update_textbox(v))
            button.grid(row=i//3, column=i%3 + 1, padx=5, pady=5)

        # Up, Down, Roll buttons
        self.up_button = tk.Button(self, text="Up", width=5, height=2, command=self.increment_value)
        self.up_button.grid(row=2, column=3, padx=5, pady=5)

        self.down_button = tk.Button(self, text="Down", width=5, height=2, command=self.decrement_value)
        self.down_button.grid(row=3, column=3, padx=5, pady=5)

        self.roll_button = tk.Button(self, text="Roll", width=5, height=2, command=self.roll_value)
        self.roll_button.grid(row=4, column=3, padx=5, pady=5)

        # OK button
        self.ok_button = tk.Button(self, text="OK", width=5, height=2, command=self.insert_value)
        self.ok_button.grid(row=4, column=0, columnspan=3, pady=10)

        # Store the currently selected value
        self.selected_value = None
        self.current_entry = None

        # Add events to text boxes
        self.text_box1.bind("<Button-1>", lambda e: self.set_current_textbox(self.text_box1))
        self.text_box2.bind("<Button-1>", lambda e: self.set_current_textbox(self.text_box2))
        self.text_box3.bind("<Button-1>", lambda e: self.set_current_textbox(self.text_box3))
        self.text_box4.bind("<Button-1>", lambda e: self.set_current_textbox(self.text_box4))

    def set_current_textbox(self, textbox):
        self.current_entry = textbox
        self.selected_value = None  # Reset value on new selection

    def update_textbox(self, value):
        # If no textbox is selected, return
        if not self.current_entry:
            return
        # If there is no selected value, set it
        if self.selected_value is None:
            self.selected_value = value
        else:
            self.selected_value = value
        self.current_entry.delete(0, tk.END)
        self.current_entry.insert(0, str(self.selected_value))

    def increment_value(self):
        # Get the current value from the text box
        current_value = self.get_current_value()
        if current_value is not None:
            self.selected_value = current_value + 1
            self.update_selected_value()

    def decrement_value(self):
        # Get the current value from the text box
        current_value = self.get_current_value()
        if current_value is not None:
            self.selected_value = current_value - 1
            self.update_selected_value()

    def roll_value(self):
        self.selected_value = randint(1, 20)
        self.update_selected_value()

    def get_current_value(self):
        # Try to get the current value from the selected text box, if it's valid
        if self.current_entry:
            try:
                value = int(self.current_entry.get())
                return value
            except ValueError:
                # If the value is not a valid integer, return None
                return None
        return None

    def update_selected_value(self):
        # Update the selected value into the textbox
        if self.current_entry and self.selected_value is not None:
            self.current_entry.delete(0, tk.END)
            self.current_entry.insert(0, str(self.selected_value))

    def insert_value(self):
        # Insert the selected value into the currently active text box
        if self.current_entry and self.selected_value is not None:
            self.current_entry.delete(0, tk.END)
            self.current_entry.insert(0, str(self.selected_value))
        self.selected_value = None  # Reset the value after inserting


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
#

'''
