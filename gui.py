#! /usr/bin/env python

# GUI Interface for drawing_splitter.py using tkinter
import tkinter as tk
import tkinter.filedialog


# Helper functions
def browsefunc(entry):
    folder = tk.filedialog.askdirectory()
    entry.config(state='normal')
    entry.delete(0, tk.END)
    entry.insert(0, folder)
    entry.config(state='disabled')

# Create window
window = tk.Tk()
window.geometry('640x480')
window.resizable(False, False)

#Create frame for inputs
input_frame = tk.Frame(master=window, borderwidth=1)
input_frame.grid(row=0, column=0, padx=5, pady=5)

#Create items for input_frame
label_dwg_number = tk.Label(master=input_frame, text='Number Element:')
label_dwg_number.grid(row=0, column=0, pady=5)
entry_dwg_number = tk.Entry(master=input_frame)
entry_dwg_number.grid(row=0, column=1, pady=5, sticky='w')

label_input_folder = tk.Label(master=input_frame, text='Input Folder:')
label_input_folder.grid(row=1, column=0, sticky='e', pady=5)
entry_input_folder = tk.Entry(master=input_frame, state='disabled', width=50)
entry_input_folder.grid(row=1, column=1, pady=5)
button_input_folder = tk.Button(master=input_frame, text='Browse...', command=lambda: browsefunc(entry_input_folder))
button_input_folder.grid(row=2, column=1, sticky='e')

label_output_folder = tk.Label(master=input_frame, text='Output Folder:')
label_output_folder.grid(row=3, column=0, sticky='e', pady=5)
entry_output_folder = tk.Entry(master=input_frame, state='disabled', width=50)
entry_output_folder.grid(row=3, column=1, pady=5)
button_output_folder = tk.Button(master=input_frame, text='Browse...', command=lambda: browsefunc(entry_output_folder))
button_output_folder.grid(row=4, column=1, sticky="e")

label_delete = tk.Label(master=input_frame, text='Delete files:')
label_delete.grid(row=5, column=0, sticky='e', pady=5)
string_delete = tk.StringVar()
string_delete.set('Yes')
option_delete = tk.OptionMenu(input_frame, string_delete, 'Yes', 'No')
option_delete.grid(row=5, column=1, sticky='w')

label_revision = tk.Label(master=input_frame, text='Save by rev:')
label_revision.grid(row=6, column=0, sticky='e', pady=5)
string_revision = tk.StringVar()
string_revision.set('Yes')
option_delete = tk.OptionMenu(input_frame, string_revision, 'Yes', 'No')
option_delete.grid(row=6, column=1, sticky='w')

label_region = tk.Label(master=input_frame, text='Region:')
label_region.grid(row=7, column=0, sticky='e', pady=5)
string_region = tk.StringVar()
string_region.set('Top Left')
option_region = tk.OptionMenu(input_frame, string_region, 'Top Left', 'Top Right', 'Bottom Left', 'Bottom Right')
option_region.grid(row=7, column=1, sticky='w')

window.mainloop()
