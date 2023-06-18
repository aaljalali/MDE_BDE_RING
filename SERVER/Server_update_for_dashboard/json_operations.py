import io
import json
import os
from pydantic import BaseModel
from typing import Optional
from varname import nameof
import inspect
########################
########  VAR  ########
########################
filename = 'nknown_machine.json'
entry = {'test': 21}
path='./'

########################################################
##########    check if file exist  ############
########################################################
def startupCheck(path,filename):
    if os.path.isfile(path+filename) and os.access( path, os.R_OK):
        # checks if file exists
        print ("File exists and is readable")
    else:
        print ("Either file is missing or is not readable, creating file...")
        with io.open(os.path.join(path+filename ), 'w') as db_file:
            db_file.write(json.dumps([]))
   
########################################################
#########      Add data to json file      ############ 
########################################################  
def json_append(path, entry): ### noch nicht fertig
    #print('entry= .....................................', entry["Station_ID"])
    try:
            try :
                 Station_ID = entry["Station_ID"] 
                 filename =f"machine_{Station_ID}.json"
            except:
                 filename = 'unknown_machine.json'
                
            print('filename ',filename)
            startupCheck(path,filename)
            # Read file contents
            with open(path+filename, "r") as file:
                data = json.load(file)
                # remove duplicates
                data = [i for n, i in enumerate(data)
                            if i not in data[n + 1:]]
            #Update json object
            data.append(entry)
            # 3. Write json file
            with open(path+filename, "r+") as file:
                # remove duplicates
                data = [i for n, i in enumerate(data)
                            if i not in data[n + 1:]]        
                json.dump(data, file)
            return 1
    except:
         return -1
        
#######################################################
        ###
########################################################
def remove_last_object_from_file(filename): ### noch nicht fertig
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
########################################################
# ##############       main       ######################
########################################################
if __name__ == '__main__':
   entry={'Station_ID': 18, 'ts': '20.11.2022 13:05:55', 'machine_leistungsart': 'AUS', 'PGM': '10114141-gh-74', 'wkz': None}           
   print(json_append('./', entry))