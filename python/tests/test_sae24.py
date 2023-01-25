import inspect
import os.path

import mock
import pytest

import tools_introspection
import tools_tests

try:
    import sae24
except:
    pass

MODULE = "sae24"


# ************************************************************************************************
class TestStructure:

    def test_import_module(self):
        message = "{} n'a pas pu être importé pour les tests\n" \
                  "➔ Vérifiez que votre code n'a pas d'erreurs syntaxiques (vaguettes rouges)".format(MODULE)
        try:
            from python import bd
        except:
            assert False, tools_tests.affiche_message_erreur(message)

    # ---
    def test_declaration_main(self):
        FONCTION = "main"
        message = "Le programme principal {}.{} doit être déclaré".format(MODULE, FONCTION)
        liste = inspect.getmembers(sae24)
        assert FONCTION in [liste[i][0] for i in range(len(liste))], \
            tools_tests.affiche_message_erreur(message)


class TestLectureConfiguration:
    FONCTION = "lecture_configuration"

    # ---
    def test_declaration_fonction(self):
        message = "La fonction {}.{} doit être déclarée".format(MODULE, self.FONCTION)
        liste = inspect.getmembers(sae24)
        assert self.FONCTION in [liste[i][0] for i in range(len(liste))], \
            tools_tests.affiche_message_erreur(message)

    # ---
    def test_nombre_parametres(self):
        nb_params = 0
        """Teste le nombre de paramètres de la fonction"""
        message = "La fonction {}.{} doit avoir {} paramètre".format(MODULE, self.FONCTION, nb_params)
        fct = tools_introspection.get_fonction_from_module(self.FONCTION, sae24)
        assert len(inspect.signature(fct).parameters) == nb_params, \
            tools_tests.affiche_message_erreur(message)

    def test_type_valeur_retour(self, monkeypatch, datadir):
        """Teste le type de la valeur de retour"""
        monkeypatch.chdir(os.path.dirname(str(datadir["acquisition.ini"])))
        res = sae24.lecture_configuration()
        assert isinstance(res, dict), "La fonction doit renvoyer une dict"
        assert "port" in res, "La clé 'port' doit être présente dans le dictionnaire"
        assert isinstance(res['port'], str), "La valeur associée à la clé 'port' doit être une chaine de caractères"

    @pytest.mark.parametrize("fichier, resultat", [
        pytest.param("fichier1.ini", {'port': "COM1"}, id="Test avec fichier1.ini"),
        pytest.param("fichier2.ini", {'port': "/dev/tty2"}, id="Test avec fichier2.ini"),
    ])
    def test_valeur_retour(self, monkeypatch, tmpdir, datadir, fichier, resultat):
        datadir[fichier].copy(tmpdir.join("acquisition.ini"))
        monkeypatch.chdir(tmpdir)
        actual = sae24.lecture_configuration()
        assert actual == resultat

    @pytest.mark.parametrize("fichier", [
        pytest.param("erreur1.ini"),
        pytest.param("erreur2.ini"),
    ])
    def test_erreur_sans_port(self, monkeypatch, tmpdir, datadir, fichier):
        datadir[fichier].copy(tmpdir.join("acquisition.ini"))
        monkeypatch.chdir(tmpdir)
        actual = sae24.lecture_configuration()
        assert actual is None


class TestConversion:
    FONCTION = "conversion"

    # ---
    def test_declaration_fonction(self):
        message = "La fonction {}.{} doit être déclarée".format(MODULE, self.FONCTION)
        liste = inspect.getmembers(sae24)
        assert self.FONCTION in [liste[i][0] for i in range(len(liste))], \
            tools_tests.affiche_message_erreur(message)

    # ---
    def test_nombre_parametres(self):
        nb_params = 1
        """Teste le nombre de paramètres de la fonction"""
        message = "La fonction {}.{} doit avoir {} paramètre".format(MODULE, self.FONCTION, nb_params)
        fct = tools_introspection.get_fonction_from_module(self.FONCTION, sae24)
        assert len(inspect.signature(fct).parameters) == nb_params, \
            tools_tests.affiche_message_erreur(message)

    def test_type_valeur_retour(self, monkeypatch, datadir):
        """Teste le type de la valeur de retour"""
        res = sae24.conversion(100)
        assert isinstance(res, float), "La fonction doit renvoyer un float"


class TestAcquisition:
    FONCTION = "acquisition"

    # ---
    def test_declaration_fonction(self):
        message = "La fonction {}.{} doit être déclarée".format(MODULE, self.FONCTION)
        liste = inspect.getmembers(sae24)
        assert self.FONCTION in [liste[i][0] for i in range(len(liste))], \
            tools_tests.affiche_message_erreur(message)

    # ---
    def test_nombre_parametres(self):
        nb_params = 1
        """Teste le nombre de paramètres de la fonction"""
        message = "La fonction {}.{} doit avoir {} paramètre".format(MODULE, self.FONCTION, nb_params)
        fct = tools_introspection.get_fonction_from_module(self.FONCTION, sae24)
        assert len(inspect.signature(fct).parameters) == nb_params, \
            tools_tests.affiche_message_erreur(message)

    def test_appel_lecture_configuration(self, datadir):
        data = tools_tests.lecture_fichier_yaml(datadir[f"data1.yaml"])
        with mock.patch("tools_elec.lecture_octet", side_effect=data["valeurs"]), \
                mock.patch("tools_date_heure.timestamp", side_effect=data["timestamps"]), \
                mock.patch("bd.inserer_valeur") as mock_inserer_valeur, \
                mock.patch("bd.connecter_mariadb") as mock_connecter_mariadb, \
                mock.patch("sae24.lecture_configuration",
                           return_value={"port": "COM1", "periode": 1}) as mock_lecture_configuration:
            sae24.acquisition(2)
        assert mock_lecture_configuration.call_count == 1, "La fonction 'lecture_configuration' doit être appelée 1 fois"

    def test_appel_connecter_mariadb(self, datadir):
        data = tools_tests.lecture_fichier_yaml(datadir[f"data1.yaml"])
        with mock.patch("tools_elec.lecture_octet", side_effect=data["valeurs"]), \
                mock.patch("tools_date_heure.timestamp", side_effect=data["timestamps"]), \
                mock.patch("bd.inserer_valeur") as mock_inserer_valeur, \
                mock.patch("bd.connecter_mariadb") as mock_connecter_mariadb, \
                mock.patch("sae24.lecture_configuration",
                           return_value={"port": "COM1", "periode": 1}) as mock_lecture_configuration:
            sae24.acquisition(2)
        assert mock_connecter_mariadb.call_count == 1, "La fonction 'connecter_mariadb' doit être appelée 1 fois"

    @pytest.mark.parametrize("nb", [
        pytest.param(5, id="Test pour 5 mesures"),
        pytest.param(10, id="Test pour 5 mesures"),
    ])
    def test_appel_lecture_octet(self, datadir, nb):
        data = tools_tests.lecture_fichier_yaml(datadir[f"data1.yaml"])
        with mock.patch("tools_elec.lecture_octet", side_effect=data["valeurs"]) as mock_lecture_octet, \
                mock.patch("tools_date_heure.timestamp", side_effect=data["timestamps"]), \
                mock.patch("bd.inserer_valeur") as mock_inserer_valeur, \
                mock.patch("bd.connecter_mariadb") as mock_connecter_mariadb, \
                mock.patch("sae24.lecture_configuration",
                           return_value={"port": "COM1", "periode": 1}) as mock_lecture_configuration:
            sae24.acquisition(nb)
        assert mock_lecture_octet.call_count == nb, f"La fonction 'tools_elec.lecture_octet' doit être appelée {nb} fois"

    @pytest.mark.parametrize("nb", [
        pytest.param(5, id="Test pour 5 mesures"),
        pytest.param(10, id="Test pour 5 mesures"),
    ])
    def test_appel_timestamp(self, datadir, nb):
        data = tools_tests.lecture_fichier_yaml(datadir[f"data1.yaml"])
        with mock.patch("tools_elec.lecture_octet", side_effect=data["valeurs"]) as mock_lecture_octet, \
                mock.patch("tools_date_heure.timestamp", side_effect=data["timestamps"]) as mock_timestamp, \
                mock.patch("bd.inserer_valeur") as mock_inserer_valeur, \
                mock.patch("bd.connecter_mariadb") as mock_connecter_mariadb, \
                mock.patch("sae24.lecture_configuration",
                           return_value={"port": "COM1", "periode": 1}) as mock_lecture_configuration:
            sae24.acquisition(nb)
        assert mock_timestamp.call_count == nb, f"La fonction 'tools_date_heure.timestamp' doit être appelée {nb} fois"

    @pytest.mark.parametrize("nb", [
        pytest.param(5, id="Test pour 5 mesures"),
        pytest.param(10, id="Test pour 5 mesures"),
    ])
    def test_appel_inserer_valeur(self, datadir, nb):
        data = tools_tests.lecture_fichier_yaml(datadir[f"data1.yaml"])
        with mock.patch("tools_elec.lecture_octet", side_effect=data["valeurs"]) as mock_lecture_octet, \
                mock.patch("tools_date_heure.timestamp", side_effect=data["timestamps"]) as mock_timestamp, \
                mock.patch("bd.inserer_valeur") as mock_inserer_valeur, \
                mock.patch("bd.connecter_mariadb") as mock_connecter_mariadb, \
                mock.patch("sae24.lecture_configuration",
                           return_value={"port": "COM1", "periode": 1}) as mock_lecture_configuration:
            sae24.acquisition(nb)
        assert mock_inserer_valeur.call_count == nb, f"La fonction 'bd.inserer_valeur' doit être appelée {nb} fois"

    @pytest.mark.parametrize("nb, cas", [
        pytest.param(20, 1, id="Test pour 5 mesures avec les donnees 1"),
        pytest.param(15, 2, id="Test pour 15 mesures avec les donnees 2"),
    ])
    def test_conversion(self, datadir, nb, cas):
        data = tools_tests.lecture_fichier_yaml(datadir[f"data{cas}.yaml"])
        with mock.patch("tools_elec.lecture_octet", side_effect=data["valeurs"]), \
                mock.patch("tools_date_heure.timestamp", side_effect=data["timestamps"]), \
                mock.patch("bd.inserer_valeur") as mock_inserer_valeur, \
                mock.patch("bd.connecter_mariadb") as mock_connecter_mariadb, \
                mock.patch("sae24.conversion", side_effect=lambda x: x) as mock_conversion, \
                mock.patch("sae24.lecture_configuration",
                           return_value={"port": "COM1", "periode": 1}) as mock_lecture_configuration:
            sae24.acquisition(nb)
        assert mock_conversion.call_count == nb, f"La fonction 'sae24.conversion' doit être appelée {nb} fois"

    @pytest.mark.parametrize("nb, cas", [
        pytest.param(20, 1, id="Test pour 5 mesures avec les donnees 1"),
        pytest.param(15, 2, id="Test pour 15 mesures avec les donnees 2"),
    ])
    def test_insertion_bd(self, datadir, nb, cas):
        data = tools_tests.lecture_fichier_yaml(datadir[f"data{cas}.yaml"])
        with mock.patch("tools_elec.lecture_octet", side_effect=data["valeurs"]), \
                mock.patch("tools_date_heure.timestamp", side_effect=data["timestamps"]), \
                mock.patch("bd.inserer_valeur") as mock_inserer_valeur, \
                mock.patch("bd.connecter_mariadb") as mock_connecter_mariadb, \
                mock.patch("sae24.conversion", side_effect=lambda x: x) as mock_conversion, \
                mock.patch("sae24.lecture_configuration",
                           return_value={"port": "COM1", "periode": 1}) as mock_lecture_configuration:
            sae24.acquisition(nb)

        appels_inserer_valeur = [[call[0][1], call[0][2], call[0][3]] for call in mock_inserer_valeur.call_args_list]
        res = tools_tests.lecture_fichier_yaml(datadir[f"resultats{cas}.yaml"])
        assert res == appels_inserer_valeur, "Les appels à la fonction inserer_valeur ne sont pas comformes"
