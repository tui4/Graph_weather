#! /usr/bin/env python

import mechanize
import cookielib
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
import re
import matplotlib.pyplot as plt



# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.102011-10-16 20:23:50')]


mech = Browser()
url = 'http://www.bom.gov.au/sa/forecasts/adelaide.shtml'
page = mech.open(url)
html = page.read()

soup = BeautifulSoup(html)
content = soup.find("div",id='content')


links = []

todays_data = []
for div in content.findAll('div'):
  if div['class'] == 'day main':
    day = re.match('Forecast.*of (.*)',div.h2.string).group(1)
    data = []
    for bit in div.findAll('dd'):
      for ems in bit.findAll('em'):
        if ems['class'] == 'max':
          data.append(ems.string)
        else:
          continue
    todays_data.append([day,data])

days_data = []
for div in content.findAll('div'):
  if div['class'] == 'day':
    day = div.h2.string
    data = []
    for bit in div.findAll('dd'):
      try:
        data.append(bit.em.string)
      except:
        continue
    days_data.append([day,data])
   
all_data = [todays_data + days_data][0]
print int(all_data[2][1][1])
max_t = []
min_t = []
days = []
for day in all_data:
  try:
    min_t.append(day[1][0])
    max_t.append(day[1][1])
    days.append(day[0])
  except:
    continue


plt.plot(max_t,'r')
plt.plot(min_t,'b')

plt.ylabel('Temperature')
plt.show()

#new = mech.select_form(links[0])
#new = mech.follow_link(links[0])
#new = mech.[links[0]]

