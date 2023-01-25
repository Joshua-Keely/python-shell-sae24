import time

from bd import *
import tools_date_heure
import tools_elec
from acquisition import *

# converts a byte to a temperature
def conversion(mesure):
    rep = mesure / 5.1
    return rep

# Reads the electronics card config file and returns a dictionary that contains the value for the port key. 
def lecture_configuration():
    dico = dict()
    try:
        with open('acquisition.ini', 'r', encoding='utf-8') as a:
            lecture = a.readlines()
            lecture = [i for i in lecture]
            for line in lecture:
                if '=' in line:
                    split = line.split("=")
                    dico[split[0].strip()] = split[1].strip()
            if dico.get('port'):
                return dico
            else:
                return None
    except FileNotFoundError:
        return None
# Reads the acquisition config file, connects to the database.  
def acquisition(nb):
    lecture = lecture_configuration()
    confport = "COM1"
    while nb == -1:
        dbb = connecter_mariadb()
        ack = acquerir(confport, 1)
        degres = conversion(ack[0])
        timestamp = tools_date_heure.timestamp()
        inserer_valeur(dbb, 'temperatures', timestamp, degres)
        time.sleep(1)
    for i in range(nb):
        dbb = connecter_mariadb()
        ack = acquerir(confport,1)
        degres = conversion(ack[0])
        timestamp = tools_date_heure.timestamp()
        inserer_valeur(dbb, "temperatures", timestamp, degres)
        time.sleep(1)

def main():

    acquisition(-1)


if __name__ == '__main__':
    main()
# Fin
