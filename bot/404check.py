def check_domain(newlink,domain,ignoreDomains,processDomains):
    if domain in processDomains:
        return True
    else:
        try:
            status = requests.head(newlink).status_code
            if status == 404:
                ignoreDomains.add(domain)
                return False
            if status == 400:
                ignoreDomains.add(domain)
                return False
            if (status > 299) and (status<400):
                print "Check%s: "%(status)+newlink
                processDomains.add(domain)
                return True
            if status == 200:
                processDomains.add(domain)
                return True
            else:
                return False    
        except requests.ConnectionError:
            print "failed to connect"
            return False