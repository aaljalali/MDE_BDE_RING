import requests
from global_settings import GlobalSettings
import json
import os


#####################################################################################
#                        Server- und Portinformationen
#####################################################################################
def update_ip():
    global port, pi_server_id, mde_url, bde_url, server_health_url, url_delete_last_mde,url_delete_last_bde
    pi_server_id = GlobalSettings.Api_server_ip_address  # '192.168.188.168'
    port = GlobalSettings.Api_server_port_number  # '8000'
    mde_url = f"http://{pi_server_id}:{port}/mde/"
    bde_url = f"http://{pi_server_id}:{port}/bde/"
    url_delete_last_mde = f"http://{pi_server_id}:{port}/mde/{GlobalSettings.Station_ID}/drob_last_activity/"
    url_delete_last_bde = f"http://{pi_server_id}:{port}/bde/{GlobalSettings.Station_ID}/drob_last_activity/"
    server_health_url = f"http://{pi_server_id}:{port}/health/"


mde_json_buffer = 'mde_buffer.json'
bde_json_buffer = 'bde_buffer.json'

#####################################################################################
#                       Testdaten für MDE- und BDE-POST-Anforderungen
#####################################################################################
mde_test_data = {
    'TS': '2022-11-12 12:01:44',
    'Station_ID': 55,
    'Machine_performance': '9',
    'Program_name': 'PROGRAM1',
    'Tool_number': 'TOOL123'
}

bde_test_data = {
    'TS': '2022-11-12 12:01:44',
    'Station_ID': 55,
    'RFID': 123456,
    'Order_number': 'ORD123',
    'Part_number': 'PART456',
    'Performance_ID': 789,
    'Duration_sec': 3600
}


#####################################################################################
#               Aktualisiert MDE-Daten und BDE-Daten aus den globalen Einstellungen
#####################################################################################
def update_mde_data():
    """
    Aktualisiert MDE-Daten aus den globalen Einstellungen
    """
    mde_data = {
        'TS': GlobalSettings.formatted_machine_activity_start_time,
        'Station_ID': GlobalSettings.Station_ID,
        'Machine_performance': GlobalSettings.registered_machine_activity_name_short_form,
        'Program_name': GlobalSettings.registered_auftrag_nr,
        'Tool_number': GlobalSettings.registered_tool_nr
    }
    return mde_data


def update_bde_data():
    """
    Aktualisiert BDE-Daten aus den globalen Einstellungen
    """
    bde_data = {
        'TS': GlobalSettings.formatted_operator_activity_start_time,
        'Station_ID': GlobalSettings.Station_ID,
        'RFID': GlobalSettings.registed_MAid,
        'Order_number': GlobalSettings.registered_auftrag_nr,
        'Part_number': GlobalSettings.registered_bauteil_nr,
        'Performance_ID': GlobalSettings.registered_operator_activity_id,
        'Duration_sec': GlobalSettings.operator_activity_duration_sec
    }
    return bde_data


#####################################################################################
#               Prüft, ob eine Verbindung zum Api server besteht
#####################################################################################
def check_connection():
    try:
        update_ip()
        response = requests.get(server_health_url, timeout=0.3)
        if response.status_code == 200:
            print('connected to api server !')
            GlobalSettings.client_server_connection_lable_color ='green'
            return True
        else:
            GlobalSettings.client_server_connection_lable_color = 'orange'
            return False
    except requests.exceptions.RequestException:
        print('no connection to api server!', server_health_url)
        GlobalSettings.client_server_connection_lable_color = 'red'
        return False


#####################################################################################
#              POST-Anfrage mit gegebenen Daten an die gegebene URL senden
#####################################################################################
def post_data(url, data):
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print('POST-Anfrage erfolgreich')
            print('Status Code:', response.status_code)
            print('JSON Response:', response.json())

        else:
            print('POST-Anfrage fehlgeschlagen')
            print('Status Code:', response.status_code)
            if url == bde_url:
                save_data_to_file(data, bde_json_buffer)
            if url == mde_url:
                save_data_to_file(data, mde_json_buffer)

    except:
        # Bei Verbindungsproblemen zur API Server, gibt es eine Fehlermeldung, und die dat in zugehorige json buffer speichern
        print('connecetion error to', url)
        if url == bde_url:
            save_data_to_file(data, bde_json_buffer)
        if url == mde_url:
            save_data_to_file(data, mde_json_buffer)


####################################################################################
##### delete the last sent data
####################################################################################
def delete_data(url):
    try:
        response = requests.post(url)
        if response.status_code == 200:
            print('Delete-Anfrage erfolgreich')
            print('Status Code:', response.status_code)
            print('JSON Response:', response.json())
            GlobalSettings.system_message = 'Delete-Anfrage erfolgreich !'
            GlobalSettings.system_message_fg_color = 'green'

        else:
            print('delete-Anfrage fehlgeschlagen')
            print('Status Code:', response.status_code)
            GlobalSettings.system_message = 'delete-Anfrage fehlgeschlagen !'
            GlobalSettings.system_message_fg_color = 'rot'


    except:
        # Bei Verbindungsproblemen zur API Server, gibt es eine Fehlermeldung
        print('connecetion error to', url)

#####################################################################################
#         Spiechr die json Daten local, wenn Verbindung zum Server fehler geschlagen ist
#####################################################################################
def save_data_to_file(data, filename):
    """
    Speichert die angegebene Daten im JSON-Format in der angegebenen Datei.

    :param data: Die zu speichernden Daten.
    :param filename: Der Name der Datei, in der die Daten gespeichert werden sollen.
    """
    # Eine Meldung ausgeben, um anzuzeigen, dass die Daten gespeichert werden
    print('Es konnte keine Verbindung zum API-Server hergestellt werden. Die Daten werden lokal gespeichert...')
    GlobalSettings.system_message = 'Es konnte keine Verbindung zum API-Server hergestellt werden. Die Daten werden lokal gespeichert...'
    GlobalSettings.system_message_fg_color = 'green'

    # Die Datei im 'append mode' öffnen und die Daten in die Datei schreiben .
    with open(filename, 'a') as f:
        f.write(json.dumps(data) + '\n')


def is_file_empty(filename):
    """
    Returns True if the file is empty, False otherwise.

    :param filename: The name of the file to check.
    """
    return os.stat(filename).st_size == 0


def remove_last_object_from_file(filename):
    """
    Deletes the last object from the JSON file specified by filename.

    :param filename: The name of the JSON file.
    """
    # Load the existing data from the file
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Remove the last line (i.e. the last object in the file)
    lines.pop()

    # Overwrite the existing file with the modified data
    with open(filename, 'w') as f:
        f.writelines(lines)


#####################################################################################
#         Sendet lokal gespeicherte Daten, wenn Verbindung wiederhergestellt ist
#####################################################################################
def send_queued_data(url, file):
    try:
        with open(file, 'r') as f:
            for line in f:
                data = json.loads(line)
                post_data(url, data)
        # Wenn alle lokal gespeicherten Daten erfolgreich gesendet wurden, lösche die Datei
        open(file, 'w').close()
        print('Alle lokal gespeicherten Daten erfolgreich gesendet')

    except FileNotFoundError:
        # Wenn keine lokal gespeicherten Daten vorhanden sind, tue nichts
        pass


#####################################################################################
#                                    Post MDE Daten
#####################################################################################
def post_mde_data():
    mde_data = update_mde_data()
    if check_connection():
        send_queued_data(mde_url, mde_json_buffer)
        post_data(mde_url, mde_data)
        GlobalSettings.system_message ='Alle lokal gespeicherten  MDE Daten erfolgreich gesendet'
        GlobalSettings.system_message_fg_color = 'green'
    else:
        save_data_to_file(mde_data, mde_json_buffer)


#######
# delete las mde data
#####
def delete_last_mde():
    print(' api_client.delete_last_mde() called!')
    if not is_file_empty(
            mde_json_buffer):  ## if buffer not empty thats mean there was no connection to server and the last data are only saved localy
        print('>>>>>>>>>>>>>>>>>>>>>> last mde object is deleted from puffer !')
        GlobalSettings.system_message ='last mde object is deleted from puffer !'
        GlobalSettings.system_message_fg_color = 'green'
        remove_last_object_from_file(mde_json_buffer)

    else:  # the last data are sendet to the server so we need to delete them from there
    # api delete request
      if check_connection():
            delete_data(url_delete_last_mde)




#####################################################################################
#                                    Post BED date
#####################################################################################
def post_bde_data():
    bde_data = update_bde_data()
    if check_connection():
        send_queued_data(bde_url, bde_json_buffer)
        post_data(bde_url, bde_data)
        GlobalSettings.system_message ='Alle lokal gespeicherten BDE Daten erfolgreich gesendet'
        GlobalSettings.system_message_fg_color = 'green'
    else:
        save_data_to_file(bde_data, bde_json_buffer)


#######
# delete las bde data
#####
def delete_last_bde():
    print('  api_client.delete_last_bde() called!')
    if not is_file_empty(
            bde_json_buffer):  ## if buffer not empty thats mean there was no connection to server and the last data are only saved localy
        print('>>>>>>>>>>>>>>>>>>>>>> last bde object is deleted from puffer !')
        GlobalSettings.system_message ='last bde object is deleted from puffer !'
        GlobalSettings.system_message_fg_color = 'green'

        remove_last_object_from_file(bde_json_buffer)


    else:  # the last data are sendet to the server so we need to delete them from there
        # api delete request
        if check_connection():
            delete_data(url_delete_last_bde)


#####################################################################################
#                                    Main
####################################################################################
if __name__ == '__main__':
    # MDE-Daten senden
    mde_data = update_mde_data()
    post_data(mde_url, mde_data)

    # BDE-Daten senden
    bde_data = update_bde_data()
    post_data(bde_url, bde_data)
