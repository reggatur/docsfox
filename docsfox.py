from Npp import *
import os
import csv
import re  # Import regex module

DATA_FILE_STORAGE = os.path.join(os.path.dirname(__file__), "DataFileName.txt")

def save_last_used_file(csv_path):
    """ Save the last used CSV file path to a local file. """
    try:
        with open(DATA_FILE_STORAGE, "w") as f:
            f.write(csv_path)
    except Exception as e:
        notepad.messageBox("Error saving Data File path:\n{}".format(e), "Error")

def get_last_used_file():
    """ Retrieve the last used CSV file path if it exists. """
    if os.path.isfile(DATA_FILE_STORAGE):
        try:
            with open(DATA_FILE_STORAGE, "r") as f:
                return f.read().strip()
        except Exception as e:
            notepad.messageBox("Error reading saved Data File path:\n{}".format(e), "Error")
    return None

def prompt_for_csv_file():
    """ Ask the user to enter a new CSV file path. """
    return notepad.prompt("Enter the Data File path and name:", "Data File Path:", "")

def read_replacement_pairs(csv_path):
    """ Read the CSV file and return replacement pairs and advanced rules. """
    pairs = []
    tf_rows = []  # Stores TF/tf rules
    try:
        with open(csv_path, "rb") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip the header row
            for row in reader:
                if len(row) >= 2:  # Ensure at least two columns exist
                    find_text = row[0].strip()
                    replace_text = row[1].strip()
                    type_value = row[2].strip().lower() if len(row) >= 3 else ""
                    action_value = row[3].strip().lower() if len(row) >= 4 else ""

                    if type_value == "v":
                        find_text = "<<{}>>".format(find_text)  # Modify Find Text if type is 'V' or 'v'

                    if type_value not in ['tf', 'TF']:  # Regular replacements
                        pairs.append((find_text, replace_text))
                    elif action_value in ['t', 'f']:  # Store TF/tf rows with action in column D
                        tf_rows.append((find_text, action_value))
    except Exception as e:
        notepad.messageBox("Error reading CSV file:\n{}".format(e), "Error")
        return [], []
    return pairs, tf_rows

def replace_text_in_notepad(replacements):
    """ Perform basic find & replace in Notepad++. """
    text = editor.getText()
    
    editor.beginUndoAction()

    for find_text, replace_text in replacements:
        text = text.replace(find_text, replace_text)

    editor.setText(text)

    editor.endUndoAction()

    notepad.messageBox("Find & Replace completed successfully!", "Success")

def advanced_replacement(text, tf_rows):
    """ Handles replacements where column C is TF/tf, supporting multi-line text. """
    for find_text, action in tf_rows:
        # Correctly format the start and end delimiters with proper escaping
        start_delim = re.escape("<<{}>>".format(find_text))
        end_delim = re.escape("<<{}/>>".format(find_text))

        # Regex pattern to find content between the delimiters (across multiple lines)
        pattern = r"{}(.*?){}".format(start_delim, end_delim)

        def replace_match(match):
            inner_text = match.group(1)  # Extract text inside delimiters
            if action == 't':  # Keep inner text, remove delimiters
                return inner_text.strip()
            elif action == 'f':  # Remove inner text and delimiters
                return ""
            return match.group(0)  # Default case (should never hit this)

        # Apply regex replacement
        text = re.sub(pattern, replace_match, text, flags=re.DOTALL)

    return text

def main():
    """ Main function to handle file loading, user prompt, and text replacement. """
    csv_path = None

    # Check for previously saved file
    last_used_file = get_last_used_file()
    if last_used_file:
        response = notepad.messageBox("Do you want to use the saved Data File?", "Use Saved File", MESSAGEBOXFLAGS.YESNO)
        if response == MESSAGEBOXFLAGS.RESULTYES:
            csv_path = last_used_file

    # If no valid saved file was chosen, prompt for a new one
    if not csv_path:
        csv_path = prompt_for_csv_file()

    # Ensure the path is valid
    if not csv_path or not os.path.isfile(csv_path):
        notepad.messageBox("CSV file not found or invalid path provided.", "Error")
        return

    # Save file path for future use
    save_last_used_file(csv_path)

    # Read replacement pairs and TF rows
    replacements, tf_rows = read_replacement_pairs(csv_path)

    if replacements:
        # Perform standard replacements
        replace_text_in_notepad(replacements)

        # Perform advanced replacements for TF/tf rows
        text = editor.getText()
        updated_text = advanced_replacement(text, tf_rows)
        
        # Update Notepad++ text
        editor.setText(updated_text)
        notepad.messageBox("Advanced Find & Replace completed successfully!", "Success")
    else:
        notepad.messageBox("No valid replacements found in the CSV file.", "Error")

# Run the script
main()
