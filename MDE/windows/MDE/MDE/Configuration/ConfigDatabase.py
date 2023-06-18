import sqlite3
import os
import traceback
##################################
# create_connection to DB function
##################################
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
        ##print(sqlite3.version)
    except  :
        print('Canont creat db ',db_file )
        
#################################################
###### check if table exist in db
#################################################
def table_exist(db_file, table_name):
    conn = create_connection(db_file)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND NAME = ?;",(table_name,))
    tables = [
        v[0] for v in cursor.fetchall()
        if v[0] != "sqlite_sequence"
    ]
    if conn:
            conn.close()
    return len(tables) > 0




class SqLiteDatabae:
    
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, schema):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({','.join(schema)})")
        self.conn.commit()
        


    def insert_data(self, table_name, data, col_names=None):
        try:
            placeholders = ",".join(["?" for _ in data])
            if col_names is None:
                query = f"INSERT INTO {table_name} VALUES ({placeholders})"
            else:
                col_names_str = ",".join(col_names)
                query = f"INSERT INTO {table_name} ({col_names_str}) VALUES ({placeholders})"
                
            self.cursor.execute(query, data)
            self.conn.commit()
            last_row_id = self.cursor.lastrowid
            print(f"{data} inserted into {table_name} with primary key: {last_row_id}")
            return last_row_id
        except:
           print(f"Failed to insert data into {table_name}!")
           return -1






    def select_data(self, table_name, columns, condition):
        self.cursor.execute(f"SELECT {columns} FROM {table_name} WHERE {condition}")
        ##print(f"SELECT {columns} FROM {table_name} WHERE {condition}")
        result = self.cursor.fetchall()
        ##print(result)
        return result

    def close_connection(self):
        self.conn.close()
        
        
class ConfigDatabase_(SqLiteDatabae):
    def __init__(self, db_name):
       
        super().__init__(db_name)
        self.last_insterted_filterd_roh_data = []
        self.current_script_path = os.path.abspath(__file__)
        self.script_dir = os.path.dirname(self.current_script_path )
        self.parent_dir = os.path.dirname(self.script_dir)
       # self.pattern_dir=f"{self.parent_dir}/PatternDetection/templates"
        self.PARAMETERS_SCHEMA = [
            "par_name TEXT NOT NULL",
            "mode_id  INTEGER NOT NULL",
            "par_pos TEXT",

            "PRIMARY KEY(par_name, mode_id)"]
        
        self.MODUS_SCHEMA = [
            "id INTEGER NOT NULL",
            "name TEXT NOT NULL",
            "PRIMARY KEY(id)"]
        
        
        self.REF_IMGs_SCHEMA =  [
            "mod_id  INTEGER NOT NULL",
            "merkmal_pos TEXT NOT NULL",
            "ref_img_path TEXT NOT NULL", 
            "PRIMARY KEY(mod_id)"]
        
         
        self.all_modes_info_dict = self.get_modes()
        

        
        
    def str_to_int_tuple(self, value):
        # Check if the value is a string representation of a tuple
        if value.startswith("(") and value.endswith(")"):
            # Convert the string to a tuple of integers
            return tuple(map(int, value.strip("()").split(",")))
        else:
            return value


    def creat_config_db(self):
        self.create_table("Parameters", self.PARAMETERS_SCHEMA)
        self.create_table("Modus", self.MODUS_SCHEMA)
        self.create_table("Refernce_Images", self.REF_IMGs_SCHEMA)
        
        
        
    def creat_filterd_roh_data_db_table(self, db_path, db_name, table_name):
        if(not table_exist(f"{db_path}/{db_name}", table_name)):
            conn = sqlite3.connect(db_path+'/'+db_name)
            sql = "CREATE TABLE IF NOT EXISTS " +table_name+" (TS TEXT INTEGER PRIMARY KEY, Machine_performance TEXT, Tool_number TEXT ,Program_name  TEXT)"
            cursor = conn.execute(sql)
            conn.close()
        
    def creat_roh_data_db_table(self, db_path, db_name, table_name ):
            
            if(not table_exist(f"{db_path}/{db_name}", table_name)):
                    result = self.cursor.execute('select par_name from Parameters;')
                    par_names= [
                        v[0] for v in result.fetchall()
                        if (v[0] != "sqlite_sequence") and (v[0]!="background_pixel")
                    ]
                   # par_names =list(dict.fromkeys(par_names)) ########
                   ###################### remove duplicate
                    unique_names = []
                    for name in par_names:
                        if name.lower() not in [n.lower() for n in unique_names]:
                            unique_names.append(name)

                    par_names =unique_names

                    ##print('selected Parameters :')
                    ##print(par_names)

                    conn = sqlite3.connect(db_path+'/'+db_name)
                    sql = "CREATE TABLE IF NOT EXISTS " +table_name+" (TS TEXT INTEGER PRIMARY KEY, ModeId INTEGER)"
                    cursor = conn.execute(sql)

                    i=0
                    while(i<len(par_names)):
                         column_name=par_names[i]
                         sql= "alter table " +  table_name + " add column '%s' 'text'" % column_name
                         conn.execute(sql)
                         par=par_names[i]
                         i+=1
                    if conn:
                            conn.close()
                        

                
    def insert_roh_data(self, db_path, table_name , parameters_names_values):
        print('parameters_names_values', type(parameters_names_values), parameters_names_values)
        # Open a connection to the database
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            
            # Build the SQL query string
            query = f"INSERT INTO {table_name} ( "
            query += ", ".join(parameters_names_values.keys())
            query += ") VALUES ( " + ", ".join(["?"] * len(parameters_names_values)) + ")"
            # Execute the query
            values =  list(parameters_names_values.values())
            c.execute(query, values)
            # Commit the changes and close the connection
            conn.commit()
            conn.close()
            print(f"{values} inserted to {table_name} table")
            
        except:
            print(f"can not insert  values  to roh {table_name} table")
            traceback.print_exc()
            
 

    def insert_unique_roh_data(self, db_path, table_name, parameters_names_values):
      #  try:
            # Open a connection to the database
            conn = sqlite3.connect(db_path)
            c = conn.cursor()

            # Retrieve the last data from the table
            query = f"SELECT {', '.join(parameters_names_values.keys())} FROM {table_name} ORDER BY ts DESC LIMIT 1"
            c.execute(query)
            last_data = c.fetchone()

            # Check if the new data is the same as the last data
            if last_data and last_data[1:] == tuple(parameters_names_values.values())[1:]: 
                print(" New data is the same as the last data.")
                return False
            else:
                # Build the SQL query string for insertion
                query = f"INSERT INTO {table_name} ("
                query += ", ".join(parameters_names_values.keys())
                query += ") VALUES ( " + ", ".join(["?"] * len(parameters_names_values)) + ")"

                # Execute the query
                values = list(parameters_names_values.values())
                c.execute(query, values)
                conn.commit()
                print(f" {values} inserted into {table_name} table")

            # Close the connection
            conn.close()
            return True
      #  except:
        #    print(f"Cannot insert values into {table_name} table")
           # traceback.print_exc()



    def get_parametrs(self, mode_id):
        parametrs_list = self.select_data("Parameters", "par_name, par_pos", f"mode_id={mode_id}")
        result = {}
        for key, value in parametrs_list:
            result[key] = self.str_to_int_tuple(value)
            

        ##print('get_parametrs-> result=',result)
        return result
    
    
    def get_mermal_pos(self, mode_id):
        merkmal_pos_str = self.select_data("Refernce_Images", "merkmal_pos",f" mod_id={mode_id}")
        merkmal_pos_tuple = self.str_to_int_tuple(merkmal_pos_str[0][0] )
        return merkmal_pos_tuple
     
    def add_mode(self , mode_name, merkmal_pos, pattern_path):
        table_name ="Refernce_Images"
        col_names = ("merkmal_pos","ref_img_path")
        data =(f"{merkmal_pos}", f"{pattern_path}")
        mode_id = self.insert_data( table_name, data, col_names )
        if mode_id >0:
            self.insert_data('Modus', (f"{mode_id}", f"{mode_name}" )) 
    #########################################
        ### get mode name
    #########################################
    def get_mod_name(self, mode_id):
        if(mode_id>0):
             
            mod_name= self.select_data("Modus", "name", f"id={mode_id}")[0][0]
            #print('modname = ', mod_name)
            return mod_name
        
    def get_modes(self):  
        mode_list = self.select_data("Refernce_Images", "mod_id, merkmal_pos,ref_img_path"," True")
        result = {}
        for  mode  in mode_list:
                
              
                    result[mode[0]] = self.str_to_int_tuple(mode[1]),f"{mode[2]}"
               

        return result
    
    
if __name__ == "__main__":
    
     config_db = ConfigDatabase_("MDE_Configuration.db")
     #config_db.insert_2("Refernce_Images", ('',''), (f"merkmal_pos", f"ref_img_path" ))

    # config_db.creat_config_db()
     #config_db.add_mode( 'mod1', '(0,1,0,5)', 'pattern_path/opopop/')
     config_db.insert_data("Parameters", ("u",3, "1336.35, 9.0, 396.48, 33.0"))
     #config_db.creat_roh_data_db_table( '/home/pi/Desktop/MDE-current/CaptureDevice/DB/Roh_Maschindaten/2023/April', 'test.db','test_table_name' )
     #config_db.get_parametrs(1)
           
     
   
     
     
