#! /usr/bin/env python

# GUI Interface for drawing_splitter.py using tkinter
import os
import threading
import time

from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog
import toml


import drawing_splitter
import user_options


# Load settings.toml and use as defaults
settings = user_options.load_settings_toml()

REGIONS = {'Top Left': 'top-left', 'Top Right': 'top-right', 'Bottom Left': 'bot-right', 'Bottom Right': 'bot-right'}
# Command functions functions
# Browse for file and update entry box
def browsefunc(entry):
    folder = tkinter.filedialog.askdirectory()
    entry.config(state='normal')
    entry.delete(0, END)
    entry.insert(0, folder)
    entry.config(state='disabled')

# Save settings to settings.toml
def save_config():
    regions = {'Top Left': 'top-left', 'Top Right': 'top-right', 'Bottom Left': 'bot-right', 'Bottom Right': 'bot-right'}
    settings = {}
    settings['dwg_number_element'] = string_dwg_number.get()
    settings['input_folder'] = string_input_folder.get()
    settings['output_folder'] = string_output_folder.get()
    settings['delete'] = bool(int(string_delete.get()))
    settings['revision'] = bool(int(string_revision.get()))
    settings['region'] = REGIONS[string_region.get()]
    with open('settings.toml', 'w') as settings_file:
        settings_file.write(toml.dumps(settings))

# TODO: Split drawings (Need to refactor drawing_splitter.py DRY)
def split_drawings():
    button_start.config(state='disabled')
    #print('Drawing Splitter\n')
    number_element = string_dwg_number.get()
    pdf_files = drawing_splitter.get_filenames(string_input_folder.get())
    #print(f'Total files to process: {len(pdf_files)}')
    #print(f'Using drawing number element: {number_element}')
    #print(f'Checking region: {string_region.get()}\n')
    for filename in pdf_files:
        progress_bar['value'] = 0
        page_size = drawing_splitter.get_page_size(filename)
        page_height = page_size[0]
        page_width = page_size[1]
        regions = {'top-left': (0, 0, page_width * 0.2, page_height * 0.5),
                   'top-right': (page_width * 0.8, 0,
                                 page_width, page_height * 0.5),
                   'bot-left': (0, page_height * 0.5, page_width * 0.2,
                                page_height),
                   'bot-right': (page_width * 0.8, page_height * 0.5,
                                 page_width, page_height),
                   'all': (0, 0, page_width, page_height)}
        string_status.set(f'Processing file: {os.path.basename(filename)}...')
        num_of_pages = drawing_splitter.get_pdf_length(filename)
        region = string_region.get()
        revision = bool(int(string_revision.get()))
        drawing_numbers = drawing_splitter.get_dwg_info(filename, num_of_pages, number_element,
                                       regions[REGIONS[region]], revision, progress_bar)
        drawing_splitter.save_drawings(filename, num_of_pages, drawing_numbers, string_output_folder.get(),
                      revision)
        if bool(int(string_delete.get())):
            drawing_splitter.delete_file(filename)
        print()
    string_status.set(f'Finished processing {len(pdf_files)} files.')
    button_start.config(state='normal')

def save_and_split():
    save_config()
    threading.Thread(target=split_drawings).start()

# Create window
window = Tk()
window.geometry('500x220')
window.resizable(False, False)
window.title("Drawing Splitter")

# Add program title
# label_program_header = Label(master=window, text='Drawing Splitter', font=('Calibri', 16, 'bold'))
# label_program_header.grid(row=0, column=0, columnspan=5, sticky='w', padx=5, pady=5)

# Create frame for inputs
input_frame = Frame(master=window, borderwidth=1)
input_frame.grid(row=1, column=0, padx=5, pady=5)

# Create items for input_frame
# Entry box for dwg_number_element
label_dwg_number = Label(master=input_frame, text='Number Element:', font=('Calibri', 10, 'bold'))
label_dwg_number.grid(row=0, column=0, pady=5)
string_dwg_number = StringVar()
entry_dwg_number = Entry(master=input_frame, textvariable=string_dwg_number)
entry_dwg_number.grid(row=0, column=1, pady=5, sticky='nsew', columnspan=2)
string_dwg_number.set(settings['dwg_number_element'])

# Entry box for input folder path, with button
label_input_folder = Label(master=input_frame, text='Input Folder:', font=('Calibri', 10, 'bold'))
label_input_folder.grid(row=1, column=0, sticky='e', pady=5)
string_input_folder = StringVar()
entry_input_folder = Entry(master=input_frame, state='disabled', width=50, textvariable=string_input_folder)
entry_input_folder.grid(row=1, column=1, pady=5, columnspan=4, sticky='nsew')
button_input_folder = Button(master=input_frame, text='Browse...', command=lambda: browsefunc(entry_input_folder))
button_input_folder.grid(row=1, column=5, sticky='e')
string_input_folder.set(settings['input_folder'])

# Entry box for output folder path, with button
label_output_folder = Label(master=input_frame, text='Output Folder:', font=('Calibri', 10, 'bold'))
label_output_folder.grid(row=3, column=0, sticky='e', pady=5)
string_output_folder = StringVar()
entry_output_folder = Entry(master=input_frame, state='disabled', width=50, textvariable=string_output_folder)
entry_output_folder.grid(row=3, column=1, pady=5, columnspan=4, sticky='nsew')
button_output_folder = Button(master=input_frame, text='Browse...', command=lambda: browsefunc(entry_output_folder))
button_output_folder.grid(row=3, column=5, sticky="e")
string_output_folder.set(settings['output_folder'])

# Drop down menu for delete files after processing
label_delete = Label(master=input_frame, text='Delete files:', font=('Calibri', 10, 'bold'))
label_delete.grid(row=5, column=0, sticky='e', pady=5)
string_delete = StringVar()
if settings['delete']:
    string_delete.set(True)
else:
    string_delete.set(False)
option_delete = Checkbutton(input_frame, variable=string_delete, onvalue=True, offvalue=False)
option_delete.grid(row=5, column=1, sticky='w', padx=5)

# Drop down box for saving by revision
label_revision = Label(master=input_frame, text='Save by revision:', font=('Calibri', 10, 'bold'))
label_revision.grid(row=5, column=2, sticky='e', pady=5)
string_revision = StringVar()
if settings['revision']:
    string_revision.set(True)
else:
    string_revision.set(False)
option_revision = Checkbutton(input_frame, variable=string_revision, onvalue=True, offvalue=False)
option_revision.grid(row=5, column=3, sticky='w', padx=5)

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
button_start = Button(master=input_frame, text='Split!', command=save_and_split)
button_start.grid(row=7, column=5, sticky="e")


# Add progress bar
progress_bar = Progressbar(master=input_frame, orient='horizontal', length=490, mode='determinate')
progress_bar.grid(row=8, column=0, columnspan=6, pady=5)

# Status label
label_status = Label(master=input_frame, text='Status:', font=('Calibri', 10, 'bold'))
label_status.grid(row=9, column=0, sticky='e', pady=5)
string_status = StringVar()
string_status.set('Not Running')
label_actual_status = Label(master=input_frame, textvariable=string_status)
label_actual_status.grid(row=9, column=1, columnspan=5, sticky='w')

window.mainloop()
