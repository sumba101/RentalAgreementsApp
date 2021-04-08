import requests
response=requests.get('https://httpbin.org/ip')
print('IP is {0}'.format(response.json()['origin']))
