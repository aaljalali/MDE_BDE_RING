from typing import Optional
from fastapi import FastAPI, Query
from pydantic import BaseModel
import sqlite
import timer
from datetime import date

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
    Machine_performance: Optional[str] = None
    Program_name: Optional[str] = None
    Tool_number: Optional[str] = None

    class Config:
        orm_mode = True

class OperationData(BaseModel):
    TS: str
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
###### # Get BDE or MDE data from start date to end date      
##############################
@app.get("/{data_type}")
async def get_activities_from_to(data_type: str = Query(..., description="bde, mde"), 
                                 start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
                                 end_date: str = Query(..., description="End date (YYYY-MM-DD)"),):
    """
    Get BDE or MDE data  between two dates.
    """
    return sqlite.get_activities_from_to(data_type, start_date, end_date)


##############################
###### Get MDE or BDE data of current week         
##############################
@app.get("/{data_type}/current_week")
async def get_activities_current_week( data_type: str,):
    """
    Get BDE or MDE data for the current week.
    """
    start_date, end_date = timer.get_week_start_today()
    return sqlite.get_activities_from_to(data_type, start_date, end_date)


##############################
###### Get MDE or BDE data of current month         
##############################
@app.get("/{data_type}/current_month")
async def get_activities_current_month(data_type: str,):
    """
    Get BDE or MDE data for the current month.
    """
    start_date, end_date = timer.get_month_start_today()
    return sqlite.get_activities_from_to(data_type, start_date, end_date)


##############################
###### Get MDE or BDE data of current year         
##############################
@app.get("/{data_type}/current_year")
async def get_activities_current_year(data_type: str,):
    """
    Get BDE or MDE data for the current year.
    """
    start_date, end_date = timer.get_year_start_today()
    return sqlite.get_activities_from_to(data_type, start_date, end_date)


##############################
###### # Get MDE or BDE data for the last n days       
##############################
@app.get("/{data_type}/last_n_days")
async def get_activities_last_n_days(data_type: str,
    last_n_days: int = Query(..., description="Number of days"),):
    """
    Get BDE or MDE data for the last n days.
    """
    start_date, end_date = timer.date_range(last_n_days)
    print('<<<<<<<<<<<<<<<<<<<<<<<< start_date ',start_date,' <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< end_date ',end_date)
    return sqlite.get_activities_from_to(data_type, start_date, end_date)


########################################################
# ##############       main       ######################
########################################################
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

