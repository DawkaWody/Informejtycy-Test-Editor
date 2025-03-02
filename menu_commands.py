import webbrowser
import os.path
import requests
from zipfile import ZipFile, ZIP_DEFLATED
from shutil import move, copy
from subprocess import run
from tkinter import messagebox, filedialog, simpledialog

from ui_components.popup_windows import *

def new_pack(app):
	name = simpledialog.askstring("New Test Pack", "Enter the test pack name:")
	if not name:
		return  # If user cancels, do nothing

	pack_name = f"{name}.test"
	with ZipFile(f"tests/{pack_name}", 'w', ZIP_DEFLATED) as new_zip:
		new_zip.writestr("in1", "")
		new_zip.writestr("out1", "")
		new_zip.writestr("CONFIG", "")

	app.file_explorer.load_pack(f"tests/{pack_name}")
	app.table.clear_limits()

def open_pack(app):
	pack_path = filedialog.askopenfilename(title="Select a file", filetypes=(("Test Pack Files", "*.test"),))
	if pack_path:
		app.file_explorer.load_pack(pack_path)
		app.table.clear_limits()
		pack_limits = app.file_explorer.load_config(pack_path)
		app.table.update_limits(pack_limits[0], pack_limits[1])
		app.hide_tests()

def save_pack(app):
	if not hasattr(app.file_explorer, "current_pack"):
		return

	temp_zip = "temp.zip"
	original_zip = app.file_explorer.current_pack

	with ZipFile(original_zip, 'r') as zip_ref:
		with ZipFile(temp_zip, 'w', ZIP_DEFLATED) as temp_zip_ref:
			for item in zip_ref.namelist():
				if not any(item == f"in{test[4:]}" or item == f"out{test[4:]}" for test in app.changes_buffer):
					temp_zip_ref.writestr(item, zip_ref.read(item))

			for test_name, content in app.changes_buffer.items():
				test_number = test_name[4:]
				temp_zip_ref.writestr(f"in{test_number}", content["input"])
				temp_zip_ref.writestr(f"out{test_number}", content["output"])

	move(temp_zip, original_zip)
	app.changes_buffer.clear()

	messagebox.showinfo("Success", "Test Pack has been successfully saved")

def new_test(app):
	if not hasattr(app.file_explorer, "current_pack"):
		return

	with ZipFile(app.file_explorer.current_pack, 'r') as zip_ref:
		test_files = [f for f in zip_ref.namelist() if f != "CONFIG"]
		new_test_number = (len(test_files) // 2) + 1
		new_in_file = f"in{new_test_number}"
		new_out_file = f"out{new_test_number}"

	with ZipFile(app.file_explorer.current_pack, 'a', ZIP_DEFLATED) as zip_ref:
		zip_ref.writestr(new_in_file, "")
		zip_ref.writestr(new_out_file, "")

	app.file_explorer.load_pack(app.file_explorer.current_pack)

def delete_test(app):
	"""Deletes the selected test (both inX and outX) from the ZIP archive and renames higher-numbered tests."""
	selected_item = app.file_explorer.tree.selection()

	if not selected_item:
		messagebox.showwarning("Warning", "No test selected.")
		return

	test_name = app.file_explorer.tree.item(selected_item, "text")
	if not test_name.startswith("test"):
		messagebox.showwarning("Warning", "No test selected.")
		return

	test_number = int(test_name[4:])  # Extract number X from testX
	in_file = f"in{test_number}"
	out_file = f"out{test_number}"

	# Check if there's an open ZIP file
	if not hasattr(app.file_explorer, "current_pack"):
		messagebox.showerror("Error", "No open ZIP file.")
		return

	original_zip = app.file_explorer.current_pack
	temp_zip = "temp.zip"

	with ZipFile(original_zip, 'r') as zip_ref:
		test_files = sorted(
			[f for f in zip_ref.namelist() if f.startswith("in") or f.startswith("out") and f != "CONFIG"]
		)

		with ZipFile(temp_zip, 'w', ZIP_DEFLATED) as temp_zip_ref:
			for item in zip_ref.namelist():
				if item in [in_file, out_file]:
					continue  # Skip the test being deleted

				temp_zip_ref.writestr(item, zip_ref.read(item))

			# Rename higher-numbered tests down by 1
			for i in range(test_number + 1, (len(test_files) // 2) + 1):
				old_in = f"in{i}"
				old_out = f"out{i}"
				new_in = f"in{i-1}"
				new_out = f"out{i-1}"

				if old_in in zip_ref.namelist():
					temp_zip_ref.writestr(new_in, zip_ref.read(old_in))
				if old_out in zip_ref.namelist():
					temp_zip_ref.writestr(new_out, zip_ref.read(old_out))

	move(temp_zip, original_zip)

	# Delete the top test
	with ZipFile(original_zip, 'r') as zip_ref:
		with ZipFile(temp_zip, 'w') as temp_zip_ref:
			max_in = f"in{len(test_files) // 2}"
			max_out = f"out{len(test_files) // 2}"
			for item in zip_ref.namelist():
				if item not in [max_in, max_out]:
					temp_zip_ref.writestr(item, zip_ref.read(item))
	move(temp_zip, original_zip)

	# Update the file explorer
	app.file_explorer.load_pack(original_zip)

	messagebox.showinfo("Success", f"Deleted {test_name}.")

	# Clear display if deleted test was currently opened
	if app.current_test == test_name:
		app.main_display.destroy()
		app.main_display = tk.Frame(app.right_frame, bg="white", bd=2, relief="solid")
		app.main_display.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
		app.current_test = None


def set_limits(app):
	popup = InputPopup(app, "New pack limits")
	if popup.result != () and popup.result != ("", ""):
		pack_path = app.file_explorer.current_pack
		with ZipFile(pack_path, 'r') as pack, ZipFile("temp.zip", 'w', ZIP_DEFLATED) as new_pack:
			for item in pack.infolist():
				if item.filename != "CONFIG":
					new_pack.writestr(item.filename, pack.read(item.filename))
			new_pack.writestr("CONFIG", f"{popup.result[0]} {popup.result[1]}")
		move("temp.zip", pack_path)
		app.table.update_limits(popup.result[0], popup.result[1])

def validate_pack(app):
	if not os.path.exists('pack_loader.py'):
		# Clone the file from checker repo
		cloning_popup = LoadingPopup(app, "Cloning pack loader from GitHub")
		print("clonign")
		with open("pack_loader.py", 'w') as file:
			c = requests.get('https://raw.githubusercontent.com/DawkaWody/Informejtycy-Checker/refs/heads/main/src/code_checking/pack_loader.py').content
			file.write(c.decode('utf-8'))
		with open("pack_loader.py", 'r') as file:
			lines = file.readlines()
		with open("pack_loader.py", 'w') as file:
			for line in lines:
				if line.strip("\n") == "	def __init__(self, logger: Logger, pack_dir: str, pack_extension: str, in_name: str, out_name: str, config_name: str):":
					file.write("	def __init__(self, logger, pack_dir: str, pack_extension: str, in_name: str, out_name: str, config_name: str):\n")
				elif line.strip("\n") != "from logger import Logger":
					file.write(line)
		print("end")
		cloning_popup.destroy()

	pack_loader = __import__('pack_loader', globals(), locals(), ['PackLoader'])
	copy(app.file_explorer.current_pack, 'validation')
	pl = pack_loader.PackLoader(None, 'validation', '.test', 'in', 'out', 'CONFIG')

	try:
		tests = pl.load_bytes(0)
		config = pl.load_config(0)
	except Exception as e:
		os.remove(f"validation/{os.path.basename(app.file_explorer.current_pack)}")
		with open('validation.log', 'w') as log:
			log.writelines([f"====PACK: {app.file_explorer.current_pack}====\n", repr(e) + "\n"])
		messagebox.showerror("Pack validation", "Error: " + str(e))
		return

	os.remove(f"validation/{os.path.basename(app.file_explorer.current_pack)}")
	messagebox.showinfo("Pack validation", "Pack is valid and ready to use")
	with open('validation.log', 'a') as log:
		log.writelines([f"====PACK: {app.file_explorer.current_pack}====\n", str(config) + "\n", str(tests) + "\n"])

def open_test_dir(app):
	run(f"explorer {os.path.abspath("tests")}")

def remove_pack_loader(app):
	os.remove("pack_loader.py")
	messagebox.showinfo("Pack loader removed", "New validator will be cloned before the next validation")

def open_log(app):
	run("notepad validation.log")

def version(app):
	messagebox.showinfo("About", "Informejtycy Test Editor v1.0")

def open_github(app):
	webbrowser.open('https://github.com/DawkaWody/Informejtycy-Test-Editor')

def report_bug(app):
	messagebox.showinfo("Bug report", "To report a bug please contact me on discord")


COMMANDS = {"new": new_pack, "open": open_pack, "save": save_pack, "new_test": new_test, "delete_test": delete_test,
			"limits": set_limits, "validate": validate_pack, "open_dir": open_test_dir, "remove_pack_loader": remove_pack_loader,
			"open_log": open_log, "version": version, "github": open_github, "bugreport": report_bug}