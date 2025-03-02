# Informejtycy test editor

GUI tool for editing test packs for informejtycy.pl website.

## Installation
Download the installer [here](https://github.com/DawkaWody/Informejtycy-Test-Editor/releases/tag/release)
and run it.

## Usage
After opening the user is greeted with a demo pack which can be edited to get to know 
the program. Select a test from the file viewer and edit the input/output text
fields. Don't forget to save (Ctrl+S) as there is no auto saving.

## Options
Every option is accessible via the menu on the top or with shortcuts. Here's a
list of all available options and what they do:

**File**:
- New pack (Ctrl+Shift+N) - creates a new pack with the given name 
in the default directory. The new pack contains an empty CONFIG and one empty
test (in1 and out1 files)
- Open existing (Ctrl+O) - opens the selected pack. May not work correctly if
the pack is done wrong
- Save (Ctrl+S) - save the changes to the pack file
- Exit - quit the program

**Pack**:
- New test (Ctrl+N) - Adds a new empty test (pair of inX and outX) to the pack
- Delete selected test (Del) - Deletes the in+out pair that user has currently
selected.
- Configure limits (Ctrl+L) - Show a popup window where the user can edit the
config file (time and memory limit) for the pack
- Validate (Ctrl+Shift+V) - Clones the pack loader from the checker repo (if not present)
and uses it to check the currently opened pack for errors. Displays an info window
when everything is okay and an error window when the pack loader raised errors

**Options**:
- Open test directory - opens the default directory where the test packs are stored
in a file explorer
- Force validator re-clone - Removes the currently present pack loader file. Handy
if a new release is available on GitHub
- Open log - Opens the validate.log file in notepad. The log contains pack
properties/error info from the validation procedures

**About**:
- Version - Displays program version
- GitHub - opens the GitHub repository in the browser
- Bug Report - displays a message "To report a bug please contact me on discord.
May change in the future"


## Screenshots
![Screenshot 1](readme_screenshots/Screenshot%202025-03-02%20185417.png)
![Screenshot 2](readme_screenshots/Screenshot%202025-03-02%20182936.png)
![Screenshot 3](readme_screenshots/Screenshot%202025-03-02%20185456.png)
![Screenshot 4](readme_screenshots/Screenshot%202025-03-02%20185513.png)
![Screenshot 5](readme_screenshots/Screenshot%202025-03-02%20185529.png)