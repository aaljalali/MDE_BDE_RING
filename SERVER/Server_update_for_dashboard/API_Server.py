from typing import Optional
from fastapi import FastAPI, Query
from pydantic import BaseModel
from json_operations import  *
from folder_operations import *
from json_operations import *
import sqlite
import timer
from datetime import date
from calculete_performance import *
import json
##############################
########    VAR      #########
##############################
app = FastAPI()
program_folder_path = './json/'
db_name = 'Pi_server.db'


##############################
######     Classes     #######
##############################
class MachineData(BaseModel):
    TS: str
    Station_ID: int
    Machine_performance: Optional[str] = None
    Program_name: Optional[str] = None
    Tool_number: Optional[str] = None

    class Config:
        orm_mode = True

class OperationData(BaseModel):
    TS: str
    Station_ID: int
    RFID: int
    Order_number: Optional[str] = None
    Part_number: Optional[str] = None
    Performance_ID: int
    Duration_sec: Optional[int] = None

    class Config:
        orm_mode = True

##############################
## to check the connection between the client and the server
##############################
@app.get('/health')
def health_check():
    return{"status": "ok"}

##############################
######  post Machine data   
############################## 
@app.post("/mde/")
def post_Machine_data(md: MachineData):
    # add the data to the database
    sqlite.add_mde_data_to_db(md)
    
    # convert the posted Class object to json
    json_md = dict(md)
    
    # create folders (json_mde->current year->current month) if not exists
    json_mde_path = current_json_path(program_folder_path, 'mde')
    
    # create json file under machine id in the current month folder
    # if not exists and append the new data, the check that successfully done
    succse_append = json_append(json_mde_path, json_md)
    
    if succse_append:
        # do something like return md
        pass
    else:
        # do something like sending a notification or retry
        pass
    
    print('json_md', json_md)
    
    return md

##############################
###### delete operation data     
##############################
@app.post("/mde/{station_id}/drob_last_activity/")
def delete_last_Machine_data(station_id:int):
    print(f'>>>>>>>>>>>>>>>station_id = {station_id}>>>>>>>>>>>>>>>>>>')
   
    # Delete the last added data from the database
    deleted_data = sqlite.delete_last_data_from_db('mde', station_id)
    print('deleted data >> ', deleted_data)
    
    # Delete the last added data from the JSON file
    #json_mde_path = current_json_path(program_folder_path, 'mde')
   # remove_last_object_from_file(json_mde_path)
    
    return {'message': 'Last operation data has been deleted successfully.'}

##############################
###### post operation data     
##############################
@app.post("/bde/")
def post_operation_data(od: OperationData):
    # add the data to the database
    sqlite.add_bde_data_to_db(od)
    
    
    # Konvertiere das gepostete Klassenobjekt in JSON
    json_od = od.dict()
    # Erstelle Ordner (json_bde-> aktuelles Jahr-> aktueller Monat), wenn nicht vorhanden
    json_mde_path = current_json_path(program_folder_path, 'bde')
    # Erstelle JSON-Datei unter der Maschinen-ID im aktuellen Monatsordner
    # wenn nicht vorhanden und füge die neuen Daten hinzu, überprüfe dann, ob es erfolgreich war
    if json_append(json_mde_path, json_od):
        # Führe etwas aus wie z.B. Rückgabe von md
        pass
    else:
        pass
        # Führe etwas aus wie z.B. das Senden einer Benachrichtigung oder einen erneuten Versuch
    print('json_md', json_od)
    return od

##############################
###### delete operation data                 
##############################
@app.post("/bde/{station_id}/drob_last_activity/")
def delete_last_operation_data(station_id:int):
    print(f'>>>>>>>>>>>>>>>station_id = {station_id}>>>>>>>>>>>>>>>>>>')
    # Delete the last added data from the database
    
    deleted_data = sqlite.delete_last_data_from_db('bde',station_id)
    print('deleted data >> ', deleted_data)
    
   # Delete the last added data from the JSON file
    #json_mde_path = current_json_path(program_folder_path, 'bde')
   #json_operations.remove_last_object_from_file(json_mde_path)
    
    return {'message': 'Last operation data has been deleted successfully.'}



##############################
###### # Get BDE or MDE data from start date to end date      
##############################
@app.get("/{data_type}/{station_id}")
async def get_activities_from_to(station_id: int,
                                 data_type: str = Query(..., description="bde, mde"), 
                                 start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
                                 end_date: str = Query(..., description="End date (YYYY-MM-DD)"),):
    """
    Get BDE or MDE data for a station between two dates.
    """
    return sqlite.get_activities_from_to(station_id, data_type, start_date, end_date)

##############################
####filterd ## # Get filterd BDE or MDE data from start date to end date      
##############################
@app.get("/{data_type}/{station_id}/filterd")
async def get_activities_from_to(station_id: int,
                                 data_type: str = Query(..., description="bde, mde"), 
                                 start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
                                 end_date: str = Query(..., description="End date (YYYY-MM-DD)"),):
    """
    Get BDE or MDE data for a station between two dates.
    """
    data_array = sqlite.get_activities_from_to(station_id, data_type, start_date, end_date)
    data_dict = process_data( data_array[0] )
    return  data_dict

##############################
###### Get MDE or BDE data of current week         
##############################
@app.get("/{data_type}/{station_id}/current_week")
async def get_activities_current_week( data_type: str, station_id: int,):
    """
    Get BDE or MDE data for a station for the current week.
    """
    start_date, end_date = timer.get_week_start_today()
    return sqlite.get_activities_from_to(station_id, data_type, start_date, end_date)

##############################
###filterd### Get filterd MDE or BDE data of current week         
##############################
@app.get("/{data_type}/{station_id}/current_week")
async def get_activities_current_week( data_type: str, station_id: int,):
    """
    Get BDE or MDE data for a station for the current week.
    """
    start_date, end_date = timer.get_week_start_today()
    data_array = sqlite.get_activities_from_to(station_id, data_type, start_date, end_date)
    data_dict = process_data( data_array[0] )
    return  data_dict
##############################
###### Get MDE or BDE data of current month         
##############################
@app.get("/{data_type}/{station_id}/current_month")
async def get_activities_current_month(data_type: str, station_id: int,):
    """
    Get BDE or MDE data for a station for the current month.
    """
    start_date, end_date = timer.get_month_start_today()
    return sqlite.get_activities_from_to(station_id, data_type, start_date, end_date)

##############################
##filterd#### Get filterd MDE or BDE data of current month         
##############################
@app.get("/{data_type}/{station_id}/current_month/filterd")
async def get_activities_current_month(data_type: str, station_id: int,):
    """
    Get BDE or MDE data for a station for the current month.
    """
    start_date, end_date = timer.get_month_start_today()
    data_array = sqlite.get_activities_from_to(station_id, data_type, start_date, end_date)
    data_dict = process_data( data_array[0] )
    return  data_dict

##############################
###### Get MDE or BDE data of current year         
##############################
@app.get("/{data_type}/{station_id}/current_year")
async def get_activities_current_year(data_type: str, station_id: int,):
    """
    Get BDE or MDE data for a station for the current year.
    """
    start_date, end_date = timer.get_year_start_today()
     
    return sqlite.get_activities_from_to(station_id, data_type, start_date, end_date)
    
##############################
###filterd### Get filterd MDE or BDE data of current year         
##############################
@app.get("/{data_type}/{station_id}/current_year/filterd")
async def get_activities_current_year_filter(data_type: str, station_id: int,):
         start_date, end_date = timer.get_year_start_today()
         data_array =sqlite.get_activities_from_to(station_id, data_type, start_date, end_date)
         data_dict = process_data( data_array[0] )
         return  data_dict

##############################
###### # Get MDE or BDE data for the last n days       
##############################
@app.get("/{data_type}/{station_id}/last_n_days")
async def get_activities_last_n_days(data_type: str, station_id: int,
    last_n_days: int = Query(..., description="Number of days"),):
    start_date, end_date = timer.date_range(last_n_days)
    print('<<< start_date ',start_date,'<<< end_date',end_date)
    return sqlite.get_activities_from_to(station_id, data_type, start_date, end_date)

##############################
####filterd ## # Get fiterd MDE or BDE data for the last n days       
##############################
@app.get("/{data_type}/{station_id}/last_n_days/filterd")
async def get_activities_last_n_days(data_type: str, station_id: int,
    last_n_days: int = Query(..., description="Number of days"),):
    start_date, end_date = timer.date_range(last_n_days)
    print('<<< start_date ',start_date,'<<< end_date',end_date)
    data_array = sqlite.get_activities_from_to(station_id, data_type, start_date, end_date)
    data_dict = process_data( data_array[0] )
    return  data_dict
########################################################
# ##############       main       ######################
########################################################
if __name__ == '__main__':
    file_path = "response_mde_update.json"
    
    data_array = load_data_from_file(file_path)
    print(data_array)
    process_data(data_array)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
  #sqlite.get_activities_from_to('70', 'mde', '2022-05-28', '2023-03-24')
