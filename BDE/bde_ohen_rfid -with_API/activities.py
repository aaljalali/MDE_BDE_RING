import sqlite
from Barcode import *
import folders
from timer import start_timer, stop_timer, calculate_duration, time
import api_client
import psutil
import os
import signal
from global_settings import  GlobalSettings

#stop_running current python script
def kill_process():
    # stop curent python scripr
    pid = os.getpid()
    parent = psutil.Process(pid)
    children = parent.children(recursive=True)
    for child in children:
        child.terminate()
    parent.terminate()

def close_bde_app():
    GlobalSettings.registed_MAid != 0
    try:
        untrack_machine_activity()
    except:
        pass

    try:
        untrack_operator_activity()
    except:
        pass

    kill_process()
########################################################################################################
#                          Maschine ud betriebsdaten localspeichern und an den server posten
########################################################################################################
def save_post_machine_data():
    # Sende die Daten an die API
    api_client.post_mde_data()
    # Erstelle und aktualisiere die Datenbank mit Maschinenaktivitäten
    sqlite.create_machine_activity_table()
    sqlite.insert_data_to_machine_activities()

def save_post_operator_data():
    # Senden Sie die BDE-Daten an die API
    api_client.post_bde_data()
    # Erstellen Sie eine Tabelle für die Operatoraktivitäten und fügen Sie die Daten hinzu
    sqlite.create_operator_activity_table()
    sqlite.insert_data_to_operator_activities()

########################################################################################################
#                           Aktualisiert die Maschinenaktivität
########################################################################################################
def update_machine_activity():
    GlobalSettings.registered_machine_activity_id = GlobalSettings.scanned_machine_activity_id
    GlobalSettings.registered_machine_activity_name, GlobalSettings.registered_machine_activity_name_short_form = decode_machine_status(
        GlobalSettings.registered_machine_activity_id)
    # hier you can do it like the update_operator_activity if you have maschine activity as ID
    GlobalSettings.scanned_machine_activity_id = 0


########################################################################################################
#                           Setzt die Maschinenaktivität zurück
########################################################################################################
def reset_machine_activity():
    GlobalSettings.registered_machine_activity_id = GlobalSettings.scanned_machine_activity_id = 0
    GlobalSettings.registered_machine_activity_name = 'Maschine Leistungsart scannen!'
    GlobalSettings.formatted_machine_activity_start_time = '0000 00 00 00:00:00'


########################################################################################################
#                Aktualisiert die Operatoraktivität (Mensch leistungsarten)
########################################################################################################
def update_operator_activity():
    GlobalSettings.registered_operator_activity_id = GlobalSettings.scanned_operator_activity_id
    GlobalSettings.registered_operator_activity_name = sqlite.get_leistungsart_name(
        GlobalSettings.registered_operator_activity_id)
    GlobalSettings.scanned_operator_activity_id = 0


########################################################################################################
#                               Setzt die Operatoraktivität zurück
########################################################################################################
def reset_operator_activity():
    GlobalSettings.registered_operator_activity_id = GlobalSettings.scanned_operator_activity_id = 0
    GlobalSettings.registered_operator_activity_name = 'Leistungsart scannen!'
    GlobalSettings.formatted_operator_activity_start_time = '0000 00 00 00:00:00'

########################################################################################################
#                          Rest Bauteil Nr.
########################################################################################################
def reset_auftrag_bautei():
    GlobalSettings.registered_bauteil_nr = GlobalSettings.scanned_bauteil_nr = 0
    GlobalSettings.registered_auftrag_nr = GlobalSettings.scanned_auftrag_nr = 0
    GlobalSettings.Bauteil_lbl_bg_color ='ORANGE'
    GlobalSettings.Auftrag_nr_bg_color = 'ORANGE'
########################################################################################################
#                           Aktualisiert den Auftrag und das Bauteil
########################################################################################################
def update_auftrag_bautei():
    GlobalSettings.registered_auftrag_nr = GlobalSettings.scanned_auftrag_nr
    GlobalSettings.registered_bauteil_nr = GlobalSettings.scanned_bauteil_nr
    if GlobalSettings.registered_bauteil_nr != 0 and GlobalSettings.registered_bauteil_nr is not None:
       GlobalSettings.Bauteil_lbl_bg_color = 'Green'
       GlobalSettings.Auftrag_nr_bg_color = 'Green'



########################################################################################################
#                                  Srat die Maschinenaktivität verfolgen
########################################################################################################
def track_machine_activity():
 ##   if GlobalSettings.registered_bauteil_nr != 0 and GlobalSettings.registered_auftrag_nr != 0:

        # Starte den Timer, um die Dauer der Maschinenaktivität zu messen
        print('starte Verfolgung des Maschinenzustands id = ', GlobalSettings.scanned_machine_activity_id)
        GlobalSettings.formatted_machine_activity_start_time, GlobalSettings.machine_activity_start_time_unix = start_timer()
        print('formatted_machine_activity_start_time = ', GlobalSettings.formatted_machine_activity_start_time)

        # Aktualisiere die Maschinenaktivität
        update_machine_activity()

        # Ändere die Hintergrundfarbe des Maschinenaktivitätslabels auf Grün
        GlobalSettings.machine_activity_lbl_bg_color = 'GREEN'

    # Wenn die Bauteil- oder Auftragsnummer nicht registriert sind
  #  else:
     #    print('... Bauteil- oder Auftrag-Nr. wurde nicht gescannt!')
         #GlobalSettings.Bauteil_lbl_bg_color = 'red'



def cancel_track_machine_activity():
    # brich die Verfolgung der Maschinenaktivität a
    print('  Verfolgung des Maschinenzustands Nr.', GlobalSettings.registered_machine_activity_id ,'abbrechen')
    GlobalSettings.machine_activity_end_time_unix = stop_timer()
    GlobalSettings.machine_activity_start_time_unix = None

    # Setze die Variablen für Maschinenaktivität zurück
    reset_machine_activity()
    GlobalSettings.machine_activity_lbl_bg_color = 'ORANGE'
    GlobalSettings.Bauteil_lbl_bg_color = 'ORANGE'



def delete_last_machine_activity():
    api_client.delete_last_mde()
    print('Functio  delete_last_machine_activity() called!')
    try:
        deleted_data = sqlite.delete_last_row_from_machine_activities()
        print('deleted data from local db >>',deleted_data)
    except:
        pass
########################################################################################################
#                                  Stopt die Maschinenaktivität verfolgen
########################################################################################################
def untrack_machine_activity():
    # Aktualisiere den Bauteil- und Auftragsstatus
   # update_auftrag_bautei()
    # Überprüfe, ob eine Bauteil- und Auftragsnummer gescannt wurde
    if GlobalSettings.registered_bauteil_nr != 0 and GlobalSettings.registered_auftrag_nr != 0:
        # Beende die Verfolgung der Maschinenaktivität
        print('stoppe Verfolgung des Maschinenzustands Nr.', GlobalSettings.registered_machine_activity_id)
        GlobalSettings.machine_activity_end_time_unix = stop_timer()
        GlobalSettings.machine_activity_duration_sec = calculate_duration(
            GlobalSettings.machine_activity_start_time_unix,
            GlobalSettings.machine_activity_end_time_unix)
        GlobalSettings.machine_activity_start_time_unix = None

        save_post_machine_data()

        # Setze die Variablen für Maschinenaktivität zurück
        reset_machine_activity()
        GlobalSettings.machine_activity_lbl_bg_color = 'ORANGE'
        GlobalSettings.Bauteil_lbl_bg_color = 'ORANGE'
    else:
        # Wenn keine Bauteil- oder Auftragsnummer gescannt wurde, ändere die Hintergrundfarbe des Bauteil-Labels auf Rot
        print('Bauteil- oder Auftrag-Nr. wurde nicht gescannt!')
        GlobalSettings.Bauteil_lbl_bg_color = 'red'


########################################################################################################
#                             Start Mensch Leistungsart Verfolgung 
########################################################################################################
def track_operator_activity():
    #if GlobalSettings.registered_bauteil_nr != 0 and GlobalSettings.registered_auftrag_nr != 0:
    #    # Ordner für aktuelle Maschinendaten und Operator-Daten erstellen
    #    GlobalSettings.current_machine_data_folder, GlobalSettings.current_operator_data_folder = folders.create_folders()
        # Starte den Timer, um die Dauer der Operator-Aktivität zu messen
        print('starte Verfolgung der Aktivität Nr.', GlobalSettings.scanned_operator_activity_id)
        GlobalSettings.formatted_operator_activity_start_time, GlobalSettings.operator_activity_start_time_unix = start_timer()
        print('formatted_operator_activity_start_time = ', GlobalSettings.formatted_operator_activity_start_time)

        # Aktualisiere die Operator-Aktivität
        update_operator_activity()

        # Ändere die Hintergrundfarbe des Operator-Aktivitätslabels auf grün
        GlobalSettings.operator_activity_lbl_bg_color = 'GREEN'
    # Wenn die Bauteil- oder Auftragsnummer nicht registriert sind
   # else:
     #    print('... Bauteil- oder Auftrag-Nr. wurde nicht gescannt!')
      #   GlobalSettings.Bauteil_lbl_bg_color = 'red'


def cancel_track_operator_activity():
    print('cancle tracking the activity Nr.', GlobalSettings.registered_operator_activity_id)
    GlobalSettings.operator_activity_end_time_unix = stop_timer()
    GlobalSettings.operator_activity_start_time_unix = None
    # Setzen Sie die Variablen für die Operatoraktivitäten zurück und ändern Sie die Hintergrundfarbe des Labels
    reset_operator_activity()
    GlobalSettings.operator_activity_lbl_bg_color = 'ORANGE'

def delete_last_operator_activity():
    api_client.delete_last_bde()
    print('Functio  delete_last_operator_activity() called!')
    try:
        deleted_data = sqlite.delete_last_row_from_operator_activities()
        print('deleted data from local db >>',deleted_data)
    except:
        pass
#
########################################################################################################
#                             Stop Mensch Leistungsart Verfolgung 
########################################################################################################
def untrack_operator_activity():
    # Aktualisieren Sie den Auftrag und das Bauteil
    # Wenn die Bauteil- und Auftragsnummer registriert sind
    #if GlobalSettings.registered_bauteil_nr != 0 and GlobalSettings.registered_auftrag_nr != 0:
        # Stoppen Sie das Verfolgen der Tätigkeit des Operators mit der entsprechenden ID
        print('stop trackinga the activity Nr.', GlobalSettings.registered_operator_activity_id)
        GlobalSettings.operator_activity_end_time_unix = stop_timer()
        GlobalSettings.operator_activity_duration_sec = calculate_duration(
            GlobalSettings.operator_activity_start_time_unix,
            GlobalSettings.operator_activity_end_time_unix)
        GlobalSettings.operator_activity_start_time_unix = None

        save_post_operator_data()

        # Setzen Sie die Variablen für die Operatoraktivitäten zurück und ändern Sie die Hintergrundfarbe des Labels
        reset_operator_activity()
        GlobalSettings.operator_activity_lbl_bg_color = 'ORANGE'

    # Wenn die Bauteil- oder Auftragsnummer nicht registriert sind
    #else:
      #  print('... Bauteil- oder Auftrag-Nr. wurde nicht gescannt!')
      #  GlobalSettings.Bauteil_lbl_bg_color = 'red'


########################################################################################################
#                             Verfolgung von Maschinenaktivitäten
########################################################################################################
def bde_machine_activties():
    if GlobalSettings.registered_machine_activity_id == GlobalSettings.scanned_machine_activity_id == 0:
        pass

    elif GlobalSettings.registered_machine_activity_id == 0 and int(GlobalSettings.scanned_machine_activity_id) > 0:
        # Wenn die Maschinenaktivität nicht registriert wurde, aber gescannt wurde, beginne mit dem Tracking
        track_machine_activity()

    elif GlobalSettings.registered_machine_activity_id == int(GlobalSettings.scanned_machine_activity_id) > 0:
        # Wenn die Maschinenaktivität bereits registriert und gescannt wurde, stoppe das Tracking
        untrack_machine_activity()
    elif int(GlobalSettings.registered_machine_activity_id) > 0 and GlobalSettings.scanned_machine_activity_id == -1:
        # Wenn die Maschinenaktivität bereits registriert und -1  gescannt  wurde, das Tracking abbrechen
        cancel_track_machine_activity()
    elif GlobalSettings.registered_machine_activity_id == 0 and GlobalSettings.scanned_machine_activity_id == -1:
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>MDE Rückgang')
        GlobalSettings.scanned_machine_activity_id =0
        delete_last_machine_activity()
########################################################################################################
#                             Verfolgung von Mensch Leistungsart
########################################################################################################
def bde_operator_activites():
    if GlobalSettings.registered_operator_activity_id == GlobalSettings.scanned_operator_activity_id == 0:
        pass

    elif GlobalSettings.registered_operator_activity_id == 0 and GlobalSettings.scanned_operator_activity_id != GlobalSettings.registered_operator_activity_id and GlobalSettings.scanned_operator_activity_id != -1:
        # Wenn die Operatoraktivität nicht registriert wurde, aber gescannt wurde, beginne mit dem Tracking
        track_operator_activity()
        print('123>>> ')

    elif GlobalSettings.registered_operator_activity_id == GlobalSettings.scanned_operator_activity_id != 0:
        # Wenn die Operatoraktivität bereits registriert und gescannt wurde, stoppe das Tracking
        untrack_operator_activity()

    elif int(GlobalSettings.registered_operator_activity_id ) > 0 and GlobalSettings.scanned_operator_activity_id == -1:
        # Wenn die Operatoraktivität bereits registriert und -1  gescannt  wurde, das Tracking abbrechen
        cancel_track_operator_activity()

    elif GlobalSettings.registered_operator_activity_id == 0 and GlobalSettings.scanned_operator_activity_id == -1:
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> BDE Rückgang')
        GlobalSettings.scanned_operator_activity_id = 0
        delete_last_operator_activity()