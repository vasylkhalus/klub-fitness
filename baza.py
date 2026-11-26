import json
import os

PLIK_BAZY = "baza_klubu.json"


def domyslna_baza() -> dict:
    """Zwraca początkowy schemat struktury JSON z przykładowym harmonogramem."""
    return {
        "uzytkownicy": {},
        "zajecia": [
            {
                "id": 1,
                "nazwa": "CrossFit",
                "termin": "Poniedziałek 18:00",
                "trener": "Marek Kowalski",
                "limit_miejsc": 10,
                "zapisani": [],
            },
            {
                "id": 2,
                "nazwa": "Joga / Mobility",
                "termin": "Środa 17:30",
                "trener": "Anna Nowak",
                "limit_miejsc": 12,
                "zapisani": [],
            },
            {
                "id": 3,
                "nazwa": "Trening Siłowy (FBW)",
                "termin": "Piątek 19:00",
                "trener": "Piotr Wiśniewski",
                "limit_miejsc": 8,
                "zapisani": [],
            },
        ],
    }


def wczytaj_baze() -> dict:
    """Wczytuje bazę z pliku JSON lub tworzy nową według schematu."""
    if not os.path.exists(PLIK_BAZY):
        baza = domyslna_baza()
        zapisz_baze(baza)
        return baza

    try:
        with open(PLIK_BAZY, "r", encoding="utf-8") as plik:
            dane = json.load(plik)
            if "uzytkownicy" not in dane or "zajecia" not in dane:
                return domyslna_baza()
            return dane
    except (json.JSONDecodeError, IOError):
        return domyslna_baza()


def zapisz_baze(baza: dict):
    """Zapisuje całą strukturę JSON do pliku."""
    with open(PLIK_BAZY, "w", encoding="utf-8") as plik:
        json.dump(baza, plik, indent=4, ensure_ascii=False)
