import subprocess

from tkinter import *
from tkinter import messagebox, ttk

class Application(Frame):
	def __init__(self, main):
		Frame.__init__(self, main)
		self.treeview = ttk.Treeview(selectmode=BROWSE)
		self.treeview.bind('<<TreeviewSelect>>', self.list_keys)
		self.treeview.pack()
		self.listbox = Listbox()
		self.listbox.bind('<<ListboxSelect>>', self.describe_key)
		self.listbox.pack()
		self.description = Label(self, text="no key selected")
		self.description.pack()
		self.range = Label(self, text="no key selected")
		self.range.pack()
		self.process = 'gsettings'
		self.command = 'help'
		self.schema = ''
		self.key = ''
		self.value = ''
		self.list_schemas()

	def list_schemas(self):
		self.schema_names = {}
		self.command = 'list-schemas'
		output = subprocess.run(
			(
				self.process,
				self.command
			),
			capture_output = True
		)
		for schema in output.stdout.decode('utf-8').split():
			parent = ''
			for word in schema.split('.'):
				for child in self.treeview.get_children(parent):
					text = self.treeview.item(child, option='text')
					if text == word:
						parent = child
						break
				else:
					parent = self.treeview.insert(parent, END, text=word)
			self.schema_names[parent] = schema

	def list_keys(self, event):
		item_id = self.treeview.selection()[0]
		if item_id not in self.schema_names:
			return
		self.schema = self.schema_names[item_id]
		self.command = 'list-keys'
		output = subprocess.run(
			(
			self.process,
			self.command,
			self.schema
			),
			capture_output = True
		)
		keys = output.stdout.decode('utf-8').split()
		self.listbox.delete(0, self.listbox.size())
		self.listbox.insert(0, *keys)

	def get_range(self):
		self.command = 'range'
		output = subprocess.run(
			(
			self.process,
			self.command,
			self.schema,
			self.key
			),
			capture_output = True
		)
		range = output.stdout.decode('utf-8')
		self.range.configure(text=range)

	def describe_key(self, event):
		self.command = 'describe'
		item = self.listbox.curselection()[0]
		self.key = self.listbox.get(item)
		output = subprocess.run(
			(
			self.process,
			self.command,
			self.schema,
			self.key
			),
			capture_output = True
		)
		description = output.stdout.decode('utf-8')
		self.description.configure(text=description)
		self.get_range()

	def get_value(self):
		self.command = 'get'
		subprocess.run(
			(
			self.process,
			self.command,
			self.schema,
			self.key
			)
		)

	def set_value(self):
		self.command = 'set'
		subprocess.run(
			(
			self.process,
			self.command,
			self.schema,
			self.key
			)
		)

	def quit(self, event=None):
		sys.exit()

root = Tk()
root.geometry('640x480')
root.title("Hello World")

Application(root).pack()

root.mainloop()
