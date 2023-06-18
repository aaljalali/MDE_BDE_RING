#pip3 install pyudev (Linux)
import re
import threading
from global_settings import GlobalSettings
from serial.tools import list_ports
from time import sleep
import serial
import serial.tools.list_ports
from sqlite import  operator_performance_id_exists
import time
import platform


### schwinn "1100-11890-X12"
def extract_auftrag_bauteil(barcode):
    GlobalSettings.scanned_bauteil_nr, GlobalSettings.scanned_auftrag_nr, more = barcode.split("-")
    print("Scanned Auftrag Nr:", GlobalSettings.scanned_auftrag_nr)
    print("Scanned Bauteil Nr:", GlobalSettings.scanned_bauteil_nr)

def decode_machine_status(barcode):
    if barcode == "103 0001 106" or barcode == "0001" or barcode == 1 :
        return "Maschine An/läuft","An"
    elif barcode == "103 0010 106" or barcode == "0010" or barcode == 10 :
        return "Maschine Aus", "Aus"
    elif barcode == "103 0011 106" or barcode == "0011" or barcode == 11:
        return "Maschine Läuft nicht","LUN"
    elif barcode == "103 0100 106" or barcode == "0100" or barcode == 100:
        return "Störung/ Wartung", "StW"
    elif barcode == "103 0101 106" or barcode == "0101" or barcode == 101:
        return "Hand Betrieb", "MB"
    elif barcode == "103 0000 106" or barcode == "0000" or barcode == 0:
        return "Delete", "-1"

def decodiere_barcode(barcode):
    #  Decode the barcode
    mitarbeiter_id_format = re.compile(r'^MAID-\d{4}$')
    leistungsdaten_format = re.compile(r'^\d{4}$')
    machine_status_format = re.compile(r'^103 (0001|0010|0011|0100|0101|0000) 106$')
    auftrag_bauteil_format = re.compile('^[A-Z]{1}\d{4}[A-Z]{1}\d{2}[A-Z]{1}\d{2}\.{1}[A-Z]{1}$')
    schwinn_auftrag_bauteil_format = re.compile('^\d{4}-\d{5}-[a-zA-Z]{1}\d{2}$')

    if mitarbeiter_id_format.match(barcode):
        # Extract Mitarbeiter ID
        GlobalSettings.last_scanned_MAid = int(barcode[-4:])

    elif leistungsdaten_format.match(barcode):
        if int(barcode[-2:]) == 99: # Rückgang
            GlobalSettings.scanned_operator_activity_id = -1
        # Extract maschine Leistungsdaten
        if operator_performance_id_exists(int(barcode[-2:])):
            GlobalSettings.scanned_operator_activity_id = int(barcode[-2:])
        else:
            pass

    elif machine_status_format.match(barcode):

        if int(barcode[4:8])== 0: ##Rückgang barcode
            GlobalSettings.scanned_machine_activity_id = -1
        else:
           GlobalSettings.scanned_machine_activity_id = int(barcode[4:8])
        GlobalSettings.scanned_machine_activity_name, GlobalSettings.registered_machine_activity_name_short_form = decode_machine_status(barcode)

    elif schwinn_auftrag_bauteil_format.match(barcode):
         extract_auftrag_bauteil(barcode)

    else:
        print("Ungültiger Barcode")


class BarcodeScanner:
    def __init__(self, baud_rate=9600, timeout=1):
        print('BarcodeScanner object created!')
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.ser = None

    def connect(self):
        system = platform.system()

        if system == 'Windows':
            # Get a list of all available serial ports
            print('Hi from Windows OS')
            # on Windows, the serial port names start with 'COM'
            ports = [p.device for p in serial.tools.list_ports.comports() if
                     'COM' in p.device and 'USB-Gerät' in p.description]
            if ports:
                print(ports)
                self.ser = serial.Serial(ports[0], self.baud_rate, timeout=self.timeout)

            else:
                GlobalSettings.system_message = 'Barcode scanner nicht verbunden1!'
                GlobalSettings.system_message_fg_color='red'
                raise Exception("No serial port found.")



        elif system == 'Linux':
            import pyudev
            print('detected system is Linux')
            # on Linux, the serial port names start with 'tty'
            ports = [p.device for p in serial.tools.list_ports.comports() if 'tty' in p.device]
            if ports:
                self.ser = serial.Serial(ports[0], self.baud_rate, timeout=self.timeout)
                print('Barcode scanner connected to port : ', ports[0])
                GlobalSettings.system_message = 'Barcode scanner verbunden!'
            else:
                raise Exception("No serial port found.")
        else:
            raise Exception("Unsupported operating system.")


    def read(self):
            if not self.ser:
                raise Exception("Not connected to a serial port.")

            data = self.ser.readline().decode().strip()
            if data:
                return data
            else:
                return None
        
        
    def read_barcode(self):
        # Reads the barcode
        try:
            self.connect()
            while True:
                data = self.read()
                if data:
                    print(f"Barcode scanned: {data}")
                    self.store_barcode(data)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.close()
        
            

    def store_barcode(self, barcode):
        # Store the barcode
        GlobalSettings.last_scanned_barcode = barcode
        decodiere_barcode(barcode)

        print(f'last_scanned_barcode = {GlobalSettings.last_scanned_barcode}')

    def start_reading(self):
        # Starts reading barcode in a separate thread
        thread = threading.Thread(target=self.read_barcode)
        thread.start()

    def close(self):
        # Closes the serial connection
        if self.ser:
            self.ser.close()
            self.ser = None


if __name__ == "__main__":
    print('start brcode scanner test')
    scanner = BarcodeScanner()
    scanner.read_barcode()
