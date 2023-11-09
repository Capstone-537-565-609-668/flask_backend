import requests

url = "https://api.planetscale.com/v1/organizations/nireeshadrai/databases/spatial-analysis/tables/bangalore/rows"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

print(response.text)