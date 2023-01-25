import matplotlib.pyplot as plt
import tools_elec

# This function acquires the number of readings the sensor has made. 
def acquerir(port,nb_points):
    tools_elec.init_acquisition(port)
    donnee = []
    for i in range(nb_points):
        donnee.append(tools_elec.lecture_octet())
    return donnee

# This function prints out the data that is in the parameter.
def visualiser(legende, donnees):
    plt.plot(donnees)
    plt.title(legende)
    plt.show()

def main():
    print(acquerir('COM1', 20)) # aquisition de la temperature


if main == 'main':
    main()
# Fin
