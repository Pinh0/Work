import json
import time
from datetime import datetime,timedelta
import requests
import matplotlib.pyplot as plt
import numpy as np
import tzlocal

user_and_password = '{"username": "tpinho","password": "tp1nh0"}'
headers = {'Content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
def get_api_authtoken():
    res = requests.post("https://api.atcll-data.nap.av.it.pt/auth", data=user_and_password, headers=headers)    
    if res.status_code == 200:
        return res.headers.get('authorization')    
    
    print("Token is missing!!")
    print(res.text)

token = get_api_authtoken()

print(token)

#data inicio (dd-mm-aaaa)
date= "15-10-2023"

#número de dias para o gráfico da média
n_days = 6


#path save figures
path = "F:\Work\FigurasRadar"

local_timezone = tzlocal.get_localzone() # get pytz timezone
#data inicio (datetime)
start_date = datetime.strptime(date, "%d-%m-%Y")

#data fim (datetime)
end_date = start_date + timedelta(days=n_days)

        
#tempo de leitura em cada query em ms (recomendável não ser superior a 1h)
step = 3600000

#número de horas que vão surgir no gráfico
n_hours = 24
    
#data inicio (unixtime)
unixtime = int(time.mktime(start_date.timetuple()))*1000
    
    
max_vehicle = [0] * n_hours
mean_vehicle = [0] * n_hours

for i in range(n_hours):
    data = True
    headers = {'authorization': token, 'fiware-service' : 'aveiro_radar'}
    attributes = ['vehicleClass', 'numberVehicles']
    start = unixtime + i*step 
    end = start + step

    r = requests.get('https://api.atcll-data.nap.av.it.pt/history?type=traffic&start=' + str(start) + '&end=' + str(end) + '&attribute=faixa', headers=headers) 
    try:
        if(r.json()):  
            faixa = r.json()['urn:ngsi-ld:Traffic:aveiro_radar:p'+str(radar)]['faixa']
    except:
        data=False
        print("No data")