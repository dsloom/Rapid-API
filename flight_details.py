import mysql.connector
import requests
from datetime import timedelta
from pprint import pprint
import json
import os 
from pathlib import Path 
os.chdir(Path(__file__).parent)

mydb = mysql.connector.connect(
    host="localhost", # or the ip of the mysql server
    user="root",
    password="root",
    database="gans"
)


def get_icao():
    # 2. create a cursor (like a servent)
    cursor = mydb.cursor() 

    # 3. SQL Statement
    sql = "SELECT icao from airport_icao;"
    
    # 4. Execute (RUN) the SQL Statement
    cursor.execute(sql)

    icao_details = cursor.fetchall()
    return icao_details


def get_date_time():
    # 2. create a cursor (like a servent)
    cursor = mydb.cursor() 

    # 3. SQL Statement
    sql = "SELECT date_time from current_weather;"
    
    # 4. Execute (RUN) the SQL Statement
    cursor.execute(sql)

    date_time_deatils = cursor.fetchall()
    return date_time_deatils
def fetch_data(icao_details,date_time_deatils):
    #print(icao_details,date_time_deatils)
    for icao in icao_details:
        
        icao_name=icao[0]
        #print(icao_name)
        for date_time in date_time_deatils:
            start_date=date_time[0]
            #print(start_date)
            end_date=start_date + timedelta(hours=11)

            date_s = start_date.strftime("%Y-%m-%d")
            time_s=start_date.strftime("%H:%M")
            date_e = end_date.strftime("%Y-%m-%d")
            time_e=end_date.strftime("%H:%M")
            #print(date_s,time_s,date_e)
            #url = f"https://aerodatabox.p.rapidapi.com/flights/airports/icao/{icao_name}/{date_s}T{time_s}/{date_e}T{time_e}"
            #print(url)
            url = f"https://aerodatabox.p.rapidapi.com/flights/airports/icao/EDDB/{date_s}T{time_s}/{date_e}T{time_e}"
 

            querystring = {"withLeg":"true","direction":"Both","withCancelled":"true","withCodeshared":"true","withCargo":"true","withPrivate":"true","withLocation":"false"}

            headers = {
	        "X-RapidAPI-Key": "45df0e68a9mshecfc69b2ccd57a8p1f7e64jsn74c1d275089d",
	        "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"
}

            response = requests.request("GET", url, headers=headers, params=querystring)

            if response.status_code == 200:
                #print(response.status_code, response.headers.get("content-type"), url)
                pprint(response.json())
            # print(response.text)
            
            

            
            #print(airport_details)

           






def main():
    icao_details=get_icao()
    date_time_deatils=get_date_time()
    fetch_data(icao_details,date_time_deatils)

   
main()    
