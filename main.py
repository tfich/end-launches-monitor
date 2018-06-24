@@ -0,0 +1,115 @@
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random, requests, json, time
from proxymanager import ProxyManager
from logger import *

#----config----#
webhook = 'https://hooks.slack.com/services/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' #slack or discord
delay = '10' #seconds (time doesn't really matter)
useProxies = True
#----config----#

print('\n###########################')
print('###      END Monitor    ###')
print('### Developed By @tfich ###')
print('############################\n')
time.sleep(1)

print('Script Started')

if webhook.startswith('https://discordapp.com/'):
    webhook = webhook+'/slack'
proxy_manager = ProxyManager('proxies.txt')
s = requests.session()
currentIDs = []
endpoint = 'https://launches-api.endclothing.com/api/products/offset/0'

def init():
    if useProxies == True:
        random_proxy = proxy_manager.random_proxy()
        proxies = random_proxy.get_dict()
        response = s.get(endpoint, proxies=proxies)
    if useProxies == False:
        response = s.get(endpoint)
    responseJson = json.loads(response.text)
    for id in responseJson['products']:
        #currentIDs.append(id['id'])
        log('Added to Database - {}'.format(id['id']))

init()

def scrape():
    while True:
        try:
            if useProxies == True:
                random_proxy = proxy_manager.random_proxy()
                proxies = random_proxy.get_dict()
                response = s.get(endpoint, proxies=proxies)
            if useProxies == False:
                response = s.get(endpoint)
            responseJson = json.loads(response.text)
            for id in responseJson['products']:
                if id['id'] in currentIDs:
                    log('Product ID already found - {}'.format(id['id']))
                    continue
                if id['id'] not in currentIDs:
                    log('New Product ID found - {}'.format(id['id']))
                    productName = '{} - {}'.format(id['name'], id['colour'])
                    productSKU = id['magentoSku']
                    productEngine = id['releaseMode']
                    productLauchDate = id['releaseDate']
                    if productEngine == 'prepaid-draw':
                        productEngine = 'Prepaid Draw'
                    productURL = 'https://launches.endclothing.com/product/{}'.format(id['urlKey'])
                    productImageURL = id['thumbnailUrl']
                    productPrice = id['productWebsites'][0]['price']
                    currentIDs.append(id['id'])
                    message = {
                      "fallback": "{}".format(productName),
                      "username": "END Launches Monitor",
                      "icon_url": "https://bit.ly/2tzQ7Oj",
                      "attachments": [
                        {
                          "author_name": "New END Launches Product Found",
                          "author_icon": "https://bit.ly/2tzQ7Oj",
                          "title": productName,
                          "title_link": productURL,
                          "color": "#000000",
                          "fields": [
                          {
                              "title": "Price: ",
                              "value": "£{}".format(productPrice),
                              "short": True
                          },
                          {
                              "title": "SKU: ",
                              "value": "{}".format(productSKU),
                              "short": True
                          },
                          {
                              "title": "Release Date: ",
                              "value": "{}".format(productLauchDate[:-15]),
                              "short": True
                          },
                          {
                              "title": "Release Type: ",
                              "value": "{}".format(productEngine),
                              "short": True
                          },
                          ],
                          "thumb_url": productImageURL,
                          "footer": "Cop2flip",
                          "footer_icon": "https://pbs.twimg.com/profile_images/945922188284018689/6OOQs1dV_400x400.jpg"
                        }
                      ]
                    }

                    ss = requests.session()
                    res = ss.post(webhook,json=message)

            time.sleep(int(delay))
        except Error as e:
            log('Error - {}'.format(e))

scrape()
