import requests
import pprint 
import json
import sys
import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import matplotlib as mpl
import seaborn as sns

# url = "https://api.atcll-data.nap.av.it.pt/history?type=count&attribute=location&start=1652778000000&end=1652778200000"

# payload={}
# headers = {
#   'fiware-service': 'aveiro_camera',
#   'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiJ0cGluaG8iLCJpYXQiOjE2ODAwMDQ0NDYsImV4cCI6MTY4MDA5MDg0Nn0.BUbjP6r4zfOdBSKmhqtcOj1lHMZs9cL6y-HAPwx0nR4'
# }

# response = requests.request("GET", url, headers=headers, data=payload)
# responsejson=response.json()
#for i in responsejson.items():
#  print(i)
# print(dict(responsejson.items())["urn:ngsi-ld:Count:aveiro_camera:p25"])
# with open("log.txt",'w') as f:
#   print(json.dumps(responsejson,indent=4),file=f)

f = open("response.json",'r')

data=json.load(f)
f.close()
smaldata=data['urn:ngsi-ld:Count:aveiro_camera:p35']
grouping=dict()
for i in range(len(smaldata['long'])):
  #print(smaldata['time_index'][i],smaldata['lat'][i],smaldata['long'][i])
  time=smaldata['time_index'][i][-8:]
  lat=round(smaldata['lat'][i],5)
  long=round(smaldata['long'][i],5)
  if time not in grouping:
    grouping[time]=[(lat,long)]
  else:
    grouping[time].append((lat,long))

minlat=round(min(smaldata['lat']),5)
minlong=round(min(smaldata['long']),5)
maxlat=round(max(smaldata['lat']),5)
maxlong=round(max(smaldata['long']),5)

counter=dict()
for lati in range(int(minlat*(10**5)),int(maxlat*(10**5)+1)):
  for longi in range(int(minlong*(10**5)),int(maxlong*(10**5)+1)):
    counter[(lati/10**5,longi/10**5)]=0

for time in grouping:
  for lat,long in grouping[time]:
    counter[(lat,long)]+=1

import pandas as pd
import matplotlib.pyplot as plt
ser = pd.Series(list(counter.values()),
                  index=pd.MultiIndex.from_tuples(counter.keys()))
df = ser.unstack().fillna(0)

g=sns.heatmap(df, xticklabels=True, yticklabels=True,alpha=0.5,zorder=2)

g.invert_yaxis()



print(minlong,maxlong,minlat,maxlat)
#TODO: Make the square on map

box = (minlong - 0.001, maxlong + 0.001, minlat - 0.001, maxlat + 0.001)

# mpl.rcParams['figure.dpi']= 50

# # Start session to get correct cookies in place (_osm_totp_token)
# session = requests.Session()
# session.headers.update({
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',
# })
# response = session.get('https://www.openstreetmap.org')

# scale = 3000
# while(True):
#     url = "https://render.openstreetmap.org/cgi-bin/export?bbox=" + str(box[0]) + "," + str(box[2]) + "," + str(box[1]) + "," + str(box[3]) + "&scale=" + str(scale) + "&format=png"
#     map = session.get(url)
#     # In case of 'Bad Request' response, retry until scale value does not lead to 'Map too large' errors
#     if map.status_code == 400:
#         scale += 200
#         continue
#     else:
#         break
# print(map.reason)

# file = open("sample_image.png", "wb")
# file.write(map.content)
# file.close()


file = open("sample_image.png", "rb")
ruh_m = plt.imread(file)
file.close()
# plt.imshow(ruh_m, zorder=0,aspect='equal',extent = box)
# plt.savefig("result.png")
# plt.show()

# import matplotlib.pyplot as plt
# import numpy as np

# Load the image
image = plt.imread("sample_image.png")

# Generate some random heatmap data
heatmap = np.random.rand(*image.shape[:2])

# Display the image and the heatmap on the same plot
fig, ax = plt.subplots()
ax.imshow(ruh_m)
ax.imshow(g)

# Save the resulting plot
plt.savefig("heatmap_over_image.png")