import requests
from time import sleep

API_KEY = '929F0011-902B-468D-9ED4-1859E0D1679D'
HOST = 'https://rest.coinapi.io/'

LOCALHOST = 'http://127.0.0.1:8000'
link = LOCALHOST + '/links/admin/crypto'

token = """Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY1NTkxNjMwLCJqdGkiOiI0YTllNGJmNWJiY2E0OGI2OTJhMTQ1YjY5NjZmZjI5NyIsInVzZXJfaWQiOjF9.sHZ5V8NCWYHV5hsYeEhXiwLcyLfXuFqwOmnAfjtp2W4"""

headers = {'X-CoinAPI-Key': API_KEY}

icon_url = 'v1/assets/icons/48'

print('Starting to Fetch Asset with their icons ...')

sleep(0.5)

print('Data is Fetching ...')
response = requests.get(HOST + icon_url, headers=headers)


coins = []

data = response.json()

print('Data Fetch is Completed')
sleep(1)

for asset in data:
    asset_id = asset.get('asset_id')
    icon_url = asset.get('url')

    print(f'Adding {asset_id} to database ...')

    requests.post(link, headers={'Authorization': token}, data={
        'wallet_address': '',
        'coin_type': asset_id,
        'icon_url': icon_url
    })

    if response.status_code == 200:
        print(f'Asset {asset_id} Successfully Added to DB')
    else:
        print(f'Asset {asset_id} Failed!')

    sleep(1.5)
