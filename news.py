import requests
url = ('https://newsapi.org/v2/top-headlines?'
       'country=us&'
       'apiKey=c0e865345b744fe8b9fb282ac3e1f7c0')
response = requests.get(url)
print(response.json())