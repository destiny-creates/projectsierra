#imports

import nmap3
import requests

#Variables and API keys

nmap = nmap3.Nmap()
nmapversion = nmap.nmap_version()
dnsdumpsterapi = 'REDACTED'

print(''' ___  ___  ___ 
| _ \| __||_ _|
|   /| _|  | | 
|_|_\|___||___|

               ''')
print('REI Recon, at your service\n')
target = input('Target domain:')

def processdumpster(data):
    for item in data:
        print('Host:' + item['host'])
        for ip in item['ips']:
            print('IP: ' + ip['ip'])
            print('ASN_NAME:' + ip['asn_name'])
            print('Country:' + ip['country'])
            print('City:' + ip.get('city', 'Not found'))
            print('-----------------------')

def dumpster():
    url = f'https://api.dnsdumpster.com/domain/{target}'
    headers = {'X-Api-Key': dnsdumpsterapi}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        pass
    else:
        print('Error connecting to DNSdumpster.')
    data = response.json()
    print('\nA records:\n')
    processdumpster(data['a'])
    print('MX records:\n')
    processdumpster(data['mx'])
    print('NS records:\n')
    processdumpster(data['ns'])

def processdns(target):
    dns_results = nmap.nmap_dns_brute_script(target)
    for item in dns_results:
        print('Hostname: ' + item['hostname'])
        print('IP Address: ' + item['address'] + '\n')
        print('-----------------------')


def processversion(target):
    version_results = nmap.nmap_version_detection(target)
    ip_address = next(iter(version_results))
    version = version_results[ip_address]
    for port in version['ports']:
        print('Protocol: ' + port['protocol'])
        print('Port: ' + port['portid'])
        print('State: ' + port['state'])
        print('Type: ' + port['reason'])
        print('-----------------------')
        # for service in port['service']:
        #     print('Name: ' + service['name'])
        #     print('Product: ' + service['product'])
        #The above commented code is still needing to be worked.


def nmapmodule():
    print('\nNmap version: ' + str(nmapversion))
    processdns(target)
    processversion(target)

def main():
    print('Running DNS dumpster module\n')
    dumpster()
    print('Running NMAP DNS module\n')
    processdns(target)
    print('Running NMAP version detection module\n')
    processversion(target)

if __name__ == '__main__':
    main()