import sqlite
from GUI_Add_usr import *
import global_settings
from global_settings import GlobalSettings

def add_user_but_fun(add_user_obj, RFID, Avatar_id, VorName, NachName, Rolle, TelefonNr1, TelefonNr2, EmailArbeit,
                     Is_Admin):
    if RFID != 0:
        try:
            if not sqlite.is_RFID_in_PersonnelData(GlobalSettings.config_db_name, RFID):
                sqlite.insert_usr_data(RFID, Avatar_id, VorName, NachName, Rolle, TelefonNr1, TelefonNr2, EmailArbeit,
                                       Is_Admin)
            else:
                print('RFID Card is already in Stamm_daten_Mensch')

        except:
            print('error !! can not insert the date to the menschstammdaten table')

    else:
        print('RFID Chip scannen!')

    add_user_obj.reset()


