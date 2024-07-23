#/usr/bin/env python
"""Tkinter frontend to the GNOME settings command.

The interface consists of three objects: the SCHEMAS list, the KEYS
list, and the currently selected VALUE. Selecting a schema and a key
determines what value is currently selected.
"""
import subprocess

from tkinter import *
from tkinter import messagebox, ttk

GSETTINGS = 'gsettings'
LISTSCHEMAS = 'list-schemas'
LISTKEYS = 'list-keys'

class Schemas(Frame):
	def __init__(self, main, **kwargs):
		super().__init__(main)
		self.treeview = ttk.Treeview(self, selectmode=BROWSE)
		self.scrollbar = Scrollbar(self, command=self.treeview.yview)
		self.treeview['yscrollcommand'] = self.scrollbar.set
		self.schemas = dict()
		self.treeview.pack(side=LEFT)
		self.scrollbar.pack(side=LEFT)
		self.pack(side=TOP, anchor=NW)
		self.populate()
		if 'command' in kwargs:
			self.treeview.bind('<<TreeviewSelect>>', kwargs['command'])

	def populate(self):
		self.schemas.clear()
		output = subprocess.run(
			(
				'gsettings',
				LISTSCHEMAS
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
			self.schemas[parent] = schema

	def retrieve(self, item_id):
		return self.schemas[item_id]

	def selection(self):
		return self.treeview.selection()[0]

	def item(self):
		item_id = self.treeview.selection()[0]
		if item_id in self.schemas:
			return self.schemas[item_id]


class Keys(Frame):
	def __init__(self, main, **kwargs):
		super().__init__(main)
		self.listbox = Listbox(self)
		self.listbox.pack()
		self.pack(side=LEFT, anchor=NW)
		if 'command' in kwargs:
			self.listbox.bind('<<ListboxSelect>>', kwargs['command'])

	def item(self):
		if self.listbox.curselection():
			index = self.listbox.curselection()[0]
			return self.listbox.get(index)

	def populate(self, schema):
		if not isinstance(schema, str):
			return
		self.schema = schema
		output = subprocess.run(
			(
				'gsettings',
				LISTKEYS,
				schema
			),
			capture_output = True
		)
		keys = output.stdout.decode('utf-8').split()
		self.listbox.delete(0, self.listbox.size())
		self.listbox.insert(0, *keys)


class Value(Frame):
	def __init__(self, main):
		super().__init__(main)
		self.description = Label(self, wraplength=250)
		self.range = Label(self)
		self.value = Label(self)
		self.spinval = StringVar(self, 'none')
		self.spinbox = ttk.Entry(self, textvariable=self.spinval)
		self.button1 = ttk.Button(
			self,
			text='Reset',
			command=self.reset
		)
		self.button2 = ttk.Button(
			self,
			text='Set',
			command=self.set
		)
		self.description.pack()
		self.range.pack()
		self.value.pack()
		self.spinbox.pack()
		self.button1.pack()
		self.button2.pack()
		self.pack(side=LEFT)

	def reset(self):
		output = subprocess.run(
			('gsettings', 'reset', self.schema, self.key)
		)
		self.show(self.schema, self.key)

	def set(self):
		value = self.spinval.get()
		output = subprocess.run(
			('gsettings', 'set', self.schema, self.key, value)
		)
		self.show(self.schema, self.key)

	def show(self, schema, key):
		if not schema or not key:
			return
		self.schema = schema
		self.key = key
		describe = subprocess.run(
			('gsettings', 'describe', schema, key),
			capture_output = True
		)
		range = subprocess.run(
			('gsettings', 'range', schema, key),
			capture_output = True
		)
		value = subprocess.run(
			('gsettings', 'get', schema, key),
			capture_output = True
		)
		self.description.configure(text=describe.stdout.decode('utf-8'))
		self.range.configure(text=range.stdout.decode('utf-8'))
		self.value.configure(text=value.stdout.decode('utf-8'))
		self.spinval.set(value.stdout.decode( 'utf-8' ))


class Application(Frame):
	def __init__(self, main):
		Frame.__init__(self, main)
		self.frame1 = ttk.Frame(self)
		self.frame2 = ttk.Frame(self)
		self.schemas = Schemas(self.frame1, command=self.select_schema)
		self.keys = Keys(self.frame1, command=self.select_key)
		self.value = Value(self.frame2)
		self.frame1.pack(side=LEFT)
		self.frame2.pack(side=LEFT)

	def select_schema(self, event):
		self.keys.populate(
			self.schemas.item()
		)

	def select_key(self, event):
		self.value.show(
			self.schemas.item(),
			self.keys.item()
		)

	def quit(self, event=None):
		sys.exit()


root = Tk()
root.geometry('640x480')
root.title("GSettings Frontend")

Application(root).pack()

root.mainloop()
