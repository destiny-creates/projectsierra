# imports

import subprocess

import nmap3
import requests

# Variables and API keys

nmap = nmap3.Nmap()
dnsdumpsterapi = 'REDACTED'

subprocess.run('clear', shell=True)
print('''

 ____  _____ ___ 
|  _ \| ____|_ _|
| |_) |  _|  | | 
|  _ <| |___ | | 
|_| \_\_____|___|

''')
print('REI Recon, at your service\n')
target = input('Target domain:')

def processdumpster(data):
    for item in data:
        print('[+] Host:' + item['host'])
        for ip in item['ips']:
            print('[+] IP: ' + ip['ip'])
            print('[+] ASN_NAME:' + ip['asn_name'])
            print('[+] Country:' + ip['country'])
            print('[+] City:' + ip.get('city', 'Not found'))
            print('-----------------------')


def dumpster():
    url = f'https://api.dnsdumpster.com/domain/{target}'
    headers = {'X-Api-Key': dnsdumpsterapi}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        pass
    else:
        print('Error connecting to DNSdumpster.')
        exit()
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
        print('[+] Hostname: ' + item['hostname'])
        print('[+] IP Address: ' + item['address'] + '\n')
        print('-----------------------')


def processversion(target):
    version_results = nmap.nmap_version_detection(target)
    ip_address = next(iter(version_results))
    version = version_results[ip_address]
    for port in version['ports']:
        print('[+] Protocol: ' + port['protocol'])
        print('[+] Port: ' + port['portid'])
        print('[+] State: ' + port['state'])
        print('[+] Name: ' + port['service']['name'])
        print('-----------------------')


def processtopports(target):
    top_ports = nmap.scan_top_ports(target)
    ports_results = next(iter(top_ports))
    port = top_ports[ports_results]
    for port in port['ports']:
        print('[+] Port: ' + port['portid'])
        print('[+] Protocol: ' + port['protocol'])
        print('[+] State: ' + port['state'])
        print('[+] Service: ' + port['service']['name'])
        print('-----------------------')
def processos(target):
    os_results = nmap.nmap_os_detection(target)
    ip_address = next(iter(os_results))
    os_version = os_results[ip_address]
    for item in os_version['osmatch']:
        print('[+] OS: ' + item['name'])
        print('[+] Family: ' + item['osclass']['osfamily'])
        print('[+] Type: ' + item['osclass']['type'])
        print('[+] Generation: ' + item['osclass']['osgen'])
        print('[+] Accuracy: ' + item['accuracy'])
        print('-----------------------')
def xsstest(target):
    url = f'https://www.{target}/search?'
    payloads = ['<script>alert(1)</script>', '"><img src=x onerror=alert(1)>']
    for payload in payloads:
        params = {'q': payload}
        r = requests.get(url, params=params)
        if payload in r.text:
            print(f'[XSS] Payload reflected: {payload}')
        else:
            print(f'[XSS] Not vulnerable to payload: {payload}')

def main():
    print('\n[+] Running DNS dumpster module\n')
    dumpster()
    print('\n[+] Running NMAP DNS module\n')
    processdns(target)
    print('\n[+] Running NMAP version detection module\n')
    processversion(target)
    print('\n[+] Running NMAP top ports module\n')
    processtopports(target)
    print('\n[+] Running NMAP OS detection module\n')
    processos(target)
    print('\n[+] Running XSS module\n')
    xsstest(target)
    print('\n[+] Happy hunting :)')

if __name__ == '__main__':
    main()
