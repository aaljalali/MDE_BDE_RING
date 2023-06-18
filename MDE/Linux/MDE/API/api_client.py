import requests
import json
import os

update_ip_called = False
mde_json_buffer = 'mde_buffer.json'

#####################################################################################
#                        Server- und Portinformationen
#####################################################################################
def update_ip():
    global port, pi_server_id, mde_url, server_health_url, url_delete_last_mde
    # Get the current working directory
    current_script_path= os.path.abspath(__file__) 
    script_dir = os.path.dirname(current_script_path)
    root_dir = os.path.dirname(script_dir)
    config_dir= root_dir + '/ConfigFiles'
    config_path = os.path.join(config_dir, 'mde_config.json') 
    
    with open(config_path, 'r') as f:
            config = json.load(f)
            pi_server_id= config['pi_server_id']
            port = config['port']
            print(f"ip={pi_server_id}   port={port}")
    
    
    
    
    print("update ip called")
    #pi_server_id ='127.0.0.1'#GlobalSettings.Api_server_ip_address  # '192.168.188.168'
    #port = '8000' #GlobalSettings.Api_server_port_number  # '8000'
    mde_url = f"http://{pi_server_id}:{port}/mde/"
  
    server_health_url = f"http://{pi_server_id}:{port}/health/"



#####################################################################################
#                       Testdaten für MDE-POST-Anforderungen
#####################################################################################
mde_test_data = {
    'TS': '2022-11-12 12:01:44',
    'Station_ID': 1,
    'Machine_performance': 'Aus'#,
    #'Program_name': 'PROGRAM1',
   # 'Tool_number': 'TOOL123'
}





#####################################################################################
#               Prüft, ob eine Verbindung zum Api server besteht
#####################################################################################
def check_connection():
    try:
       
        response = requests.get(server_health_url, timeout=0.3)
        if response.status_code == 200:
            print('connected to api server !')
            #GlobalSettings.client_server_connection_lable_color ='green'
            return True
        else:
           # GlobalSettings.client_server_connection_lable_color = 'orange'
            return False
    except requests.exceptions.RequestException:
        print('no connection to api server!', server_health_url)
      #  GlobalSettings.client_server_connection_lable_color = 'red'
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
            if url == mde_url:
                save_data_to_file(data, mde_json_buffer)

    except:
        # Bei Verbindungsproblemen zur API Server, gibt es eine Fehlermeldung, und die dat in zugehorige json buffer speichern
        print('connecetion error to', url)
        if url == mde_url:
            save_data_to_file(data, mde_json_buffer)



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
   # GlobalSettings.system_message = 'Es konnte keine Verbindung zum API-Server hergestellt werden. Die Daten werden lokal gespeichert...'
    #GlobalSettings.system_message_fg_color = 'green'

    # Die Datei im 'append mode' öffnen und die Daten in die Datei schreiben .
    with open(filename, 'a') as f:
        f.write(json.dumps(data) + '\n')


def is_file_empty(filename):
    """
    Returns True if the file is empty, False otherwise.

    :param filename: The name of the file to check.
    """
    return os.stat(filename).st_size == 0



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
def post_mde_data(mde_data):
    global update_ip_called
    if not update_ip_called:
        # Call update_ip
        update_ip()
        # Set the flag to indicate that update_ip has been called
        update_ip_called = True
        
        
    #mde_data = update_mde_data()
    if check_connection():
        #send_queued_data(mde_url, mde_json_buffer)
        post_data(mde_url, mde_data)
        #GlobalSettings.system_message ='Alle lokal gespeicherten  MDE Daten erfolgreich gesendet'
       #  GlobalSettings.system_message_fg_color = 'green'
    else:
        save_data_to_file(mde_data, mde_json_buffer)



 
#####################################################################################
#                                    Main
####################################################################################
if __name__ == '__main__':
    # MDE-Daten senden
    
    mde_data = mde_test_data #update_mde_data()
 
    post_mde_data(mde_data)
 
