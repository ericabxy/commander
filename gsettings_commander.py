import subprocess

from tkinter import *
from tkinter import ttk

command0 = 'gsettings'

cmd_help = 'help'
cmd_list_schemas = 'list-schemas'
cmd_list_keys = 'list-keys'
cmd_range = 'range'
cmd_describe = 'describe'
cmd_get = 'get'
cmd_set = 'set'
cmd_reset = 'reset'

arg_none = ''
arg_trackball = 'org.gnome.desktop.peripherals.trackball'
arg_keyboard = 'org.gnome.desktop.peripherals.keyboard'

def add_command():
	command0button.configure(
		text = ' '.join((command0, gsettings_command.get( )))
	)

def runcommand():
	subprocess.run(
		(
		command0,
		gsettings_command.get()
		)
	)

root = Tk()
root.geometry('640x480')
root.title("Hello World")

gsettings_command = StringVar(root, cmd_help)
gsettings_argument0 = StringVar(root, arg_none)

command0button = ttk.Button(root, text=command0, command=runcommand)
command0button.grid()
command0button.configure(text=command0)

radio_help = ttk.Radiobutton(
	root,
	text=cmd_help,
	command=add_command,
	variable=gsettings_command,
	value=cmd_help
)
radio_help.grid()

radio_list_schemas = ttk.Radiobutton(
	root,
	text=cmd_list_schemas,
	command=add_command,
	variable=gsettings_command,
	value=cmd_list_schemas
)
radio_list_schemas.grid()

radio_list_keys = ttk.Radiobutton(
	root,
	text=cmd_list_keys,
	command=add_command,
	variable=gsettings_command,
	value=cmd_list_keys
)
radio_list_keys.grid()

radio_get = ttk.Radiobutton(
	root,
	text=cmd_get,
	command=add_command,
	variable=gsettings_command,
	value=cmd_get
)
radio_get.grid()

root.mainloop()
