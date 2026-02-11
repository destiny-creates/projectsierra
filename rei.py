# imports
import subprocess

import nmap3
import requests
from pymenu import Menu

# Variables and API keys

nmap = nmap3.Nmap()
dnsdumpsterapi = ''
wpscanapi = ''

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
    target = input('[+] Target domain:')
    url = f'https://api.dnsdumpster.com/domain/{target}'
    headers = {'X-Api-Key': dnsdumpsterapi}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        pass
    else:
        print('Error connecting to DNSdumpster.')
        exit()
    data = response.json()
    print('\n[+] A records:\n')
    processdumpster(data['a'])
    print('[+] MX records:\n')
    processdumpster(data['mx'])
    print('[+] NS records:\n')
    processdumpster(data['ns'])


def processdns():
    target = input('[+] Target domain:')
    dns_results = nmap.nmap_dns_brute_script(target)
    for item in dns_results:
        print('\n[+] Hostname: ' + item['hostname'])
        print('[+] IP Address: ' + item['address'] + '\n')
        print('-----------------------')


def processversion():
    target = input('[+] Target domain:')
    version_results = nmap.nmap_version_detection(target)
    ip_address = next(iter(version_results))
    version = version_results[ip_address]
    for port in version['ports']:
        print('\n[+] Protocol: ' + port['protocol'])
        print('[+] Port: ' + port['portid'])
        print('[+] State: ' + port['state'])
        print('[+] Name: ' + port['service']['name'])
        print('-----------------------')


def processtopports():
    target = input('[+] Target domain:')
    top_ports = nmap.scan_top_ports(target)
    ports_results = next(iter(top_ports))
    port = top_ports[ports_results]
    for port in port['ports']:
        print('\n[+] Port: ' + port['portid'])
        print('[+] Protocol: ' + port['protocol'])
        print('[+] State: ' + port['state'])
        print('[+] Service: ' + port['service']['name'])
        print('-----------------------')


def processos():
    target = input('[+] Target domain:')
    os_results = nmap.nmap_os_detection(target)
    ip_address = next(iter(os_results))
    os_version = os_results[ip_address]
    for item in os_version['osmatch']:
        print('\n[+] OS: ' + item['name'])
        print('[+] Family: ' + item['osclass']['osfamily'])
        print('[+] Type: ' + item['osclass']['type'])
        print('[+] Generation: ' + item['osclass']['osgen'])
        print('[+] Accuracy: ' + item['accuracy'])
        print('-----------------------')


def xsstest():
    target = input('[+] Target domain:')
    url = f'https://www.{target}/search?'
    payloads = ['<script>alert(1)</script>', '"><img src=x onerror=alert(1)>']
    for payload in payloads:
        params = {'q': payload}
        r = requests.get(url, params=params)
        if payload in r.text:
            print(f'\n[XSS] Payload reflected: {payload}')
        else:
            print(f'\n[XSS] Not vulnerable to payload: {payload}')


def vulnscanmodule():
    target = input('[+] Target URL/IP Address: ')
    subprocess.run(f'''nmap --script vuln --script-args mincvss+5.0 {target}''', shell=True)

def wpscanmodule():
    target = input('[+] Target URL/IP Address: ')
    subprocess.run(f'''wpscan --api-token {wpscanapi} --url {target} --random-user-agent --force''')

menu = Menu('''

 ____  _____ ___ 
|  _ \| ____|_ _|
| |_) |  _|  | | 
|  _ <| |___ | | 
|_| \_\_____|___|

\nREI recon, at your service''')
menu.add_option('[+] DNS dumpster module', lambda: dumpster())
menu.add_option('[+] NMAP DNS module', lambda: processdns())
menu.add_option('[+] NMAP version detection module', lambda: processversion())
menu.add_option('[+] NMAP top ports module', lambda: processtopports())
menu.add_option('[+] NMAP os module', lambda: processos())
menu.add_option('[+] XSS detection module', lambda: xsstest())
menu.add_option('[+] CVE scanner (NMAP)', lambda: vulnscanmodule())
menu.add_option('[+] Wordpress scanner (WPScan API required)', lambda: wpscanmodule())
menu.show()
