import requests

data = requests.post('http://127.0.0.1:5000/ad/',
                     json={
                         'title': 'ad_1',
                         'description': 'Text',
                         'owner': 'Person_1',
                     })

print(data.status_code)
print(data.text)