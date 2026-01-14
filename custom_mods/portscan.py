import nmap3

nmap = nmap3.Nmap()


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


def main():
    target = input("Target: ")
    processdns(target)
    processversion(target)
