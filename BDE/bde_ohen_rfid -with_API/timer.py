import time
from datetime import datetime, timedelta
import calendar
import datetime as dt
#################################################
###### set datum und uhrzeit variable
#################################################
def get_ts():
     return (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
  
def get_current_month():
    return datetime.now().strftime("%B")
    

def get_current_year():
    return( datetime.now().strftime("%Y"))

def start_timer():
    # Start the timer
    print('start time ', time.time())
    formated_start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    unix_start_time = time.time()
    return formated_start_time, unix_start_time


def stop_timer():
    # Stop the timer
    print('stop time ', time.time())
    end_time_unix = time.time()
    return end_time_unix


def calculate_duration(start_time_unix, end_time_unix):
    # Calculate the elapsed time between start and stop timer
    return int(end_time_unix - start_time_unix)



def extract_date_info(start_time):
    date = datetime.strptime(start_time, "%Y-%m-%d")
    year = date.year
    month_name = calendar.month_name[date.month]
    day = date.day
    return year, month_name, day


from datetime import datetime

def months_between_dates(start_datum, end_datum):
    # Parsen des Start- und Enddatums aus den übergebenen strings
    start_date = datetime.strptime(start_datum, "%Y-%m-%d")
    end_date = datetime.strptime(end_datum, "%Y-%m-%d")

    # Initialisieren einer Liste, um die Jahr-Monats-Informationen zu speichern
    monate = []
    current_date = start_date
    # Schleife über die Monate zwischen Start- und Enddatum
    while current_date <= end_date:
        # Extrahieren des Jahres und Monatsnamens aus dem aktuellen Datum
        jahr = current_date.strftime("%Y")
        monats_name = current_date.strftime("%B")
        # Hinzufügen des Jahr-Monats-Paares zur Liste
        monate.append((jahr, monats_name))
        # Überprüfen, ob der aktuelle Monat Dezember ist
        if current_date.month == 12:
            # Wenn ja, dann das Jahr um 1 erhöhen und den Monat auf Januar setzen
            current_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            # Wenn nein, dann den Monat um 1 erhöhen
            current_date = current_date.replace(month=current_date.month + 1)

    # Wenn das Enddatum nicht der letzte Tag des Monats ist, füge das Enddatum hinzu
    if end_date.day != 1:
        monate.append((end_date.strftime("%Y"), end_date.strftime("%B")))

    # Rückgabe der Liste mit Jahr-Monats-Informationen
    return monate



def date_range(var):
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=var)
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        return start_date_str, end_date_str
  
  
def get_week_start_today():
         # Heutiges Datum
        today = dt.date.today()
        # Erster Tag dieser Woche
        week_start = today - dt.timedelta(days=today.weekday())
        
        return week_start.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")
    
def get_month_start_today():
    # Heutiges Datum
    today = dt.date.today()
    # Erster Tag dieses Monats
    month_start = today.replace(day=1)

    return month_start.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")

def get_year_start_today():
    # Heutiges Datum
    today = dt.date.today()
    # Erster Tag dieses Jahres
    year_start = today.replace(month=1, day=1)
  
    return year_start.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")

#print(get_year_start_today())
## for test
#start_datum = "2022-01-01"
#end_datum = "2022-12-31"
start_datum = '2022-05-28'
end_datum = '2023-03-1'
monate = months_between_dates( start_datum, end_datum)
print(monate)