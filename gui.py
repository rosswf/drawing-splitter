#! /usr/bin/env python

# GUI Interface for drawing_splitter.py using tkinter
from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog
import toml

import user_options

# Load settings.toml and use as defaults
settings = user_options.load_settings_toml()

# Command functions functions
# Browse for file and update entry box
def browsefunc(entry):
    folder = tkinter.filedialog.askdirectory()
    entry.config(state='normal')
    entry.delete(0, END)
    entry.insert(0, folder)
    entry.config(state='disabled')

# TODO: Add function for running splitter and saving toml
def save_config():
    settings = {}
    settings['dwg_number_element'] = string_dwg_number.get()
    with open('settings.toml', 'w') as settings_file:
        settings_file.write(toml.dumps(settings))

# Create window
window = Tk()
window.geometry('500x320')
window.resizable(False, False)
window.title("Drawing Splitter")

# Add program title
label_program_header = Label(master=window, text='Drawing Splitter', font=('Calibri', 16, 'bold'))
label_program_header.grid(row=0, column=0, columnspan=5, sticky='w', padx=5, pady=5)

# Create frame for inputs
input_frame = Frame(master=window, borderwidth=1)
input_frame.grid(row=1, column=0, padx=5, pady=5)

# Create items for input_frame
# Entry box for dwg_number_element
label_dwg_number = Label(master=input_frame, text='Number Element:', font=('Calibri', 10, 'bold'))
label_dwg_number.grid(row=0, column=0, pady=5)
string_dwg_number = StringVar()
entry_dwg_number = Entry(master=input_frame, textvariable=string_dwg_number)
entry_dwg_number.grid(row=0, column=1, pady=5, sticky='nsew', columnspan=3)
string_dwg_number.set(settings['dwg_number_element'])

# Entry box for input folder path, with button
label_input_folder = Label(master=input_frame, text='Input Folder:', font=('Calibri', 10, 'bold'))
label_input_folder.grid(row=1, column=0, sticky='e', pady=5)
string_input_folder = StringVar()
entry_input_folder = Entry(master=input_frame, state='disabled', width=50, textvariable=string_input_folder)
entry_input_folder.grid(row=1, column=1, pady=5, columnspan=5, sticky='nsew')
button_input_folder = Button(master=input_frame, text='Browse...', command=lambda: browsefunc(entry_input_folder))
button_input_folder.grid(row=2, column=5, sticky='e')
string_input_folder.set(settings['input_folder'])

# Entry box for output folder path, with button
label_output_folder = Label(master=input_frame, text='Output Folder:', font=('Calibri', 10, 'bold'))
label_output_folder.grid(row=3, column=0, sticky='e', pady=5)
string_output_folder = StringVar()
entry_output_folder = Entry(master=input_frame, state='disabled', width=50, textvariable=string_output_folder)
entry_output_folder.grid(row=3, column=1, pady=5, columnspan=5, sticky='nsew')
button_output_folder = Button(master=input_frame, text='Browse...', command=lambda: browsefunc(entry_output_folder))
button_output_folder.grid(row=4, column=5, sticky="e")
string_output_folder.set(settings['output_folder'])

# Drop down menu for delete files after processing
label_delete = Label(master=input_frame, text='Delete files:', font=('Calibri', 10, 'bold'))
label_delete.grid(row=5, column=0, sticky='e', pady=5)
string_delete = StringVar()
if settings['delete']:
    string_delete.set('Yes')
else:
    string_delete.set('No')
option_delete = OptionMenu(input_frame, string_delete, string_delete.get(), 'Yes', 'No')
option_delete.grid(row=5, column=1, sticky='w')

# Drop down box for saving by revision
label_revision = Label(master=input_frame, text='Save by revision:', font=('Calibri', 10, 'bold'))
label_revision.grid(row=6, column=0, sticky='e', pady=5)
string_revision = StringVar()
if settings['revision']:
    string_revision.set('Yes')
else:
    string_revision.set('No')
option_revision = OptionMenu(input_frame, string_revision, string_revision.get(), 'Yes', 'No')
option_revision.grid(row=6, column=1, sticky='w')

# Drop down box for region
label_region = Label(master=input_frame, text='Region:', font=('Calibri', 10, 'bold'))
label_region.grid(row=7, column=0, sticky='e', pady=5)
string_region = StringVar()
if settings['region'] == 'top-left':
    string_region.set('Top Left')
elif settings['region'] == 'top-right':
    string_region.set('Top Right')
elif settings['region'] == 'bot-left':
    string_region.set('Bottom Left')
elif settings['region'] == 'bot-right':
    string_region.set('Bottom Right')
option_region = OptionMenu(input_frame, string_region, string_region.get(), 'Top Left', 'Top Right', 'Bottom Left', 'Bottom Right')
option_region.config(width=12)
option_region.grid(row=7, column=1, sticky='w')

# Start Button
# TODO: Add command
button_start = Button(master=input_frame, text='Split!', command=save_config)
button_start.grid(row=7, column=5, sticky="e")

window.mainloop()
