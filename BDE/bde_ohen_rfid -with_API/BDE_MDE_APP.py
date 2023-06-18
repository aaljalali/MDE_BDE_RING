from GUI_BDE_MDE_APP import *
from global_settings import GlobalSettings, time_diff
from bde import bde_process
from Barcode import *
from activities import close_bde_app

def main():
    # Starte den BDE Prozess
    bde_process()
    
    GlobalSettings.set_config(GlobalSettings)
    # Erstelle eine Instanz der BDEApp und setze die Labels entsprechend
    api = BDEApp(' Hi ', ' Ali ')
    api.bereich_lbl['text'] = f'{GlobalSettings.BEREICH_NAME}'
    api.abteilung_lbl['text'] = f'{GlobalSettings.ABTEILUNGNAME}'
    api.Station_lbl['text'] = f' {GlobalSettings.Station_ID} '




    try:
        # Aktualisiere die Labels in der GUI in einer Endlosschleife
        while True:
            api.operator_activity_duration_lbl['text'] = f'{time_diff(GlobalSettings.operator_activity_start_time_unix)}'
            api.machine_activity_duration_lbl['text'] = f'{time_diff(GlobalSettings.machine_activity_start_time_unix)}'
            api.Bauteil_lbl['text'] = f'{GlobalSettings.registered_bauteil_nr}'
            api.Bauteil_lbl['bg'] =  GlobalSettings.Bauteil_lbl_bg_color
            api.Auftrag_nr_lbl['text'] = f'{GlobalSettings.registered_auftrag_nr}'
            api.Auftrag_nr_lbl['bg'] = f'{GlobalSettings.Auftrag_nr_bg_color}'
            api.leistungsart_lbl['text'] = f'{GlobalSettings.registered_operator_activity_name}'
            api.leistungsart_lbl['bg'] = GlobalSettings.operator_activity_lbl_bg_color
            api.system_message['text'] = f'{GlobalSettings.system_message}'
            api.system_message['fg'] = f'{GlobalSettings.system_message_fg_color}'
            api.client_server_connection_lable['bg'] = GlobalSettings.client_server_connection_lable_color
            api.machine_leistungsart_lbl['text'] =  f'{GlobalSettings.registered_machine_activity_name}'
            api.machine_leistungsart_lbl['bg'] = GlobalSettings.machine_activity_lbl_bg_color
            api.usr_lbl['text'] = f'{GlobalSettings.registed_user_name}'
            api.usr_lbl['bg'] = f'{GlobalSettings.registed_user_name_bg_color}'
            api.update_image(GlobalSettings.current_img_path)
            api.root.update()  # Aktualisiere die GUI

    except KeyboardInterrupt:
        # Wenn das Programm durch den Benutzer unterbrochen wird, gebe diese Meldung aus
        print("Programm wurde durch Benutzer unterbrochen.")
    except :
        print('close!')
        close_bde_app()

if __name__ == "__main__":
    main()
