import requests
import re
import os

olditems = []

with open('itemslist', 'a+') as itemslist, open('itemslistold', 'a+') as itemslistold:
    for item in itemslist.readlines() + itemslistold.readlines():
        olditems.append(item[:-1] + '\n')
os.remove('itemslist')
os.remove('itemslistold')
with open('itemslistold', 'a') as oldlist:
    for item in list(set(olditems)):
        oldlist.write(item)
with open('forumslist', 'r') as forumslist, open('itemslist', 'a+') as itemslist:
    for forumname in forumslist.readlines():
        if not re.search(r'\...f$', forumname): # ignore these forums, threads discovery is different on these
            response = requests.get('http://%s.yuku.com/feed/get/type/rss/source/domain/'%(forumname[:-1]))
            highestid = 0
            for topicid in re.findall(r'/topic/([0-9]+)/', response.text):
                if int(topicid) > highestid:
                    highestid = int(topicid)
                    print('Found %s topics for forum %s.'%(topicid, forumname[:-1]))
            items = []
            if len(str(highestid)) > 1:
                for num in range(0, int(str(highestid)[:-1]) + 1):
                    items.append('yuku:10threads:' + forumname[:-1] + ':' + str(num) + '\n')
            for num in range(0, 10):
                items.append('yuku:thread:' + forumname[:-1] + ':' + str(num) + '\n')
            for item in items:
                if not item in olditems:
                    if len(items) > 1000000:
                        if os.path.isfile('itemlist_' + forumname):
                            os.remove('itemlist_' + forumname)
                        with open('itemlist_' + forumname, 'a') as itemslistlarge:
                            itemslistlarge.write(item)
                    else:
                        itemslist.write(item)