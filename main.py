from custom_mods import api_search
from custom_mods import ddos
from custom_mods import portscan
from custom_mods import dumpster


def menu():
    selection = input("""██████ ██████  █████     ██████████ █████ ███████        █████ ████████████████████ ██████   ███         
█     ██     ██     █      ██      █     █   █          █         █   █      █     ██     █ █   █        
██████ ██████ █     █      ██      █         █           █████    █   █      ██████ ██████ █     █       
█      █   █  █     █      ██████  █         █                █   █   █████  █   █  █   █  ███████       
█      █    █ █     ██     ██      █     █   █                █   █   █      █    █ █    █ █     █       
█      █     █ █████  █████ ███████ █████    █           █████ ███████████████     ██     ██     █       
                                                                                                         

[1]: shodan search (coming soon)
[2]: DDOS tool (coming soon)
[3]: Port scanner (nmap based)
[4]: DNSdumpster (API key required)

*****MORE COMING SOON*********

Selection: """)
    if selection == "1":
        print('Coming soon')
    if selection == "2":
        print('Coming soon')
    if selection == "3":
        portscan.main()
    if selection == "4":
        dumpster.main()


menu()
