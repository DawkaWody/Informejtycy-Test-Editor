from cx_Freeze import setup, Executable

include_files = [
	("icon.ico", "icon.ico"),
	# Directories
	("ui_components", "ui_components"),
	("tests", "tests"),
	("validation", "validation"),
	# Additional scripts
	("exceptions.py", "exceptions.py"),
	("menu_commands.py", "menu_commands.py"),

	("validation.log", "validation.log")
]

base = "Win32GUI"

setup(
	name="Informejtycy-Test-Editor",
	version="1.1",
	description="Test pack editor for informejtycy.pl",
	executables=[Executable("app.py", base=base, icon="icon.ico")],
	options={
		"build_exe": {
			"packages": ["requests"],
			"include_files": include_files
		}
	}
)