# Use python to read the file regex_test.txt and print the last name on each line using
# regular expressions and groups (return None for names with no first and last name, or names that aren't properly capitalized)
import re

with open ("regex_test.txt") as my_file:
    data = my_file.read()

pattern = re.compile(r"[A-Z]{1}\w+[' ']([A-Z]{1}\w+|[A-Z]{1})([' '][A-Z]{1}\w+|)")

for names in data.split("\n"):
    match = pattern.match(names)
    if match:
        print(match.group())
    else:
        print("None")