import importlib, inspect, re


def get_fonction_from_module(nom_fonction, module_importe):
    """Renvoie la référence à une fonction dans un module_importe avec importlib"""
    liste = inspect.getmembers(module_importe)  # Récupère un tuple indiquant les objets du test_module (aka bibliotheque_turtle)
    for (k, v) in liste:
        if k == nom_fonction:  # si la fonction est là :)
            return v  # l'id de la fonction
    raise Exception("Fonction de tests %s non trouvée" % nom_fonction)


def get_code_source(nom_module, nom_fonction):
    """Renvoie le code source d'un module"""
    mod = importlib.import_module(nom_module)
    id_fonction = get_fonction_from_module(nom_fonction, mod)
    code_source = inspect.getsource(id_fonction)
    return code_source


def inspect_fonction_d_un_module_nbre_mots(fonction="module.fonction", mot_recherche="for"):
    """Inspect le code_source d'un module à la recherche du nombre d'occurences du mot_recherche"""
    try:
        [nom_module, nom_fonction] = fonction.split(".")
        code_source = get_code_source(nom_module, nom_fonction)
        return inspect_code_nbre_mots(code_source, mot_recherche=mot_recherche)
    except:
        print("{} non trouvée".format(fonction))


def inspect_fonction_d_un_module(fonction="module.fonction", mot_recherche="for"):
    """Inspect le code_source d'un module"""
    try:
        return inspect_fonction_d_un_module_nbre_mots(fonction, mot_recherche=mot_recherche) > 0
    except:
        print("{} non trouvée".format(fonction))


def remove_triple_comment(code_source):
    """Supprime les triples commentaires à condition qu'il ne contienne pas de caractères '"' """
    pattern = r'(""")[^"]*(""")'
    p = re.compile(pattern)
    correspondances = list(p.finditer(code_source))
    for match in correspondances:
        code_source = code_source.replace(match.group(0), "")
    return code_source


def remove_comment(code_source):
    """Supprime les commentaires (ceux débutant par #) """
    pattern = r"""(#)[^\n]*\n"""
    p = re.compile(pattern)
    correspondances = list(p.finditer(code_source))
    for match in correspondances:
        code_source = code_source.replace(match.group(0), "")
    return code_source


def inspect_code_nbre_mots(code_source, mot_recherche="for "):
    """Renvoie le nombre d'occurences du mot_recherche"""
    code_source = remove_triple_comment(code_source)
    code_source = remove_comment(code_source)
    return code_source.count(mot_recherche)


def inspect_code(code_source, mot_recherche="for "):
    """Renvoie le nombre d'occurences du mot_recherche"""
    return inspect_code_nbre_mots(code_source, mot_recherche=mot_recherche) > 0


def main():
    code = 'def carre():\n"""Dessine sur la console un carré  et par unités\n (les colonnes).\n\n:return: None\n"""\nchaine = ""\nfor i : # boucle 1\n   for j : # for\n            chaine = " "\n    chaine += "\n"\nprint(chaine)\n    return None\n'
    print(code)
    print(inspect_code(code, mot_recherche="if "))


if __name__ == "__main__":
    main()
