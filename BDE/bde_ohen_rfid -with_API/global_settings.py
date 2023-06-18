import time
import json


def get_configuration(filename):
    with open(filename) as f:
        config = json.load(f)
    pi_server_ip = config["pi_server_ip"]
    port = config["Port"]
    station_id = config["StationID"]
    return pi_server_ip, port, station_id

# Berechnet die Differenz zwischen einer Startzeit und der aktuellen Zeit
def time_diff(ref_time):
    if ref_time is None:
        return '00:00:00'
    else:
        # Aktuelle Zeit abrufen
        current_time = time.time()
        time_diff_ = current_time - ref_time
        return time.strftime("%H:%M:%S", time.gmtime(time_diff_))





###########################################################################
   # This class contains global settings and variables for the application.
###########################################################################
class GlobalSettings:
    def set_config(self):
        GlobalSettings.Api_server_ip_address, GlobalSettings.Api_server_port_number, GlobalSettings.Station_ID = get_configuration(
            GlobalSettings.config_json_file)

    Api_server_ip_address= None
    Api_server_port_number = None
    # IDs and names
    Station_ID = 1
    ARBEITSPLATZ_ID = 1
    BEREICH_NAME = 'Fertigung'
    ABTEILUNGNAME = 'Montage'

    # Paths
    bde_path = '.'#'C://Users//aaljalali//Desktop//MA_Code//bde'
    db_bde_folder_name = 'Mensch'
    db_mde_folder_name = 'Machine'
    default_img_path ='Avatare//x.png'# bde_path + '//Avatare//x.png'
    config_db_name = 'BDE_Config.db'
    config_json_file = 'Config.json'
    current_machine_activities_path = None
    current_operator_activities_path = None
    current_img_path = default_img_path
    displayed_img_path = None
    current_machine_data_folder = None
    current_operator_data_folder = None
    current_operator_activity_table_name = None
    current_machine_activity_table_name = None
    # Timestamps
    operator_activity_start_time_unix = None
    formatted_operator_activity_start_time = '0000 00 00 00:00:00'
    operator_activity_end_time_unix = None
    operator_activity_duration_sec = None
    machine_activity_start_time_unix = None
    formatted_machine_activity_start_time = '0000 00 00 00:00:00'
    machine_activity_end_time_unix = None
    machine_activity_duration_sec = None


    # Colors
    operator_activity_lbl_bg_color = 'ORANGE'
    machine_activity_lbl_bg_color = 'ORANGE'
    Bauteil_lbl_bg_color = 'ORANGE'
    Auftrag_nr_bg_color = 'ORANGE'
    registed_user_name_bg_color = 'ORANGE'
    client_server_connection_lable_color = 'orange'
    system_message_fg_color = 'white'

    # Scan RFID information
    last_scanned_MAid = 000
    registed_MAid = 0
    is_MAID_registed = False
    registed_user_name = 'RFID scannen!'

    # Scan Barcode information
    last_scanned_barcode = '000000'

    # Activities
    registered_operator_activity_name = 'Mensch Leistungsart scannen!'
    scanned_operator_activity_id = 0
    registered_operator_activity_id = 0

    # Machine status
    scanned_machine_activity_id = 0
    registered_machine_activity_id = 0
    scanned_machine_activity_name = 'Maschine Leistungsart scannen!'
    registered_machine_activity_name = 'Maschine Leistungsart scannen!' # that`s what will be displayed on Gui
    registered_machine_activity_name_short_form = 'None' # that`s what will be saved in db

    # Bauteil
    scanned_bauteil_nr = 0
    registered_bauteil_nr = 0


    # Auftrag
    scanned_auftrag_nr = 0
    registered_auftrag_nr = 0

 # wekzeug
    registered_tool_nr = 0

# System_message
    system_message =' '