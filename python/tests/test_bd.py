import inspect

import pymysql
import mock
import pytest
import yaml

import tools_introspection
import tools_tests

try:
    from python import bd
except:
    pass

MODULE = "bd"


# ************************************************************************************************
class TestStructure:

    def test_import_module(self):
        message = "{} n'a pas pu être importé pour les tests\n" \
                  "➔ Vérifiez que votre code n'a pas d'erreurs syntaxiques (vaguettes rouges)".format(MODULE)
        try:
            import python.bd
        except:
            assert False, tools_tests.affiche_message_erreur(message)

    # ---
    def test_declaration_main(self):
        FONCTION = "main"
        message = "Le programme principal {}.{} doit être déclaré".format(MODULE, FONCTION)
        liste = inspect.getmembers(bd)
        assert FONCTION in [liste[i][0] for i in range(len(liste))], \
            tools_tests.affiche_message_erreur(message)


class TestConnecterMariadb:
    FONCTION = "connecter_mariadb"

    # ---
    def test_declaration_fonction(self):
        message = "La fonction {}.{} doit être déclarée".format(MODULE, self.FONCTION)
        liste = inspect.getmembers(bd)
        assert self.FONCTION in [liste[i][0] for i in range(len(liste))], \
            tools_tests.affiche_message_erreur(message)

    # ---
    def test_nombre_parametres(self):
        nb_params = 0
        """Teste le nombre de paramètres de la fonction"""
        message = "La fonction {}.{} doit avoir {} paramètre".format(MODULE, self.FONCTION, nb_params)
        fct = tools_introspection.get_fonction_from_module(self.FONCTION, bd)
        assert len(inspect.signature(fct).parameters) == nb_params, \
            tools_tests.affiche_message_erreur(message)

    def test_appel_connect(self, datadir):
        data = datadir["bdconfig.ini"].read()
        """Teste le type de la valeur de retour"""
        with mock.patch("pymysql.connect") as mocked_func, \
                mock.patch('builtins.open', mock.mock_open(read_data=data)):
            mocked_func.return_value = "connect"
            res = bd.connecter_mariadb()
            mocked_func.assert_called_once_with(host='192.168.0.1', port=3306, database='sae24', user='sae24user',
                                                password='xxxx')

    def test_type_valeur_retour(self, datadir):
        data = datadir["bdconfig.ini"].read()
        """Teste le type de la valeur de retour"""
        with mock.patch("pymysql.connect") as mocked_func, \
                mock.patch('builtins.open', mock.mock_open(read_data=data)):
            mocked_func.return_value = "connect"
            res = bd.connecter_mariadb()
        assert res == "connect", "La fonction doit renvoyer le résultat de l'appel à la fonction 'connect'"


class TestInterroger:
    FONCTION = "interroger"

    # ---
    def test_declaration_fonction(self):
        message = "La fonction {}.{} doit être déclarée".format(MODULE, self.FONCTION)
        liste = inspect.getmembers(bd)
        assert self.FONCTION in [liste[i][0] for i in range(len(liste))], \
            tools_tests.affiche_message_erreur(message)

    # ---
    def test_nombre_parametres(self):
        nb_params = 4
        """Teste le nombre de paramètres de la fonction"""
        message = "La fonction {}.{} doit avoir {} paramètre".format(MODULE, self.FONCTION, nb_params)
        fct = tools_introspection.get_fonction_from_module(self.FONCTION, bd)
        assert len(inspect.signature(fct).parameters) == nb_params, \
            tools_tests.affiche_message_erreur(message)

    def test_type_valeur_retour(self, datadir):
        """Teste le type de la valeur de retour"""

        data = yaml.safe_load(datadir["data.yaml"].open())
        with mock.patch("pymysql.connect", spec=pymysql.Connection) as cnx:
            cursor_mock = mock.Mock()
            cnx.cursor.return_value = cursor_mock
            execute_mock = mock.Mock()
            cursor_mock.execute = execute_mock
            commit_fetchall = mock.Mock()
            cursor_mock.fetchall = commit_fetchall
            commit_fetchall.return_value = data
            res = bd.interroger(cnx, "test", "2022-03-01", "2022-03-15")
        assert isinstance(res, list), "La fonction doit renvoyer une liste"
        assert isinstance(res[0], dict), "La fonction doit renvoyer une liste contenant des dictionnaires"
        date = res[0].get("date")
        assert date is not None, \
            "La fonction doit renvoyer une liste contenant des dictionnaires avec une clé nommée 'date'"
        assert isinstance(date, str), "La clé date doit être une chaîne de caractères"
        value = res[0].get("valeur")
        assert value is not None, \
            "La fonction doit renvoyer une liste contenant des dictionnaires avec une clé nommée 'valeur'"
        assert isinstance(value, float), "La clé date doit être une valeur flottane"

    @pytest.mark.parametrize("fichier", ["data", "data2"])
    def test_valeur_retour(self, datadir, fichier):
        """Teste si la liste des données est correcte"""
        data = yaml.safe_load(datadir[f"{fichier}.yaml"].open())
        with mock.patch("pymysql.connect", spec=pymysql.Connection) as cnx:
            cursor_mock = mock.Mock()
            cnx.cursor.return_value = cursor_mock
            execute_mock = mock.Mock()
            cursor_mock.execute = execute_mock
            commit_fetchall = mock.Mock()
            cursor_mock.fetchall = commit_fetchall
            commit_fetchall.return_value = data
            res = bd.interroger(cnx, "test", "2022-03-01", "2022-03-15")

        expected = yaml.safe_load(datadir[f"_expected/{fichier}.yaml"].open())
        assert res == expected


class TestInsererValeur:
    FONCTION = "inserer_valeur"

    # ---
    def test_declaration_fonction(self):
        message = "La fonction {}.{} doit être déclarée".format(MODULE, self.FONCTION)
        liste = inspect.getmembers(bd)
        assert self.FONCTION in [liste[i][0] for i in range(len(liste))], \
            tools_tests.affiche_message_erreur(message)

    # ---
    def test_nombre_parametres(self):
        nb_params = 4
        """Teste le nombre de paramètres de la fonction"""
        message = "La fonction {}.{} doit avoir {} paramètre".format(MODULE, self.FONCTION, nb_params)
        fct = tools_introspection.get_fonction_from_module(self.FONCTION, bd)
        assert len(inspect.signature(fct).parameters) == nb_params, \
            tools_tests.affiche_message_erreur(message)

    def test_type_valeur_retour(self):
        """Teste le type de la valeur de retour"""
        with mock.patch("pymysql.connect", spec=pymysql.Connection) as cnx:
            res = bd.inserer_valeur(cnx, "test", 1644602070, 20.2)
        message = "La fonction {}.{} doit retourner None".format(MODULE, self.FONCTION)
        assert res is None, tools_tests.affiche_message_erreur(message)

    def test_appels_fonctions(self):
        """Teste les appels aux méthodes du mysql"""
        with mock.patch("pymysql.connect", spec=pymysql.Connection) as cnx:
            cursor_mock = mock.Mock()
            cnx.cursor.return_value = cursor_mock
            execute_mock = mock.Mock()
            cursor_mock.execute = execute_mock
            commit_mock = mock.Mock()
            cnx.commit = commit_mock

            bd.inserer_valeur(cnx, "test", 1644602070, 20.2)

            message = "La fonction {}.{} doit appeler la methode cursor.execute".format(MODULE, self.FONCTION)
            assert execute_mock.call_count == 1, tools_tests.affiche_message_erreur(message)

            message = "La fonction {}.{} doit appeler la méthode commit sur la connexion".format(MODULE, self.FONCTION)
            assert commit_mock.call_count == 1, tools_tests.affiche_message_erreur(message)
