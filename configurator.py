from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import PathValidator
import json
import const as c
import actions as a

def main(release, format, media, limit, freeleech, file_dir):

    question1_choice = []

    for i in c.releases:
        if c.releases[i] in release:
            question1_choice.append(Choice(c.releases[i], enabled=True))
        else:
            question1_choice.append(Choice(c.releases[i], enabled=False))

    question2_choice = []

    for i in c.formats:
        if c.formats[i] in format:
            question2_choice.append(Choice(c.formats[i], enabled=True))
        else:
            question2_choice.append(Choice(c.formats[i], enabled=False))

    question3_choice = []

    for i in c.media:
        if c.media[i] in media:
            question3_choice.append(Choice(c.media[i], enabled=True))
        else:
            question3_choice.append(Choice(c.media[i], enabled=False))


    release_selection = inquirer.checkbox(
        message="Select the releases you wish to see by default:\n(Press space to toggle one; Press ctrl+a to toggle all)",
        choices=question1_choice,
        validate=lambda result: len(result) >= 1,
        invalid_message="should be at least 1 selection",
        instruction="(select at least 1)",
    ).execute()
    format_selection = inquirer.checkbox(
        message="Select the formats you wish to see by default:\n(Press space to toggle one; Press ctrl+a to toggle all)",
        choices=question2_choice,
        validate=lambda result: len(result) >= 1,
        invalid_message="should be at least 1 selection",
        instruction="(select at least 1)",
    ).execute()
    media_selection = inquirer.checkbox(
        message="Select the media types you wish to see by default:\n(Press space to toggle one; Press ctrl+a to toggle all)",
        choices=question3_choice,
        validate=lambda result: len(result) >= 1,
        invalid_message="should be at least 1 selection",
        instruction="(select at least 1)",
    ).execute()
    toplimit_selection = inquirer.select(
        message="How many results do you want to see when searching the Top X lists?:",
        choices=[10,100,250],
        multiselect=False,
        default=limit
    ).execute()
    freeleech_selection = inquirer.confirm(
        message="Do you want to automatically use available freeleech tokens when downloading torrent files?",
        default=freeleech
    ).execute()
    dest_path = inquirer.filepath(
        message="Enter the path where you want files to be downloaded to:",
        validate=PathValidator(is_dir=True, message="Input is not a directory"),
        only_directories=True,
        default = file_dir
    ).execute()
    
    c.config_json["defaults"]["release"] = release_selection
    c.config_json["defaults"]["media"] = media_selection
    c.config_json["defaults"]["format"] = format_selection
    c.config_json["toplist_limit"] = toplimit_selection
    c.config_json["freeleech"] = freeleech_selection
    if dest_path[-1] == "/":
        c.config_json["file_dir"] = dest_path
    elif dest_path[-1] != "/":
        c.config_json["file_dir"] = dest_path + "/"

    with open(a.config_path, "w") as f:
        json.dump(c.config_json, f, indent=4)

if __name__ == "__main__":
    main()