import sqlite3
from datetime import datetime
from global_settings import GlobalSettings
import json
import tkinter.messagebox as messagebox
import timer
import folders
import os
####################################################################################
##########################################   BDE    ############################### 
####################################################################################
def create_operator_activity_table():
    GlobalSettings.current_operator_activities_path = f"{GlobalSettings.current_operator_data_folder}/operator_activities.db"

    # Get the current month and year
    now = datetime.now()
    month = now.strftime("%B")
    year = now.year
    GlobalSettings.current_operator_activity_table_name = table_name = f"operator_{month}_{year}"

    # Connect to the database (or create it if it doesn't exist)
    conn = sqlite3.connect(GlobalSettings.current_operator_activities_path)
    c = conn.cursor()

    c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    if c.fetchone() is None:
        # Create the table with the specified columns and primary key
        c.execute(
            f"CREATE TABLE {table_name} (TS TEXT PRIMARY KEY,RFID "
            f"INTEGER NOT NULL,"
            f"Order_number INTEGER NOT NULL, Part_number INTEGER NOT NULL, Performance_ID INTEGER NOT NULL , Duration_sec  INTEGER NOT "
            f"NULL)")
        conn.commit()
    # Close the connection
    conn.close()


def insert_data_to_operator_activities():
    # Get the current month and year
    now = datetime.now()
    month = now.strftime("%B")
    year = now.year

    # Create the table name
    table_name = GlobalSettings.current_operator_activity_table_name

    # Connect to the database
    conn = sqlite3.connect(GlobalSettings.current_operator_activities_path)
    c = conn.cursor()

    # Insert the data into the table
    c.execute(f"INSERT INTO {table_name} (TS, RFID, Order_number, Part_number, "
              f"Performance_ID, Duration_sec) VALUES (?,?,?,?,?,?)",
              (GlobalSettings.formatted_operator_activity_start_time,
               GlobalSettings.registed_MAid, GlobalSettings.registered_auftrag_nr,
               GlobalSettings.registered_bauteil_nr, GlobalSettings.registered_operator_activity_id,
               GlobalSettings.operator_activity_duration_sec))

    # Save changes and close the connection
    conn.commit()
    conn.close()


def delete_last_row_from_operator_activities():
    # Create the table name
    table_name = GlobalSettings.current_operator_activity_table_name

    # Connect to the database
    conn = sqlite3.connect(GlobalSettings.current_operator_activities_path)
    c = conn.cursor()

    # Select the last row in the table using the ROWID column
    c.execute(f'SELECT max(rowid) FROM {table_name}')
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



def operator_performance_id_exists(operator_performance_id):
    with sqlite3.connect(GlobalSettings.config_db_name) as con:
        cur = con.cursor()
        cur.execute("SELECT 1 FROM operator_performance_type  WHERE ID = ?", (operator_performance_id,))
        result = cur.fetchone()
        return True if result else False


def get_leistungsart_name(ID):
    with sqlite3.connect(GlobalSettings.config_db_name) as conn:
        c = conn.cursor()

        # Execute a SELECT statement to retrieve the Leistungart
        c.execute("SELECT Performance  FROM operator_performance_type  WHERE ID = ?", (ID,))

        # Fetch the result
        leistungsart = c.fetchone()[0]

    return leistungsart




####################################################################################
##########################################   MDE    ############################### 
####################################################################################
def create_machine_activity_table():
    GlobalSettings.current_machine_activities_path = f"{GlobalSettings.current_machine_data_folder}" \
                                                     f"/machine_activities.db"
    # Get the current month and year
    now = datetime.now()
    month = now.strftime("%B")
    year = now.year
    GlobalSettings.current_machine_activity_table_name = table_name = f"machine_{month}_{year}"

    # Connect to the database (or create it if it doesn't exist)
    conn = sqlite3.connect(GlobalSettings.current_machine_activities_path)
    c = conn.cursor()

    c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    if c.fetchone() is None:
        # Create the table with the specified columns and primary key
        c.execute(
            f"CREATE TABLE {table_name} (TS TEXT PRIMARY KEY,"
            f"Order_number INTEGER NOT NULL, Part_number INTEGER NOT NULL, MaschinePerformance_ID INTEGER NOT NULL ,"
            f" Duration_sec  INTEGER NOT NULL)")
        conn.commit()
    # Close the connection
    conn.close()


def insert_data_to_machine_activities():
    # Get the current month and year
    now = datetime.now()
    month = now.strftime("%B")
    year = now.year

    # Create the table name
    table_name = GlobalSettings.current_machine_activity_table_name

    # Connect to the database
    conn = sqlite3.connect(GlobalSettings.current_machine_activities_path)
    c = conn.cursor()

    # Insert the data into the table
    c.execute(f"INSERT INTO {table_name} (TS, Order_number, Part_number, "
              f"MaschinePerformance_ID, Duration_sec) VALUES (?,?,?,?,?)",
              (GlobalSettings.formatted_machine_activity_start_time,
               GlobalSettings.registered_auftrag_nr,
               GlobalSettings.registered_tool_nr, GlobalSettings.registered_machine_activity_name_short_form,
               GlobalSettings.machine_activity_duration_sec))

    # Save changes and close the connection
    conn.commit()
    conn.close()



def delete_last_row_from_machine_activities():
    # Create the table name
    table_name = GlobalSettings.current_machine_activity_table_name

    # Connect to the database
    conn = sqlite3.connect(GlobalSettings.current_machine_activities_path)
    c = conn.cursor()

    # Select the last row in the table using the ROWID column
    c.execute(f'SELECT max(rowid) FROM {table_name}')
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


####################################################################################
#################################    user data   ############################### 
####################################################################################

def insert_usr_data(RFID, Avatar_id, First_name, Last_name, Role, Telephone_number_1, Telephone_number_2, Work_email,
                    Is_admin):
    with sqlite3.connect(GlobalSettings.config_db_name) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO PersonnelData  (
                RFID, Avatar_id, First_name , Last_name , Role, Telephone_number_1, Telephone_number_2, Work_email , Is_admin
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
        RFID, Avatar_id, First_name, Last_name, Role, Telephone_number_1, Telephone_number_2, Work_email, Is_admin))
        conn.commit()


def delete_user(RFID):
    with sqlite3.connect(GlobalSettings.config_db_name) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM PersonnelData  WHERE RFID = ?", (RFID,))
        conn.commit()


def rfid_exists(rfid):
    with sqlite3.connect(GlobalSettings.config_db_name) as con:
        cur = con.cursor()
        cur.execute("SELECT 1 FROM PersonnelData  WHERE RFID = ?", (rfid,))
        result = cur.fetchone()
        return True if result else False


def get_unused_avatar_names_and_ids():
    results = []
    with sqlite3.connect(GlobalSettings.config_db_name) as conn:
        c = conn.cursor()
        c.execute('''SELECT  Avatars.ID, Avatars.Name
                    FROM Avatars
                    LEFT JOIN PersonnelData  ON Avatars.ID = PersonnelData .Avatar_id
                    WHERE PersonnelData .Avatar_id IS NULL''')
        tuples = c.fetchall()
        results = [list(t) for t in tuples]
    print('results', results)
    return results


## function to return name to be displied as user name
def get_name(rfid, option):
    with sqlite3.connect(GlobalSettings.config_db_name) as conn:
         
        cursor = conn.cursor()

        cursor.execute("SELECT Avatar_id FROM PersonnelData  WHERE RFID=?", (rfid,))
        avatar_id = cursor.fetchone()[0]

        cursor.execute(
            "SELECT Name, First_name , Last_name  FROM Avatars JOIN PersonnelData  ON Avatars.ID = "
            "PersonnelData .Avatar_id WHERE PersonnelData .RFID=?",
            (rfid,))
        name, First_name, Last_name = cursor.fetchone()

        if option == 1:
            return name
        elif option == 2:
            if First_name or Last_name:
                return f"{First_name} {Last_name}"
            else:
                return name
        else:
            return name


def get_img_path(rfid):
    try:
        # Connect to the database
        con = sqlite3.connect(GlobalSettings.config_db_name)
        cur = con.cursor()

        # Query the 'Avatars' table for the 'img_path' where the 'RFID' in the 'PersonnelData ' table matches the provided RFID
        cur.execute(
            "SELECT Avatars.img_path FROM Avatars JOIN PersonnelData  ON Avatars.ID = PersonnelData .Avatar_id WHERE PersonnelData .RFID = ?",
            (rfid,))

        # Fetch the result
        result = cur.fetchone()

        # Close the cursor and connection
        cur.close()
        con.close()

        # Return the result
        return result[0]
    except:
        return GlobalSettings.default_img_path


def is_RFID_in_PersonnelData(db_name, RFID):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PersonnelData  WHERE RFID=?", (RFID,))
    result = cursor.fetchall()
    conn.close()

    if len(result) > 0:
        message = "Die RFID-Karte ist im System vorhanden mit den folgenden Daten:\n"
        message += "RFID: " + str(result[0][0]) + "\n"
        message += "Avatar ID: " + str(result[0][1]) + "\n"
        message += "First_name : " + result[0][2] + "\n"
        message += "Last_name : " + result[0][3] + "\n"
        message += "Role: " + result[0][4] + "\n"
        message += "Telephone_number_1: " + result[0][5] + "\n"
        message += "Telephone_number_2: " + result[0][6] + "\n"
        message += "Work_email : " + result[0][7] + "\n"
        message += "Is_admin: " + result[0][8]
        messagebox.showinfo("RFID Info", message)
        return True

    else:
        messagebox.showinfo("Ok ", "Done!")
    return False




######################################################### 
########################## API ##########################
#########################################################
def  get_activities_from_to(activity_type, start_date, end_date):
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
            table_name_ = 'operator'
            source_db_path = 'DB/Erfasste_Betriebsdaten/'
            source_db_name_ ='operator_activities.db'
        elif activity_type == 'mde':
            print('du willst mde daten haben')
            table_name_ = 'machine'
            source_db_path = 'DB/Erfasste_Maschindaten/'
            source_db_name_ ='machine_activities.db'
        else:
            # Fehlermeldung ausgeben, wenn der Typ nicht bde oder mde ist
            print(f"Eingabe muss entweder bde oder mde sein deine Eingbe war : {activity_type}")
            return -1
        
        # Liste aller Jahre und Monate zwischen den Daten berechnen
        years_months = timer.months_between_dates(start_date, end_date)
        print(years_months)
        paths = []
        for year, month in years_months:
            source_db_name = source_db_path+ f"{year}/{month}/"+ source_db_name_
            table_name = table_name_ +f"_{month}_{year}"
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
                    c.execute(f"SELECT * FROM {table_name} WHERE TS BETWEEN '{start_date}' AND '{end_date}'")
                    print(f"SELECT * FROM {table_name} WHERE  TS BETWEEN '{start_date}' AND '{end_date}'")
                    # Ergebnisse abrufen
                    results = c.fetchall()
                    # Convert the results to a JSON string
                    response_json = json.dumps(results)
                    json_list.append(json.loads(response_json))
                



       

                except Exception as e:
                    raise HTTPException(status_code=500, detail="Failed to retrieve activity data")

                finally:
                    conn.close()
                    #print('json_list>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', json_list)
                    # Write the JSON string to a file
                   # with open(f"response.json", 'w') as f:
                      #  f.write(str(json_list))
        return json_list







########################################################
# ##############       main       ######################
########################################################
if __name__ == '__main__':
    
    print(get_activities_from_to('mde', '2022-05-28', '2023-03-24'))




