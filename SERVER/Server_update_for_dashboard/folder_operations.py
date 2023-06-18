from datetime import datetime
import os

#################################################
###### set datum und uhrzeit variable
#################################################
def get_ts():
     return (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
  
def get_current_month():
    return datetime.now().strftime("%B")
    

def get_current_year():
    return( datetime.now().strftime("%Y"))
    
#################################################
###### creat folder if not exist  
#################################################
def creat_folder(path, folder_name):
    if not os.path.exists(path + folder_name):
           os.makedirs(path + folder_name)
    return path +folder_name + "/"

#creat db path if not exist DB/Year/
def current_server_db_path():
    server_db_path = creat_folder('', f"DB/{get_current_year()}")
    
    return server_db_path 


def current_json_path(program_folder_path,new_folder):
    json_mde_path = creat_folder(program_folder_path, new_folder)
    json_mde_path = creat_folder(json_mde_path, get_current_year())
    json_mde_path = creat_folder(json_mde_path, get_current_month())
    return json_mde_path 
########################################################
# ##############       main       ######################
########################################################
if __name__ == '__main__':
    
  print(current_server_db_path())