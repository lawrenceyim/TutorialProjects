#! python3

import re, pyperclip

# regex for phone number
phone_regex = re.compile(r'''
(((\d\d\d)|(\(\d\d\d\)))?  # area code (optional)
(\s|-)  # first separator
\d\d\d  # first 3 digits
-  # separator
\d\d\d\d  # last 4 digits
(((ext(\.)?\s)|x) # extension word-part (optional)
(\d{2, 5}))?)  # extension number-part (optional)
''', re.VERBOSE)

# regex for email addresses
email_regex = re.compile(r'''
[a-zA-Z0-9_.+]+  # name portion
@  # @ symbol
[a-zA-Z0-9_.+]+  # domain name portion

''', re.VERBOSE)

# read text off of the clipboard
text = pyperclip.paste()

# extract email and phone numbers from text variable
extracted_phone_numbers = phone_regex.findall(text)
extracted_email_addresses = email_regex.findall(text)

# list of only the first regex group from each extracted phone number
all_phone_numbers = []
for phone_numbers in extracted_phone_numbers:
    all_phone_numbers.append(phone_numbers[0])

#
results = '\n'.join(all_phone_numbers) + '\n' + '\n'.join(extracted_email_addresses)
pyperclip.copy(results)
