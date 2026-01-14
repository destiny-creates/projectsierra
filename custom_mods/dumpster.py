import requests
from custom_mods.keylist import dnsdumpsterapi
#If you have plus membership, replace the response variable with the line below
#response = requests.get(url, headers=headers, params={'map': '1'})

def processor(data):
    for item in data:
        print('Host:' + item['host'])
        for ip in item['ips']:
            print('IP: ' + ip['ip'])
            print('ASN_NAME:' + ip['asn_name'])
            print('Country:' + ip['country'])
            print('City:' + ip.get('city', 'Not found'))
            print('-----------------------')

def main():
    target = input('Target domain:')
    url = f'https://api.dnsdumpster.com/domain/{target}'
    headers = {'X-Api-Key': dnsdumpsterapi}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        pass
    else:
        print('Error connecting to DNSdumpster.')
    data = response.json()
    print('\nA records:\n')
    processor(data['a'])
    print('MX records:\n')
    processor(data['mx'])
    print('NS records:\n')
    processor(data['ns'])
    print('\n\nHappy hunting :)')
