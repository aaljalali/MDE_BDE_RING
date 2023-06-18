from global_settings import GlobalSettings
from GUI_Add_usr import AddUser
from Barcode import *
from activities import kill_process

def main():
    def update_gui():
        api = AddUser(' Hi ')

        while True:
            try:
                if GlobalSettings.last_scanned_MAid == 0:
                    api.rfid_nr_lbl2['text'] = "Neue Chip scannen"
                else:
                    api.rfid_nr_lbl2['text'] = f"{GlobalSettings.last_scanned_MAid}"
                api.root.update()  # update the GUI to reflect the new label values
            except:
                pass

    scanner = BarcodeScanner()
    scanner.start_reading()
    update_gui()


if __name__ == "__main__":
    try:
      main()
    except:
        kill_process()
