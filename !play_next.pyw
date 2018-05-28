import os
import subprocess
import shelve
import tkinter as tk
from tkinter import ttk
import sys

# Initialise window
window = tk.Tk()
# window.geometry("560x160+0+0")
window.title("IMember")
# window.configure(bg='#ffff00')
current_dir = os.getcwd()
# get a list of all the files - remove this file and the watched.txt file also
full_selection = os.listdir(current_dir)
full_selection.remove('!play_next.pyw')

# Remove shelve module data files and any other non video files
for name in full_selection:
    if name.startswith('watched'):
        full_selection.remove(name)
    if name.endswith('.srt'):
        full_selection.remove(name)
try:
    full_selection.remove('watched.dat')
except:
    pass


# Functions for key bound events
def on_return_key(event):
    play_continuous()

def on_escape_key(event):
    sys.exit()

def add_episode(event):
    t2.set(t2.get()+1)

def subtract_episode(event):
    t2.set(t2.get()-1)


# Functions for button clicks
def update_text_box():
    global full_selection
    d = shelve.open('watched')
    # Check if ep exists, if not assign it to zero
    try:
        watched = d['ep']
    except:
        d['ep'] = 0
        watched = d['ep']
    try:    
        msg = "Next show is: \n" + full_selection[d['ep']] + "\nWhich is episode " + str(d['ep'] + 1)
    except:
        msg = 'Not enough episodes you only have \n' + str(len(full_selection)) + ' episodes downloaded'
    t1.delete('1.0', tk.END)
    t1.insert(tk.END, msg)
    d.close()

def reset_playlist():
    d = shelve.open('watched')
    d['ep'] = 0
    d.close()
    update_text_box()

def skip_back():
    d = shelve.open('watched')
    d['ep'] -=1
    d.close()
    update_text_box()

def skip_fwd():
    d = shelve.open('watched')
    d['ep'] +=1
    d.close()
    update_text_box()


def play_continuous():
    global full_selection
    played = 0
    total = t2.get()
    while played < total :
        d = shelve.open('watched')
        watched = d['ep']
        to_play = full_selection[watched]
        to_play = os.path.join(current_dir, to_play)
        # Add 1 to move to next episode
        d['ep'] += 1
        d.close()
        subprocess.Popen([r'C:\Program Files (x86)\VideoLAN\VLC\vlc.exe', to_play]).wait()
        update_text_box()
        played += 1

# Tkinter window setup
labelText= tk.StringVar()
labelText.set("Up Next:")
labelDir= tk.Label(window, textvariable=labelText)
labelDir.grid(row=0,column=0)

t1 = tk.Text(window, height = 5, width = 40)
t1.grid(row=0, column=1, columnspan=1)
# Only displays for the first 1 second of opening program
t1.insert('1.0', "Coming up next is......")

t2 = tk.Scale(window, from_=1, to=10, orient=tk.HORIZONTAL)
t2.grid(row=1, column=1, sticky=tk.N)

b_continue_play = ttk.Button(window, text="Continue Play", command=play_continuous)
b_continue_play.grid(row=2, column=1)

b_skip_back = ttk.Button(window, text="Skip Back", command=skip_back)
b_skip_back.grid(row=1, column=3, sticky=tk.S)

b_skip_fwd = ttk.Button(window, text="Skip Forward", command=skip_fwd)
b_skip_fwd.grid(row=2, column=3, sticky=tk.S)

b_reset = ttk.Button(window, text="Reset Playlist", command=reset_playlist)
b_reset.grid(row=1, column=0, sticky=tk.S)

# 1 second after loading
window.after(1000, update_text_box)

window.bind('<Return>', on_return_key)
window.bind('<Escape>', on_escape_key)
window.bind('<Right>', add_episode)
window.bind('<Left>', subtract_episode)

window.mainloop()