import pymysql
import tools_date_heure
# Reads the MariaDb config files and then connects to the db
def connecter_mariadb():
    caractere = ""
    dictionnaire = {}

    with open('bdconfig.ini', "r", encoding="utf-8") as fh:
        liste = fh.readlines()
        for i in range(len(liste)):
            caractere += liste[i]
    fichier = caractere.split("\n")
    fichier = [i for i in fichier if "=" in i]
    for i in range(len(fichier)):
        if len(fichier[i]) > 0:
            liste = str(fichier[i])
            bddinfo = liste.split("=")
            dictionnaire[bddinfo[0]] = bddinfo[1]
    db = pymysql.connect(host=dictionnaire['host'],
                         user=dictionnaire['user'],
                         port=int(dictionnaire['port']),
                         password=dictionnaire['password'],
                         database=dictionnaire['database'],)

    return db

# Inserts data stored in a parameter in a table also specified in the parameters. 
def inserer_valeur(connection, table, timestamp, value):
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(f""" INSERT INTO {table} (timestamp, value) VALUES ({timestamp},{value})""")
    connection.commit()



# This function interogates the database and fetches the data that is included in a certain time frame. 
def interroger(connection, table, date_debut, date_fin):
    listebdd = []
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(""" SELECT * FROM table WHERE date BETWEEN :date_debut AND :date_fin""", {'table': table, 'date_debut': date_debut, 'date_fin': date_fin})
    sql = cursor.fetchall()
    for i in range(len(sql)):
        dico = {}
        test = sql[i]
        dico["date"] = test[0].strftime('%Y-%m-%d' " "'%H:%M:%S')
        dico["valeur"] = test[1]
        listebdd.append(dico)

    return listebdd

def main():
    #interroger(connecter_mariadb(),"test",'22-02-2002','22-03-2003')
    connecter_mariadb()
if __name__ == '__main__':
    main()
# Fin
