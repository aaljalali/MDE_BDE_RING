import sqlite3
from folder_operations import current_server_db_path, get_current_month, get_current_year
import json
import os
import sqlite3
from datetime import datetime
from http.client import HTTPException
import timer
 


# test data sets with sample data 
bde_test_data = {'TS': '2023-02-27 12:00:00',
             'Station_ID': 1,
             'RFID': '0001',
             'Order_number': 'ORD-123',
             'Part_number': 'PART-456',
             'Performance_ID': '5',
             'Duration_sec': 120}

mde_test_data = {'TS': '2023-02-27 12:00:00',
             'Station_ID': 1,
             'Machine_performance': '3',
             'Program_name': 'PROG-456',
             'Tool_number': '789'}



# create a connection to the database
def connect(db_name):
    """Connect to the specified database and create tables if they don't exist."""
    conn = sqlite3.connect(db_name)
    create_tables(conn)
    return conn

def create_tables(conn):
    # create tables to store the data

                
    conn.execute('''CREATE TABLE IF NOT EXISTS MDEData (
                     TS TEXT PRIMARY KEY,
                     Station_ID INTEGER NOT NULL,
                     Machine_performance TEXT,
                     Program_name TEXT,
                     Tool_number TEXT,
                     FOREIGN KEY (Station_ID) REFERENCES Station(ID)
                 )''')

    conn.execute('''CREATE TABLE IF NOT EXISTS BDEData (
                     TS TEXT PRIMARY KEY,
                     Station_ID INTEGER NOT NULL,
                     RFID INTEGER NOT NULL,
                     Order_number TEXT,
                     Part_number TEXT,
                     Performance_ID INTEGER NOT NULL,
                     Duration_sec INTEGER,
                     FOREIGN KEY (Station_ID) REFERENCES Station(ID),
                     FOREIGN KEY (RFID) REFERENCES PersonnelData (RFID),
                     FOREIGN KEY (Performance_ID) REFERENCES OperatorPerformance (ID)
                 )''')
    




# function to insert data into MDEData table
def add_mde_data_to_db(mde_data):
    db_name = current_server_db_path() + f"BDE_MDE_{get_current_month()}_{get_current_year()}"
    conn = connect(db_name)
    # get the data as a dictionary
    data = dict(mde_data)

    # create an SQL query to insert the data into the table
    query = '''INSERT INTO MDEData
               (TS, Station_ID, Machine_performance, Program_name, Tool_number)
               VALUES
               (?, ?, ?, ?, ?)'''

    # execute the query
    try:
        with conn:
            conn.execute(query, (data['TS'], data['Station_ID'], data.get('Machine_performance', None), 
                                 data.get('Program_name', None), data.get('Tool_number', None)))
    except :#sqlite3.IntegrityError:
        print("Data already exists in the database")

    conn.close()
    

    
##################################################    
# function to insert data into BDEData table
################################################## 
def add_bde_data_to_db(bde_data):
    db_name = current_server_db_path() + f"BDE_MDE_{get_current_month()}_{get_current_year()}"
    conn = connect(db_name)
    # get the data as a dictionary
    data = dict(bde_data)

    # create an SQL query to insert the data into the table
    query = '''INSERT INTO BDEData
               (TS, Station_ID, RFID, Order_number, Part_number, Performance_ID, Duration_sec)
               VALUES
               (?, ?, ?, ?, ?, ?, ?)'''
    

    # execute the query
    try:
        with conn:
            conn.execute(query, (data['TS'], data['Station_ID'], data['RFID'], data.get('Order_number', None), 
                                 data.get('Part_number', None), data['Performance_ID'], data.get('Duration_sec', None)))
    except :#sqlite3.IntegrityError:
        print("Data already exists in the database")
    # close the database connection
    conn.close()
    
    

#################################################
    ## delete lastinserteted bde or mde data
#################################################
def delete_last_data_from_db(var, station_id):
    if var == 'mde':
        table_name = 'MDEData'
    elif var == 'bde':
        table_name = 'BDEData'
    print(f'<<<<<< sqlite.delete_last_{table_name.lower()}_data_from_db() called!')
    db_name = current_server_db_path() + f"BDE_MDE_{get_current_month()}_{get_current_year()}"
    conn = connect(db_name)

    c = conn.cursor()

    # Select the last row in the table using the ROWID column
    c.execute(f'SELECT max(rowid) FROM {table_name} WHERE Station_ID = {station_id}')
    last_rowid = c.fetchone()[0]

    # Select the data in the last row
    c.execute(f'SELECT * FROM {table_name} WHERE rowid=?', (last_rowid,))
    deleted_data = c.fetchone()

    # Delete the last row using the ROWID
    c.execute(f'DELETE FROM {table_name} WHERE rowid=?', (last_rowid,))
    print(f'DELETE FROM {table_name} WHERE rowid=?', (last_rowid,))
    # Save changes and close the connection
    conn.commit()
    conn.close()

    # Return the deleted data
    return deleted_data


    
    


def get_activities_from_to(station_id, activity_type, start_date, end_date):
    """
    Function to retrieve activity data for a specific type of activity (bde or mde) within a given time range.
    :param activity_type: Type of activity (bde or mde)
    :param start_date: Start date
    :param end_date: End date
    :return: Dictionary of activities in JSON format
    """
    # Create an empty dictionary to store the JSON objects
    json_dict = {}

    # Check if the provided activity_type is either "bde" or "mde"
    if activity_type == 'bde':
        table_name = 'BDEData'
    elif activity_type == 'mde':
        table_name = 'MDEData'
    else:
        # Return an error message if the type is not "bde" or "mde"
        return {"error": f"Invalid activity_type: {activity_type}. Must be either 'bde' or 'mde'"}

    # List all the years and months between the given start_date and end_date
    years_months = timer.months_between_dates(start_date, end_date)

    for year, month in years_months:
        source_db_name = current_server_db_path() + f"BDE_MDE_{month}_{year}"
        
        if os.path.exists(source_db_name):
            # Check if the database response has been created
            
            # Try to establish a connection to the database
            try:
                # Connect to the database
                conn = sqlite3.connect(source_db_name)
                # Create a cursor
                c = conn.cursor()
                # Query the data from the table
                c.execute(f"SELECT * FROM {table_name} WHERE Station_ID = {station_id} AND TS BETWEEN '{start_date}' AND '{end_date}'")
                results = c.fetchall()
                
                # Get the column names from the cursor description
                column_names = [column[0] for column in c.description]
                
                # Convert the results to a list of dictionaries with column names as keys
                results_dict = [dict(zip(column_names, row)) for row in results]
                
                # Append the results to the json_dict
                #json_dict.update({f"{year}_{month}": results_dict})
                json_dict.update({f"{year}_{month}": results_dict})
                
            except Exception as e:
                raise HTTPException(status_code=500, detail="Failed to retrieve activity data")
            
            finally:
                conn.close()

 

    return json_dict

  
 


'''def  get_activities_from_to(station_id,activity_type, start_date, end_date):
    print('activity_type ',activity_type)
    """
    Funktion um Aktivitätsdaten für den Zeitraum zwischen start_date und end_date für einen bestimmten Typ von Aktivität (bde oder mde) zu erhalten.
    :param activity_type: Typ der Aktivität (bde oder mde)
    :param start_date: Anfangsdatum
    :param end_date: Enddatum
    :return: Liste von Aktivitäten im JSON-Format
    """
    # create an empty list to store the JSON objects
    json_list = []
    # Überprüfen, ob der übergebene Aktivitätstyp entweder bde oder mde ist
    if activity_type == 'bde':
        print('du willst bde daten haben')
        table_name = 'BDEData'
    
    elif activity_type == 'mde':
        print('du willst mde daten haben')
        table_name = 'MDEData'
    else:
        # Fehlermeldung ausgeben, wenn der Typ nicht bde oder mde ist
        print(f"Eingabe muss entweder bde oder mde sein deine Eingbe war : {activity_type}")
        return -1
    
    # Liste aller Jahre und Monate zwischen den Daten berechnen
    years_months = timer.months_between_dates(start_date, end_date)
    print('<<<<<<<<<<<years_months <<<',years_months)
    paths = []
    for year, month in years_months:
        source_db_name = current_server_db_path() + f"BDE_MDE_{month}_{year}"
        print('>>>>>>>>>>>>>>>>>> source_db_name', source_db_name)
        if os.path.exists(source_db_name):
          print('Quelltabelle gefunden', source_db_name)
            # Überprüfen, ob das Datenbank-Response erstellt wurde
        
             # Versuchen, eine Verbindung zur Datenbank herzustellen
          try:
                # Verbindung zur Datenbank herstellen
                conn = sqlite3.connect(source_db_name)
                # Cursor erstellen
                c = conn.cursor()
                # Daten aus der Tabelle abfragen
                #c.execute(f"SELECT * FROM {table_name} Where Station_ID = {station_id}")
                c.execute(f"SELECT * FROM {table_name} WHERE Station_ID = {station_id} AND TS BETWEEN '{start_date}' AND '{end_date}'")
                print(f"SELECT * FROM {table_name} WHERE Station_ID = {station_id} AND TS BETWEEN '{start_date}' AND '{end_date}'")
                # Ergebnisse abrufen
                results = c.fetchall()
                # Convert the results to a JSON string
                response_json = json.dumps(results)
                json_list.append(json.loads(response_json))
                #print('<<<<<<<<<<<<<<',response_json)



 

          except Exception as e:
                raise HTTPException(status_code=500, detail="Failed to retrieve activity data")

          finally:
                conn.close()
                print('json_list>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', json_list)
                # Write the JSON string to a file
               # with open(f"response.json", 'w') as f:
                   # f.write(str(json_list))
    return json_list'''
    


