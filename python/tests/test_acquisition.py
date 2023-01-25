import inspect
import random

import mock
import pytest

import tools_introspection
import tools_tests

try:
    import acquisition
except:
    pass

MODULE = "acquisition"


# ************************************************************************************************
class TestStructure:

    def test_import_module(self):
        message = "{} n'a pas pu être importé pour les tests\n" \
                  "➔ Vérifiez que votre code n'a pas d'erreurs syntaxiques (vaguettes rouges)".format(MODULE)
        try:
            import acquisition
        except:
            assert False, tools_tests.affiche_message_erreur(message)

    # ---
    def test_declaration_main(self):
        FONCTION = "main"
        message = "Le programme principal {}.{} doit être déclaré".format(MODULE, FONCTION)
        liste = inspect.getmembers(acquisition)
        assert FONCTION in [liste[i][0] for i in range(len(liste))], \
            tools_tests.affiche_message_erreur(message)


class TestAcquerir:
    FONCTION = "acquerir"

    # ---
    def test_declaration_fonction(self):
        message = "La fonction {}.{} doit être déclarée".format(MODULE, self.FONCTION)
        liste = inspect.getmembers(acquisition)
        assert self.FONCTION in [liste[i][0] for i in range(len(liste))], \
            tools_tests.affiche_message_erreur(message)

    # ---
    def test_nombre_parametres(self):
        nb_params = 2
        """Teste le nombre de paramètres de la fonction"""
        message = "La fonction {}.{} doit avoir {} paramètre".format(MODULE, self.FONCTION, nb_params)
        fct = tools_introspection.get_fonction_from_module(self.FONCTION, acquisition)
        assert len(inspect.signature(fct).parameters) == nb_params, \
            tools_tests.affiche_message_erreur(message)

    def test_type_valeur_retour(self):
        """Teste le type de la valeur de retour"""
        with mock.patch("tools_elec.lecture_octet", return_value=0) as mocked_func:
            res = acquisition.acquerir("port", 100)
        assert isinstance(res, list), "La fonction doit renvoyer une liste"
        assert len(res) == 100, "La fonction doit renvoyer une liste de 100 éléments"

    @pytest.mark.parametrize("nb_points", [100, 200])
    def test_nombre_valeurs_renvoyes(self, nb_points):
        """Teste si le nombre données renvoyé est correct"""
        with mock.patch("tools_elec.lecture_octet", return_value=0) as mocked_func:
            res = acquisition.acquerir("port", nb_points)
        assert len(res) == nb_points, \
            f"La fonction doit renvoyer {nb_points} dates lors que le paramètres est {nb_points}"

    @pytest.mark.parametrize("nb_points", [100, 200])
    def test_appel_lecture_octet(self, nb_points):
        """Teste si le nombre données renvoyé est correct"""
        with mock.patch("tools_elec.lecture_octet", return_value=0) as mocked_func:
            res = acquisition.acquerir("port", nb_points)
        assert mocked_func.call_count == nb_points, \
            f"La fonction doit effectuer {nb_points} appels a tools_elec.lecture_octet " \
            f"lors que le paramètres est {nb_points}"

    @pytest.mark.parametrize("nb_points", [100, 200])
    def test_appel_init_acquisition(self, nb_points):
        """Teste si le nombre données renvoyé est correct"""
        with mock.patch("tools_elec.init_acquisition") as mocked_func, \
                mock.patch("tools_elec.lecture_octet", return_value=0):
            acquisition.acquerir("port", nb_points)
            assert mocked_func.call_count == 1

    @pytest.mark.parametrize("nb_points", [100, 200])
    @pytest.mark.parametrize("fonction", ["sinus", "carre", "triangle"])
    def test_nombre_valeurs_renvoyes_simules(self, nb_points, fonction):
        """Teste si le nombre données renvoyé est correct"""
        res = acquisition.acquerir(fonction, nb_points)
        assert len(res) == nb_points, \
            f"La fonction doit renvoyer {nb_points} dates lors que le paramètres est {nb_points}"

    @pytest.mark.parametrize("nb_valeurs", [10, 25])
    def test_valeur_retour(self, nb_valeurs):
        """Teste si la liste des données est correcte"""
        values = [random.randint(0, 255) for i in range(nb_valeurs)]
        expected_values = values.copy()
        with mock.patch("tools_elec.lecture_octet", side_effect=lambda: values.pop(0)):
            actual = acquisition.acquerir("COM1", nb_valeurs)
        assert actual == expected_values, "La liste des valeurs n'est pas correcte"

    @pytest.mark.parametrize("nb_valeurs", [10, 25])
    @pytest.mark.parametrize("fonction", ["sinus", "carre", "triangle"])
    def test_valeur_retour_simules(self, datadir, nb_valeurs, fonction):
        """Teste si la liste des données est correcte"""
        expected_values = tools_tests.lecture_fichier_yaml(datadir[f"{fonction}.yaml"])[:nb_valeurs]
        actual = acquisition.acquerir(fonction, nb_valeurs)
        assert actual == expected_values, "La liste des valeurs n'est pas correcte"
