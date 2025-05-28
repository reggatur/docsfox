'''
Disclaimer:  This code resulted from an experiment in February, 2025, to see if 
ChatGPT and CoPilot could completely write a working application without human 
code modification. After 40+ human prompt modifications, surprisingly, the 
experiment succeeded. The Python code is far from pretty, but it works.

This comment is literally the only part of this application that was human-
written.

If you believe the code should be improved, by all means, fork it!

MIT License

Copyright (c) 2025 Wells H. Anderson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import os
import csv
import uno
import unohelper
import urllib.parse
from com.sun.star.awt import XActionListener

DATA_FILE = os.path.expanduser("~\\datafilename.txt")

def uno_url_to_path(uno_url):
    """Converts a LibreOffice file URL to a standard Windows path."""
    if uno_url.startswith("file:///"):
        return urllib.parse.unquote(uno_url[8:]).replace("/", "\\")
    return uno_url  # Return as is if it's already a normal path

def get_csv_filename():
    """Prompts user for CSV file selection and stores last used file."""
    last_used_file = None
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            last_used_file = f.read().strip()

    ctx = XSCRIPTCONTEXT.getComponentContext()
    smgr = ctx.getServiceManager()
    file_picker = smgr.createInstanceWithContext("com.sun.star.ui.dialogs.FilePicker", ctx)

    file_picker.setTitle("Select CSV File")
    file_picker.appendFilter("CSV Files (*.csv)", "*.csv")

    if last_used_file and os.path.exists(last_used_file):
        file_picker.setDisplayDirectory(os.path.dirname(last_used_file))

    if file_picker.execute():
        selected_files = file_picker.getFiles()
        if selected_files and selected_files[0]:
            csv_filename = uno_url_to_path(selected_files[0])
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                f.write(csv_filename)  # Save last used file
            return csv_filename

    return last_used_file  # Use last known file if the user cancels

def read_replacement_data(csv_filename):
    """Reads a CSV file and creates a dictionary of placeholder replacements."""
    replacements = {}
    remove_f_flags = set()
    remove_tf_flags = set()
    simple_replacements = {}
    variable_replacements = {}

    if not csv_filename or not os.path.exists(csv_filename):
        return replacements, remove_f_flags, remove_tf_flags, simple_replacements, variable_replacements

    try:
        with open(csv_filename, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header row
            for row in reader:
                if len(row) >= 4:
                    key = row[0].strip()
                    value = row[1].strip()
                    flag_c = row[2].strip().upper()
                    flag_d = row[3].strip().upper()
                    
                    if flag_d == "F":
                        remove_f_flags.add(key)
                    if flag_c == "TF" and (flag_d == "T" or flag_d == "F"):
                        remove_tf_flags.add(key)
                    
                    if flag_d != "F" and flag_c != "TF":
                        simple_replacements[f"<<{key}>>"] = value
                        simple_replacements[f"<<{key}/>>"] = value
                    
                    if flag_c == "R":
                        variable_replacements[f"{key}"] = value

    except Exception as e:
        pass

    return replacements, remove_f_flags, remove_tf_flags, simple_replacements, variable_replacements

def replace_placeholders():
    """Finds and replaces placeholders in the current Writer document."""

    csv_filename = get_csv_filename()
    if not csv_filename:
        return

    replacements, remove_f_flags, remove_tf_flags, simple_replacements, variable_replacements = read_replacement_data(csv_filename)
    if not replacements and not remove_f_flags and not remove_tf_flags and not simple_replacements and not variable_replacements:
        return

    # Check if the document is open
    try:
        doc = XSCRIPTCONTEXT.getDesktop().getCurrentComponent()
        if not doc:
            return
        if not doc.supportsService("com.sun.star.text.TextDocument"):
            return
    except Exception as e:
        return

    try:
        search = doc.createSearchDescriptor()
        if not search:
            return
    except Exception as e:
        return

    # First process simple search and replace for rows that do not have "TF" in column C
    for key, value in simple_replacements.items():
        search.setSearchString(key)
        found = doc.findFirst(search)

        while found:
            found.setString(value)
            found = doc.findNext(found, search)
            
    # Process variable replacement search and replace for rows that have "R" in column C
    for key, value in variable_replacements.items():
        search.setSearchString(key)
        found = doc.findFirst(search)

        while found:
            found.setString(value)
            found = doc.findNext(found, search)

    # Replace placeholders using columns A and B for all other rows
    for key, value in replacements.items():
        search.setSearchString(f"<<{key}>>")
        found = doc.findFirst(search)

        while found:
            found.setString(value)
            found = doc.findNext(found, search)

        search.setSearchString(f"<<{key}/>>")
        found = doc.findFirst(search)

        while found:
            found.setString(value)
            found = doc.findNext(found, search)

    # Remove text and delimiters for rows with "F" in column D
    for key in remove_f_flags:
        placeholder_start = f"<<{key}>>"
        placeholder_end = f"<<{key}/>>"

        while True:
            search.setSearchString(placeholder_start)
            found_start = doc.findFirst(search)
            
            if not found_start:
                break
            
            search.setSearchString(placeholder_end)
            found_end = doc.findNext(found_start, search)
            
            if found_end:
                cursor = doc.Text.createTextCursorByRange(found_start.getStart())
                cursor.gotoRange(found_end.getEnd(), True)
                cursor.setString("")
            else:
                break

    # Delete all delimiter pairs that have "TF" in column C and either "T" or "F" in column D
    for key in remove_tf_flags:
        search.setSearchString(f"<<{key}>>")
        found = doc.findFirst(search)

        while found:
            found.setString("")
            found = doc.findNext(found, search)

        search.setSearchString(f"<<{key}/>>")
        found = doc.findFirst(search)

        while found:
            found.setString("")
            found = doc.findNext(found, search)

def replace_text_in_writer(event=None):
    """Main function called by LibreOffice. Only proceeds if OK is pressed."""

    # Show confirmation dialog
    ctx = XSCRIPTCONTEXT.getComponentContext()
    smgr = ctx.getServiceManager()
    toolkit = smgr.createInstanceWithContext("com.sun.star.awt.Toolkit", ctx)

    dialogModel = smgr.createInstanceWithContext("com.sun.star.awt.UnoControlDialogModel", ctx)
    dialogModel.Width = 100
    dialogModel.Height = 50
    dialogModel.Title = "Make changes with Docsfox?"

    okButtonModel = dialogModel.createInstance("com.sun.star.awt.UnoControlButtonModel")
    okButtonModel.Name = "okButton"
    okButtonModel.Label = "OK"
    okButtonModel.PositionX = 35
    okButtonModel.PositionY = 20
    okButtonModel.Width = 30
    okButtonModel.Height = 14
    dialogModel.insertByName("okButton", okButtonModel)

    dialog = smgr.createInstanceWithContext("com.sun.star.awt.UnoControlDialog", ctx)
    dialog.setModel(dialogModel)
    dialog.setVisible(False)

    class Listener(unohelper.Base, XActionListener):
        def __init__(self, dialog):
            self.dialog = dialog
            self.result = None

        def actionPerformed(self, actionEvent):
            self.result = True
            self.dialog.endDialog(1)

    listener = Listener(dialog)
    okButton = dialog.getControl("okButton")
    okButton.addActionListener(listener)

    dialog.createPeer(toolkit, None)
    dialog.execute()
    dialog.dispose()

    if not listener.result:
        return

    replace_placeholders()


# Register the function
g_exportedScripts = (replace_text_in_writer,)
