#! /usr/bin/env python

# GUI Interface for drawing_splitter.py using tkinter
from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog


# TODO: Load settings.toml and use as defaults


# Command functions functions
# Browse for file and update entry box
def browsefunc(entry):
    folder = tkinter.filedialog.askdirectory()
    entry.config(state='normal')
    entry.delete(0, END)
    entry.insert(0, folder)
    entry.config(state='disabled')

# TODO: Add function for running splitter and saving toml

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
entry_dwg_number = Entry(master=input_frame)
entry_dwg_number.grid(row=0, column=1, pady=5, sticky='nsew', columnspan=3)

# Entry box for input folder path, with button
label_input_folder = Label(master=input_frame, text='Input Folder:', font=('Calibri', 10, 'bold'))
label_input_folder.grid(row=1, column=0, sticky='e', pady=5)
entry_input_folder = Entry(master=input_frame, state='disabled', width=50)
entry_input_folder.grid(row=1, column=1, pady=5, columnspan=5, sticky='nsew')
button_input_folder = Button(master=input_frame, text='Browse...', command=lambda: browsefunc(entry_input_folder))
button_input_folder.grid(row=2, column=5, sticky='e')

# Entry box for output folder path, with button
label_output_folder = Label(master=input_frame, text='Output Folder:', font=('Calibri', 10, 'bold'))
label_output_folder.grid(row=3, column=0, sticky='e', pady=5)
entry_output_folder = Entry(master=input_frame, state='disabled', width=50)
entry_output_folder.grid(row=3, column=1, pady=5, columnspan=5, sticky='nsew')
button_output_folder = Button(master=input_frame, text='Browse...', command=lambda: browsefunc(entry_output_folder))
button_output_folder.grid(row=4, column=5, sticky="e")

# Drop down menu for delete files after processing
label_delete = Label(master=input_frame, text='Delete files:', font=('Calibri', 10, 'bold'))
label_delete.grid(row=5, column=0, sticky='e', pady=5)
string_delete = StringVar()
string_delete.set('Yes')
option_delete = OptionMenu(input_frame, string_delete, 'Yes', 'Yes', 'No')
option_delete.grid(row=5, column=1, sticky='w')

# Drop down box for saving by revision
label_revision = Label(master=input_frame, text='Save by revision:', font=('Calibri', 10, 'bold'))
label_revision.grid(row=6, column=0, sticky='e', pady=5)
string_revision = StringVar()
string_revision.set('Yes')
option_revision = OptionMenu(input_frame, string_revision, 'Yes', 'Yes', 'No')
option_revision.grid(row=6, column=1, sticky='w')

# Drop down box for region
label_region = Label(master=input_frame, text='Region:', font=('Calibri', 10, 'bold'))
label_region.grid(row=7, column=0, sticky='e', pady=5)
string_region = StringVar()
string_region.set('Top Right')
option_region = OptionMenu(input_frame, string_region, 'Top Right', 'Top Left', 'Top Right', 'Bottom Left', 'Bottom Right')
option_region.config(width=12)
option_region.grid(row=7, column=1, sticky='w')

# Start Button
# TODO: Add command
button_start = Button(master=input_frame, text='Split!')
button_start.grid(row=7, column=5, sticky="e")

window.mainloop()
