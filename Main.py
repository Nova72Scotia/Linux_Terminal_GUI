#Import Statements
from tkinter import *
from tkinter.ttk import *
import os
from Linux_Terminal_GUI.LinkedList import LinkedList
from Linux_Terminal_GUI.LinkedStack import LinkedStack

def main_buttons():
  """The main_buttons function constructs and places the buttons of the main menu as well as reset some objects to default values. It is called in the functions beling to the Home, back, and forward, and Enter buttons as well as the inital flow of execution before entering mainloop. 0 Arguments"""
  global command_buttons
  global button_frame
  global command_dict
  global command_linked_list
  global user_label
  global user_entry
  global user_button
  global user_string
  #The user input is not needed at this point.
  user_label["text"] = "Input Unneeded"
  user_entry["state"] = DISABLED
  user_button["state"] = DISABLED
  user_string.set("")
  #Destroy prior buttons
  for i in command_buttons[::-1]:
    i.destroy()
    command_buttons.pop()
  #Main command button creation
  command_buttons.append(Button(button_frame, text =  "cat\nprint file", command = cat))
  command_buttons.append(Button(button_frame, text =  "cd\nchange directroy", command = cd))
  command_buttons.append(Button(button_frame, text =  "ls\nprint directory contents", command = ls))
  command_buttons.append(Button(button_frame, text =  "mkdir\nmake new directory", command = mkdir))
  command_buttons.append(Button(button_frame, text =  "pwd\nprint current directory", command = pwd))
  command_buttons.append(Button(button_frame, text =  "rm\ndelete file", command = rm))
  command_buttons.append(Button(button_frame, text =  "rmdir\ndelete directory", command = rmdir))
  command_buttons.append(Button(button_frame, text =  "touch\ncreate empty file", command = touch))
  #Automated placement in the grid structure
  ro = 0
  col = 0
  for k in command_buttons:
    k.grid(column = col, row = ro, padx = 5, pady = 3)
    col += 1
    if col == 4:
      ro += 1
      col = 0

def secondary_buttons(command_name):
  """Called by the helper functions for the command buttons created in the main_buttons function. Creates buttons for modifiers and activates the user_frame components"""
  global command_dict
  global command_buttons
  global button_frame
  global user_label
  global user_entry
  global user_button
  #Reset entry from forward and back functions and adds command to the Command LinkedList
  command_linked_list.clear()
  command_string_update()
  command_linked_list.add(command_name, 0)
  command_string_update()
  #Destroys main command buttons
  for i in command_buttons[::-1]:
    i.destroy()
    command_buttons.pop()
  #Creates modifier buttons if needed and builds a personal function for the button
  for i in command_dict[command_name][1]:

    def add_modifier(mod = i[0]):
      """Wrapped within the secondary_buttons function. This function allows buttons created in a loop to have a specialized function which passes its unique info along. 1 Arguments: 1st: Automatically obtained from dictionary through default"""
      global command_linked_list
      command_linked_list.add(mod, 1)
      command_string_update()
    
    command_buttons.append(Button(button_frame, text =  i[0] + "\n" + i[1], command = add_modifier))
  #Sets grid placement for modifier buttons
  ro = 0
  col = 0
  for k in command_buttons:
    k.grid(column = col, row = ro, padx = 5, pady = 3)
    col += 1
    if col == 4:
      ro += 1
      col = 0
  #Activates user input widgets if desired
  if command_dict[command_name][2][0]:
    user_label["text"] = command_dict[command_name][2][1]
    user_entry["state"] = ACTIVE
    user_button["state"] = ACTIVE
    

def cat():
  """Helper function for the cat button. 0 Arguments"""
  secondary_buttons("cat")

def cd():
  """Helper function for the cd button. 0 Arguments"""
  secondary_buttons("cd")

def ls():
  """Helper function for the ls button. 0 Arguments"""
  secondary_buttons("ls")

def mkdir():
  """Helper function for the mkdir button. 0 Arguments"""
  secondary_buttons("mkdir")

def pwd():
  """Helper function for the pwd button. 0 Arguments"""
  secondary_buttons("pwd")

def rm():
  """Helper function for the rm button. 0 Arguments"""
  secondary_buttons("rm")

def rmdir():
  """Helper function for the rmdir button. 0 Arguments"""
  secondary_buttons("rmdir")
  
def touch():
  """Helper function for the touch button. 0 Arguments"""
  secondary_buttons("touch")

def back():
  """Called by the back button and makes use of a LinkedList. Allows user to move back through past commands. 0 Arguments"""
  global viewer_list
  global viewer_index
  global command_string
  #Moves an index through a list and sends the corresponding item to the Command Entry
  if viewer_index != len(viewer_list) - 1:
    viewer_index += 1
    command_string.set(viewer_list[viewer_index])
  main_buttons()

def forward():
  """Called by the forward button and makes use of a LinkedList. Allows uer to move forwards through past commands. 0 Arguments"""
  global viewer_list
  global viewer_index
  global command_string
  #Moves an index through a list and sends the corresponding item to the Command Entry
  if viewer_index >= 0:
    viewer_index -= 1
    command_string.set(viewer_list[viewer_index])
  main_buttons()

def history_update():
  """Called whenever a command is entered and makes use of a LinkedStack. Overwrites command_history.txt with the 50 most recent commands. 0 Arguments"""
  global command_stack
  #Clones the command stack which contains the initial command_history.txt data and any commands called since. Then writes it back to file
  helper_stack = command_stack.clone()
  command_history =   open("/home/runner/Nova72Scotiapy/Linux_Terminal_GUI/command_history.txt", "w")
  for i in range(min(len(helper_stack), 50)):
    command_history.write(helper_stack.peek() + "\n")
    helper_stack.pop()
  command_history.close()

def command_string_update():
  """This function performs LinkedList to the necessary string format for commands and then sets that string to the Command Entry. 0 Arguments"""
  global command_string
  global command_linked_list
  command_string.set(" ".join( \
    str(command_linked_list)[2 : -2].split('", "')))

def user_submit():
  """Adds user input to the Command LinkedList. 0 Arguments"""
  global user_string
  global command_linked_list
  #Condition handles cases where a user has already inputted a value
  if len(command_linked_list) > 1 and command_linked_list[len(command_linked_list) - 1][0] != "-":
    command_linked_list[len(command_linked_list) - 1] = user_string.get()
  else:
    command_linked_list.add(user_string.get(), len(command_linked_list))
  user_string.set("")
  command_string_update()

def enter():
  "Function is called by the enter button and performs a wide variety of actions including interaction with the terminal. 0 Arguments"
  global command_string
  global command_stack
  global viewer_list
  global viewer_index
  global output_text
  command = command_string.get()
  #cd commands are ineffective through a shell, so their results must be implemented with the aid of the os module
  if command[: 2] == "cd" and "--help" not in command:
    path = os.popen("pwd").read()[: -1]
    #Handling for 'cd ..' command
    if command_string.get()[: -2] == "..":
      char = None
      i = len(path)
      while char != "/":
        i -= 1
        char = path[i]
      os.chdir(path[: i])
    else:
      new_path = command_string.get().split(" ")[-1]
      #Handles both relative and absolute paths
      if new_path[0] == "/":
        os.chdir(new_path)
      else:
        os.chdir(path + "/" + new_path)
  else:
    #This line runs the command through the terminal
    output = os.popen(command).read()
    print(output)
    #Displays output in text widget
    output_text.insert(END, output)
  #Adding command to the command history LinkedStack
  command_linked_list.clear()
  command_string_update()
  command_stack.push(command)
  viewer_list = command_stack.convert_to_list()
  viewer_index = -1
  history_update()
  main_buttons()

#Initialization of all global variables. Global variables are convenient for tkinter use as arguments and return values are often difficult or impossible
global command_buttons
global command_string
global user_string
global user_entry
global user_label
global user_button
global button_frame
global output_text
global command_dict
global command_linked_list
global command_stack
global viewer_list
global viewer_index
#Information dictionary for button building. Element one of lists is the text displayed along with the command on buttons. Element two of the lists is a list of lists with modifiers and modifier explanations. Element three controls the activation and text of the user input widgets.
command_dict = { \
  "cat": ["print file", [["-A", "show all"], ["-n", "number lines"], ["--help", "help"]], [True, "Enter file name:"]], \
  "cd" : ["change directroy", [], [True, "Enter directory path:"]], \
  "ls": ["print directory contents", [["-a", "all"], ["-l", "long"], ["-r", "reverse"], ["-R", "recursive"], ["-s", "size"], ["-t", "sort by time"], ["-U", "unsorted"], ["--help", "help"]], [True, "Enter Directory path"]], \
  "mkdir": ["make new directory", [["-v", "verbose"], ["--help", "help"]], [True, "Enter new directory name:"]], \
  "pwd": ["print current directory", [], [False, None]], \
  "rm": ["delete file", [["-v", "verbose"], ["--help", "help"]], [True, "Enter file name:"]], \
  "rmdir": ["delete directory", [["-v", "verbose"], ["--help", "help"]], [True, "Enter directory name:"]], \
  "touch": ["create empty file", [["--help", "help"]], [True, "Enter new file name:"]] \
}
command_buttons = []
command_linked_list = LinkedList()
main_window = Tk()
#Sets window to fullscreen
main_window.geometry(str(main_window.winfo_screenwidth()) + "x" + str(main_window.winfo_screenheight()))
command_string = StringVar(main_window)
user_string = StringVar(main_window)
#input_frame contains all buttons, form left side of window
input_frame = Frame(main_window, padding = 10)
input_frame.grid(column = 0, row = 0)
#home_frame contains Home and Close buttons
home_frame = Frame(input_frame, padding = 10)
home_frame.grid(column = 0, row = 0)
home_button = Button(home_frame, text = "Home", command = main_buttons)
home_button.grid(column = 0, row = 0, padx = 20)
close_button = Button(home_frame, text = "Close", command = main_window.destroy)
close_button.grid(column = 1, row = 0, padx = 20)
#button_frame contains grid of the varying command and modifier buttons
button_frame = Frame(input_frame, padding = 10)
button_frame.grid(column = 0, row = 1)
#user_frame contains user input widgets which are sometimes disabled
user_frame = Frame(input_frame, padding = 10)
user_frame.grid(column = 0, row = 2)
user_label = Label(user_frame, text = "Input unneeded:")
user_label.grid(column = 0, row = 0, padx = 2)
user_entry = Entry(user_frame, textvariable = user_string, state = DISABLED)
user_entry.grid(column = 1, row = 0, padx = 2)
user_button = Button(user_frame, text = "Submit", command = user_submit, state = DISABLED)
user_button.grid(column = 2, row = 0, padx = 2)
#entry_frame contains the Command Entry and  Enter, forward, and back buttons
entry_frame = Frame(input_frame, padding = 10)
entry_frame.grid(column = 0, row = 3)
forward_button = Button(entry_frame, text = "forward", command = forward)
forward_button.grid(column = 0, row = 0)
back_button = Button(entry_frame, text = "back", command = back)
back_button.grid(column = 0, row = 1)
command_entry = Entry(entry_frame, textvariable = command_string, width = 40)
command_entry.grid(column = 1, row = 0, pady = 4, padx = 15)
enter_button = Button(entry_frame, text = "Enter", command = enter)
enter_button.grid(column = 1, row = 1, pady = 4, padx = 15)
#output_frame fills the right side of the window and contains a text and scrollbar widget
output_frame = Frame(main_window, padding = 10)
output_frame.grid(column = 1, row = 0)
output_scrollbar = Scrollbar(output_frame)
output_text = Text(output_frame, height = 25, width = 40, yscrollcommand = output_scrollbar.set)
output_text.pack(side = LEFT)
output_scrollbar.pack(side = RIGHT, fill = Y)
output_scrollbar["command"] = output_text.yview
#Loads the recorded commands from prior sessions into a LinkedStack
command_history = open("/home/runner/Nova72Scotiapy/Linux_Terminal_GUI/command_history.txt", "r")
old_commands = command_history.readlines()
command_history.close()
for i in range(len(old_commands)):
  old_commands[i] = old_commands[i][: -1]
command_stack = LinkedStack(old_commands)
viewer_list = command_stack.convert_to_list()
viewer_index = -1
#Initial function call
main_buttons()
#event loop
main_window.mainloop()
