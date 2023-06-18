# pip3 install serial
import global_settings
from activities import *


def print_and_update(to_print, last_printed):
    if to_print != last_printed:
        last_printed = to_print
        print(to_print)
    return last_printed


##########################################################################
##Die Funktion check_and_update_rfid_status() prüft den Status der gescannten RFID und aktualisiert ihn entsprechend.
# Die Funktion prüft, ob die gescannte RFID in der Datenbank vorhanden ist, ob ein Mensch angemeldet ist, ob ein Mensch
# angemeldet werden soll oder ob ein Mensch abgemeldet werden soll. Je nach Ergebnis aktualisiert die Funktion
# die entsprechenden globalen Einstellungen und druckt eine entsprechende Nachricht.
######################################################################################
def check_and_update_rfid_status():
    last_printed = None

    # Überprüfen, ob die zuletzt gescannte RFID in der Datenbank vorhanden ist
    def check_last_scanned_rfid():
        nonlocal last_printed
        if GlobalSettings.last_scanned_MAid != 0 and not sqlite.rfid_exists(GlobalSettings.last_scanned_MAid):
            GlobalSettings.last_scanned_MAid = 0
            to_print = 'Ihre RFID ist nicht im System!'
            last_printed = print_and_update(to_print, last_printed)
            ## blinke falls die MID NICHT BEKANNT ist
            registed_user_name_bg_color = GlobalSettings.registed_user_name_bg_color
            registed_user_name = GlobalSettings.registed_user_name
            for i in range(6):  # blink 6 times
                GlobalSettings.registed_user_name = 'NICHT BEKANNT!'
                GlobalSettings.registed_user_name_bg_color ='red'  # turn on
                time.sleep(0.1)  # wait for 0.1 seconds
                GlobalSettings.registed_user_name_bg_color ='white' # turn off
                time.sleep(0.1)  # wait for 0.1 seconds
                GlobalSettings.registed_user_name_bg_color = registed_user_name_bg_color # BACK TO THE LAST COLOR
            GlobalSettings.registed_user_name = registed_user_name

    # Überprüfen, ob ein Mensch angemeldet ist
    def check_registered_rfid():
        nonlocal last_printed
        if GlobalSettings.registed_MAid == 0 and GlobalSettings.last_scanned_MAid == 0:
            to_print = 'Kein Mensch an BDE angemeldet!'
            last_printed = print_and_update(to_print, last_printed)
            GlobalSettings.registed_user_name_bg_color = 'orange'

    # Überprüfen, ob ein Mensch angemeldet werden soll
    def check_to_register_rfid():
        nonlocal last_printed
        if GlobalSettings.registed_MAid == 0 and GlobalSettings.last_scanned_MAid != 0:
            GlobalSettings.last_scanned_barcode = 0
            GlobalSettings.registed_MAid = GlobalSettings.last_scanned_MAid
            GlobalSettings.last_scanned_MAid = 0
            GlobalSettings.registed_user_name = sqlite.get_name(GlobalSettings.registed_MAid, 2)
            GlobalSettings.is_MAID_registed = True
            to_print = f'Mensch mit RFID = {GlobalSettings.registed_MAid} ist angemeldet...'
            GlobalSettings.registed_user_name_bg_color = 'green'
            last_printed = print_and_update(to_print, last_printed)


    # Überprüfen, ob ein Mensch abgemeldet werden soll
    def check_to_unregister_rfid():
        nonlocal last_printed
        if GlobalSettings.registed_MAid == GlobalSettings.last_scanned_MAid != 0:
            GlobalSettings.registed_MAid = GlobalSettings.last_scanned_MAid = 0
            GlobalSettings.registed_user_name = 'RFID scannen'
            GlobalSettings.is_MAID_registed = False
            to_print = f'Mensch mit RFID = {GlobalSettings.registed_MAid} ist abgemeldet.'
            last_printed = print_and_update(to_print, last_printed)
            GlobalSettings.registed_user_name_bg_color = 'Orange'
            try:
                #untrack_machine_activity()
                untrack_operator_activity()
            except:
                pass
            #reset_auftrag_bautei()

    # Überprüfen, ob eine Registrierung aktualisiert werden soll
    def check_to_update_registration():
        nonlocal last_printed
        if GlobalSettings.registed_MAid != 0 and GlobalSettings.last_scanned_MAid != 0 and GlobalSettings.registed_MAid != GlobalSettings.last_scanned_MAid:
            GlobalSettings.last_scanned_barcode = 0
            GlobalSettings.registed_MAid = GlobalSettings.last_scanned_MAid
            GlobalSettings.last_scanned_MAid = 0
            GlobalSettings.registed_user_name = sqlite.get_name(GlobalSettings.registed_MAid, 2)
            GlobalSettings.is_MAID_registed = True
            to_print = f'Mensch mit RFID = {GlobalSettings.registed_MAid} ist angemeldet...'
            GlobalSettings.registed_user_name_bg_color = 'green'
            last_printed = print_and_update(to_print, last_printed)
            try:
                #untrack_machine_activity()
                untrack_operator_activity()
            except:
                pass
            #reset_auftrag_bautei()

    # Aufruf der einzelnen Funktionen
    check_last_scanned_rfid()
    check_registered_rfid()
    check_to_register_rfid()
    check_to_unregister_rfid()
    check_to_update_registration()


###########################################################################################

def bde_process():
    # Code for main function 1
    # Erstelle eine Instanz des BarcodeScanners und starte das Lesen
    scanner = BarcodeScanner()
    scanner.start_reading()

    def infinite_loop():
        while True:
            # print(GlobalSettings.is_MAID_registed)
            check_and_update_rfid_status()
            update_auftrag_bautei()
            if GlobalSettings.is_MAID_registed:
                GlobalSettings.current_img_path = GlobalSettings.bde_path + sqlite.get_img_path(
                    GlobalSettings.registed_MAid)

                # Ordner für aktuelle Maschinendaten und Operator-Daten erstellen
                GlobalSettings.current_machine_data_folder, GlobalSettings.current_operator_data_folder = folders.create_folders()
                bde_machine_activties()
                bde_operator_activites()
            else:
                GlobalSettings.current_img_path = GlobalSettings.default_img_path



            time.sleep(1.5)

    # Erstelle einen neuen Thread und führe die Funktion read_smartcard darin aus
    thread = threading.Thread(target=infinite_loop)
    thread.start()


if __name__ == '__main__':
    bde_process()
