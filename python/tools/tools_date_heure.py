"""
===========================
Module `tools_date_heure`
===========================

A télécharger :download:`ici <../../../../python/tools/tools_date_heure.py>`.

"""

from datetime import datetime, timedelta

ISO_FORMAT = "%Y-%m-%d %H:%M:%S"


def timestamp() -> int:
    """
    Retourne la valeur du timestamp actuel.
    """
    return int(datetime.now().timestamp())


def maintenant() -> str:
    """
    Retourne la date et l'heure actuelle au format iso.
    """
    return datetime.now().strftime(ISO_FORMAT)


def il_y_a(minutes: int) -> str:
    """
    Retourne la date et l'heure d'il y a `minutes` minutes au format iso.

    :param minutes: le nombre de minutes avant maintenant
    """
    d = datetime.now() - timedelta(minutes=minutes)
    return d.strftime(ISO_FORMAT)


def formatage_iso(d: datetime) -> str:
    """
    Retourne la date au format iso de l'objet datetime passé en paramètre.

    :param d: un objet de type `datetime`
    :return: la date au format iso
    """
    return d.strftime(ISO_FORMAT)


def formatage_timestamp_iso(ts: int) -> str:
    """
    Retourne la date au format iso du timestamp passé en paramètre.

    :param d: un objet de type `datetime`
    :return: la date au format iso
    """
    return datetime.fromtimestamp(ts).strftime(ISO_FORMAT)
