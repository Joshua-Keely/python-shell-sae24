try:
    import colorama

    colorama.init()
    COULEURS_MESSAGE = {"ini": colorama.Fore.BLACK + colorama.Back.YELLOW + colorama.Style.BRIGHT,
                        "fin": colorama.Style.RESET_ALL}
except:
    COULEURS_MESSAGE = {"ini": "", "fin": ""}

import json
import re

import yaml

__CSV_PATTERN = re.compile(r" +;")


# *************************************************************************
def affiche_message_erreur(message):
    """Met en couleur les messages affichés lorsque les tests sont en erreur"""
    # return "\n" + COULEURS_MESSAGE["ini"] + "⚠ " + message + "\n" + COULEURS_MESSAGE["fin"]
    return message  # pour les partiels machines


# *************************************************************************
def lecture_lignes_fichier_csv(file):
    """Lecture d'une liste depuis un fichier json"""
    if isinstance(file, str):
        with open(file, encoding="utf8") as fh:
            res = fh.readlines()
    else:
        res = file.open("r", encoding="utf8").readlines()
    return [__CSV_PATTERN.sub(";", r.strip()) for r in res if r.strip() != ""]


# *************************************************************************
def lecture_fichier_json(file):
    """Lecture d'un dictionaire depuis un fichier json"""
    if isinstance(file, str):
        with open(file, encoding="utf8") as fh:
            return json.load(fh)
    else:
        return json.load(file.open("rb"))


# *************************************************************************
def lecture_fichier_yaml(file):
    """Lecture d'un dictionaire depuis un fichier yaml"""
    if isinstance(file, str):
        with open(file, encoding="utf8") as fh:
            return yaml.load(fh, Loader=yaml.SafeLoader)
    else:
        return yaml.load(file.open("rb"), Loader=yaml.SafeLoader)


def lecture_fichier(file):
    """Lecture d'un fichier texte depuis un fichier json"""
    with open(str(file), encoding="UTF-8") as fd:
        content = fd.read()
        return content


# *************************************************************************
__TEXT_PATTERNS = [
    (re.compile(r"\s+$", re.MULTILINE), "\n"),
    (re.compile(r"\n+"), "\n"),
    (re.compile(r"\n+$"), ""),
    (re.compile(r"^\n+"), ""),
]


def nettoyage_chaine(txt):
    """
    Suppression des espaces en fin de chaine

    :param txt: chaîne à nettoyer
    ;:type txt: str
    :return: chaîne nettoyée
    :rtype: str
    """
    for pat, repl in __TEXT_PATTERNS:
        txt = pat.sub(repl, txt)

    return txt


MESSAGE_ERREUR_CONSOLE = "L'affichage console n'est pas correct à partir de la ligne "


# Utilitaire pour les tests
def remove_first_ligne(carre):
    return "\n".join(carre.split("\n")[1:])


def remove_space(motif):
    lignes = motif.split("\n")
    return "\n".join([l.rstrip() for l in lignes])
