import json
import os
import sqlite3
from datetime import datetime
from http.client import HTTPException

import timer
from global_settings import GlobalSettings

def delete_db_file_if_exists(db_file):
    if os.path.exists(db_file):
        os.remove(db_file)

def copy_sqlite_db(src_path, src_table, dest_path,  dest_table):
    delete_db_file_if_exists(dest_path)
    # Connect to the source database
    src_conn = sqlite3.connect(src_path)
    src_cursor = src_conn.cursor()

    # Connect to the destination database
    dest_conn = sqlite3.connect(dest_path)
    dest_cursor = dest_conn.cursor()

    # Retrieve the CREATE TABLE statement for the source table
    src_cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{src_table}'")
    create_table_statement = src_cursor.fetchone()[0]

    # Replace the table name in the CREATE TABLE statement
    create_table_statement = create_table_statement.replace(src_table, dest_table)

    # Create the destination table
    dest_cursor.execute(create_table_statement)

    # Commit the changes to the destination database
    dest_conn.commit()

    # Close the connections to both databases
    src_conn.close()
    dest_conn.close()


def copy_table_data(src_db_file, src_table_name, dest_db_file, dest_table_name):
    src_conn = sqlite3.connect(src_db_file)
    src_cursor = src_conn.cursor()

    dest_conn = sqlite3.connect(dest_db_file)
    dest_cursor = dest_conn.cursor()

    query = "SELECT * FROM {}".format(src_table_name)
    src_cursor.execute(query)
    rows = src_cursor.fetchall()

    for row in rows:
        dest_cursor.execute("INSERT INTO {} VALUES ({})".format(dest_table_name, ",".join(['?'] * len(row))), row)

    dest_conn.commit()

    src_conn.close()
    dest_conn.close()


def get_activity_from_to(activity_type, start_date, end_date):
    """
    Funktion um Aktivitätsdaten für den Zeitraum zwischen start_date und end_date für einen bestimmten Typ von Aktivität (bde oder mde) zu erhalten.
    :param activity_type: Typ der Aktivität (bde oder mde)
    :param start_date: Anfangsdatum
    :param end_date: Enddatum
    :return: Liste von Aktivitäten im JSON-Format
    """
    # Boolean-Variable, um zu überprüfen, ob eine Datenbankdatei für das Ergebnis bereits erstellt wurde
    response_db_created = False

    # Überprüfen, ob der übergebene Aktivitätstyp entweder bde oder mde ist
    if activity_type == 'bde':
        db_folder = GlobalSettings.db_bde_folder_name
    elif activity_type == 'mde':
        db_folder = GlobalSettings.db_mde_folder_name
    else:
        # Fehlermeldung ausgeben, wenn der Typ nicht bde oder mde ist
        print('Eingabe muss entweder bde oder mde sein')
        return -1

    # Überprüfen, ob eine vorhandene Datenbankdatei für das Ergebnis gelöscht werden muss
    delete_db_file_if_exists(f"{GlobalSettings.bde_path}//DB//{db_folder}//requsted")

    # Liste aller Jahre und Monate zwischen den Daten berechnen
    years_months = timer.months_between_dates(start_date, end_date)
    paths = []
    for year, month in years_months:
        print(year, month)
        if activity_type == 'bde':
            source_tbl_name = f"operator_{month}_{year}"
            source_db_name = "operator_activities.db"
        elif activity_type == 'mde':
            source_tbl_name = f"machine_{year}_{month}"
            source_db_name = "machine_activities.db"

        source_db_file_path = f"{GlobalSettings.bde_path}//DB//{db_folder}//{year}//{month}//{source_db_name}"
        print('source_db_file_path', source_db_file_path)
        if os.path.exists(source_db_file_path):
            print('Quelltabelle gefunden', source_db_file_path)
            # Überprüfen, ob das Datenbank-Response erstellt wurde
            if not response_db_created:
                # Setzen Sie response_db_created auf True, wenn es nicht erstellt wurde
                response_db_created = True
                # Kopieren Sie die Quelldatenbank in die Zieldatenbank
                copy_sqlite_db(source_db_file_path, source_tbl_name,
                               f"{GlobalSettings.bde_path}//DB/{db_folder}//requsted.db", 'requst_tbl')
                # Kopieren Sie die Daten aus der Quelltabelle in die Zieltabelle
                copy_table_data(source_db_file_path, source_tbl_name,
                                f"{GlobalSettings.bde_path}//DB/{db_folder}//requsted.db", 'requst_tbl')

            # Versuchen, eine Verbindung zur Datenbank herzustellen
            try:
                # Verbindung zur Datenbank herstellen
                conn = sqlite3.connect(f"{GlobalSettings.bde_path}//DB/{db_folder}//requsted.db")
                # Cursor erstellen
                c = conn.cursor()
                # Daten aus der Tabelle abfragen
                c.execute("SELECT * FROM requst_tbl")
                # Ergebnisse abrufen
                results = c.fetchall()
                # Rückgabewert als JSON-String
                return json.dumps(results)


            except Exception as e:
                raise HTTPException(status_code=500, detail="Failed to retrieve activity data")

            finally:
                conn.close()