def check_domain(newlink, domain, ignoreDomains, processDomains):
    if domain in processDomains:
        return True

    status = None

    try:
        status = requests.head(newlink).status_code
    except requests.ConnectionError:
        print "failed to connect"
        return False

    if status == 404 or status == 400:
        ignoreDomains.add(domain)
        return False

    if status > 299 and status < 400 :
        print "Check%s: " % (status) + newlink
        processDomains.add(domain)
        return True

    if status == 200:
        processDomains.add(domain)
        return True
    return False   
