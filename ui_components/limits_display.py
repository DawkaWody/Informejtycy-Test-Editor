import tkinter as tk
from tkinter import ttk


class TableDisplay(tk.Frame):
	def __init__(self, parent):
		super().__init__(parent)
		self.table = self.create_table()

	def create_table(self):
		headers = ["Time Limit", "Memory Limit"]
		values = ["- sec", "- Mb"]

		table = ttk.Treeview(self, columns=headers, show="headings", height=2)

		for header in headers:
			table.heading(header, text=header)
			table.column(header, anchor="center")

		table.insert("", "end", values=values)
		table.pack(fill="x")

		return table

	def update_limits(self, time_limit, memory_limit):
		"""Updates the values in the table"""
		for item in self.table.get_children():
			self.table.delete(item)
		self.table.insert("", "end", values=[time_limit + " sec", memory_limit + " Mb"])

	def clear_limits(self):
		self.update_limits("-", "-")
