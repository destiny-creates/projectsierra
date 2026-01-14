def shodansearcher():
    import shodan
    from custom_mods.keylist import shodanapikey
    api = shodan.Shodan(shodanapikey)
    search = input("Query:")
    results = api.search(search)
    print('Results found: {}'.format(results['total']))
    for result in results['matches']:
        print('IP: {}'.format(result['ip_str']))
        print(result['data'])
        print('')
