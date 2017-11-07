#!/usr/bin/python

import getpass
import urllib2

class HTTPProxy:
    def __init__(self, host, port, user):
        self.host=host
        self.port=port
        self.user=user
        self.pwd=getpass.getpass('Enter password for {}:'.format(user))
        proxyString='http://{}:{}@{}:{}'.format(self.user,
                                                self.pwd,
                                                self.host,
                                                self.port)
        proxy = urllib2.ProxyHandler({'http':proxyString})
        auth=urllib2.HTTPBasicAuthHandler()
        opener=urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        
    def getUrlLib(self):
        return urllib2
        
