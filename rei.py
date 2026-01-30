#imports

import nmap3
import requests

#Variables and API keys

nmap = nmap3.Nmap()
dnsdumpsterapi = 'REDACTED'

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


# def processversion(target):
#     version_results = nmap.nmap_version_detection(target)
#     ip_address = next(iter(version_results))
#     version = version_results[ip_address]
#     for port in version['ports']:
#         print('[+] Protocol: ' + port['protocol'])
#         print('[+] Port: ' + port['portid'])
#         print('[+] State: ' + port['state'])
#         print('-----------------------')
#         # for service in port['service']:
#         #     print('Name: ' + port['service'][service])

def processtopports(target):
    top_ports = nmap.scan_top_ports(target)
    ports_results = next(iter(top_ports))
    portid = top_ports[ports_results]
    for port in portid['ports']:
        print('[+] Port: ' + port['portid'])
        print('[+] Protocol: ' + port['protocol'])
        print('[+] State: ' + port['state'])
        print('-----------------------')


def main():
    print('Running DNS dumpster module\n')
    dumpster()
    print('Running NMAP DNS module\n')
    processdns(target)
    print('Running NMAP top ports module\n')
    processtopports(target)
    # print('Running NMAP version detection module\n')
    # processversion(target)


if __name__ == '__main__':
    main()
