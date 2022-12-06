from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
import json
import actions
import const as c

try:
    config = actions.load_config()
    configured = True
except Exception:
    configured = False

if configured == True:
    format = actions.default_format
    media = actions.default_media
    release = actions.default_release

# question1_choice = [
#     Separator(),
#     Choice("ap-southeast-2", name="Sydney", enabled=True),
#     Choice("ap-southeast-1", name="Singapore", enabled=False),
#     Separator(),
#     "us-east-1",
#     "us-west-1",
#     Separator(),
# ]

question1_choice = []

for i in c.releases:
    if c.releases[i] in actions.default_release:
        question1_choice.append(Choice(c.releases[i], enabled=True))
    else:
        question1_choice.append(Choice(c.releases[i], enabled=False))

question2_choice = []

for i in c.formats:
    if c.formats[i] in actions.default_format:
        question2_choice.append(Choice(c.formats[i], enabled=True))
    else:
        question2_choice.append(Choice(c.formats[i], enabled=False))

question3_choice = []

for i in c.media:
    if c.media[i] in actions.default_media:
        question3_choice.append(Choice(c.media[i], enabled=True))
    else:
        question3_choice.append(Choice(c.media[i], enabled=False))

question4_choice = []

for i in c.top_list_count:
    if i == actions.toplist_limit:
        question4_choice.append(Choice(i, enabled=True))
    else:
        question4_choice.append(Choice(i, enabled=False))


def main():
    release_selection = inquirer.checkbox(
        message="Select the releases you wish to see by default:",
        choices=question1_choice,
        # cycle=False,
        # transformer=lambda result: "%s release%s selected"
        # % (len(result), "s" if len(result) > 1 else ""),
        validate=lambda result: len(result) >= 1,
        invalid_message="should be at least 1 selection",
        instruction="(select at least 1)",
    ).execute()
    format_selection = inquirer.checkbox(
        message="Select the formats you wish to see by default:",
        choices=question2_choice,
        validate=lambda result: len(result) >= 1,
        invalid_message="should be at least 1 selection",
        instruction="(select at least 1)",
    ).execute()
    media_selection = inquirer.checkbox(
        message="Select the media types you wish to see by default:",
        choices=question3_choice,
        validate=lambda result: len(result) >= 1,
        invalid_message="should be at least 1 selection",
        instruction="(select at least 1)",
    ).execute()
    media_selection = inquirer.checkbox(
        message="How many results do you want to see when searchign the Top X lists?:",
        choices=question3_choice,
        validate=lambda result: len(result) >= 1,
        invalid_message="should be at least 1 selection",
        instruction="(select at least 1)",
    ).execute()


if __name__ == "__main__":
    main()