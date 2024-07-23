#/usr/bin/env python
import subprocess

from tkinter import *
from tkinter import messagebox, ttk

GSETTINGS = 'gsettings'

class Schemas(Frame):
	def __init__(self, main):
		super().__init__(main)
		self.treeview = ttk.Treeview(self, selectmode=BROWSE)
		self.scrollbar = Scrollbar(self, command=self.treeview.yview)
		self.treeview['yscrollcommand'] = self.scrollbar.set
		self.schemas = dict()
		self.treeview.pack(side=LEFT)
		self.scrollbar.pack(side=LEFT)
		self.pack(side=TOP, anchor=NW)
		self.populate()

	def bind(self, event, command):
		self.treeview.bind(event, command)

	def populate(self):
		self.schemas.clear()
		output = subprocess.run(
			(
				GSETTINGS,
				'list-schemas'
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


class Keys(Listbox):
	def __init__(self, main):
		super().__init__(main)
		self.pack(side=TOP, anchor=NW)

	def populate(self, schema):
		self.schema = schema
		output = subprocess.run(
			(
				GSETTINGS,
				'list-keys',
				schema
			),
			capture_output = True
		)
		keys = output.stdout.decode('utf-8').split()
		self.delete(0, self.size())
		self.insert(0, *keys)


class Info(Frame):
	def __init__(self, main):
		super().__init__(main)
		self.description = Label(self, wraplength=250)
		self.description.pack()
		self.range = Label(self)
		self.range.pack()
		self.value = Label(self)
		self.value.pack()
		self.pack()

	def show(self, schema, key):
		describe = subprocess.run(
			(GSETTINGS, 'describe', schema, key),
			capture_output = True
		)
		range = subprocess.run(
			(GSETTINGS, 'range', schema, key),
			capture_output = True
		)
		value = subprocess.run(
			(GSETTINGS, 'get', schema, key),
			capture_output = True
		)
		self.description.configure(text=describe.stdout.decode('utf-8'))
		self.range.configure(text=range.stdout.decode('utf-8'))
		self.value.configure(text=value.stdout.decode('utf-8'))


class Value(Frame):
	"""Show and set the value of a key."""
	def __init__(self, main):
		super().__init__(main)
		self.spinval = StringVar(self, 'none')
		self.spinbox = ttk.Entry(self, textvariable=self.spinval)
		self.spinbox.pack()
		self.pack()

	def range_get(self, schema, key):
		self.schema = schema
		self.key = key
		range = subprocess.run(
			(GSETTINGS, 'range', schema, key),
			capture_output = True
		)
		get = subprocess.run(
			(GSETTINGS, 'get', schema, key),
			capture_output = True
		)
		range = range.stdout.decode('utf-8')
		self.spinval.set(get.stdout.decode( 'utf-8' ))
		if range[:7] == 'range i':
			pass
		elif range[:6] == 'type i':
			pass
		elif range[:6] == 'type b':
			pass

	def set(self):
		value = self.spinval.get()
		output = subprocess.run(
			(GSETTINGS, 'set', self.schema, self.key, value)
		)


class Application(Frame):
	def __init__(self, main):
		Frame.__init__(self, main)
		self.frame1 = ttk.Frame(self)
		self.frame1.pack(side=LEFT)
		self.frame2 = ttk.Frame(self)
		self.frame2.pack(side=LEFT)
		self.treeview = Schemas(self.frame1)
		self.listbox = Keys(self.frame1)
		self.treeview.bind('<<TreeviewSelect>>', self.list_keys)
		self.listbox.bind('<<ListboxSelect>>', self.information)
		self.description = Info(self.frame2)
		self.setting = Value(self.frame2)
		self.button = ttk.Button(
			self.frame2,
			text='Set',
			command=self.setting.set
		)
		self.button.pack()
		self.process = GSETTINGS
		self.command = 'help'
		self.schema = ''
		self.key = ''
		self.value = ''

	def set_value(self):
		self.setting.set()
		self.description.show()

	def reset_value(self):
		self.setting.reset()
		self.description.show()

	def list_keys(self, event):
		item_id = self.treeview.selection()
		if item_id not in self.treeview.schemas:
			return
		self.listbox.populate(self.treeview.retrieve( item_id ))

	def get_range(self):
		self.command = 'range'
		output = subprocess.run(
			(
			GSETTINGS,
			'range',
			self.schema,
			self.key
			),
			capture_output = True
		)
		range = output.stdout.decode('utf-8')
		if range[:7] == 'range i':
			low = range.split()[2]
			high = range.split()[3]
			self.range_i.configure(from_=low, to=high)
			self.get_value(int)

	def information(self, event):
		if not self.listbox.curselection():
			return
		item = self.listbox.curselection()[0]
		key = self.listbox.get(item)
		self.description.show(self.listbox.schema, key)
		self.setting.range_get(self.listbox.schema, key)

	def get_value(self, cast):
		self.command = 'get'
		output = subprocess.run(
			(
			self.process,
			self.command,
			self.schema,
			self.key
			),
			capture_output = True
		)
		value = output.stdout.decode('utf-8')
		self.spinval = cast( value )

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
root.title("GNOME Settings Frontend")

Application(root).pack()

root.mainloop()
