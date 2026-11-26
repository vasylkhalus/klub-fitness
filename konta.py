import hashlib

from baza import zapisz_baze


def zahashuj_haslo(haslo: str) -> str:
    return hashlib.sha256(haslo.encode("utf-8")).hexdigest()


def rejestracja(baza: dict):
    print("\n--- REJESTRACJA ---")
    uzytkownicy = baza["uzytkownicy"]
    login = input("Podaj nowy login: ").strip()

    if not login:
        print("Błąd: Login nie może być pusty.")
        return

    if login in uzytkownicy:
        print("Błąd: Użytkownik o takim loginie już istnieje.")
        return

    haslo = input("Podaj hasło: ").strip()
    if len(haslo) < 4:
        print("Błąd: Hasło musi mieć minimum 4 znaki.")
        return

    powtorz_haslo = input("Powtórz hasło: ").strip()
    if haslo != powtorz_haslo:
        print("Błąd: Hasła nie są identyczne.")
        return

    print("Wybierz typ konta: 1 - Klubowicz | 2 - Trener")
    wybor_roli = input("Rola (domyślnie 1): ").strip()
    rola = "trener" if wybor_roli == "2" else "klubowicz"

    uzytkownicy[login] = {
        "haslo": zahashuj_haslo(haslo),
        "rola": rola,
        "karnet_do": None,
    }

    zapisz_baze(baza)
    print(f"Konto '{login}' ({rola}) zostało utworzone!")


def logowanie(baza: dict):
    print("\n--- LOGOWANIE ---")
    login = input("Login: ").strip()
    haslo = input("Hasło: ").strip()

    dane_uzytkownika = baza["uzytkownicy"].get(login)

    if dane_uzytkownika and dane_uzytkownika["haslo"] == zahashuj_haslo(haslo):
        print(
            f"\nZalogowano pomyślnie! Witaj w klubie, {login} (rola: {dane_uzytkownika['rola']})."
        )
        return login
    else:
        print("Błąd: Nieprawidłowy login lub hasło.")
        return None


def usun_uzytkownika_z_bazy(login_do_usuniecia: str, baza: dict):
    """Usuwa użytkownika ze słownika oraz wypisuje go ze wszystkich zajęć."""
    if login_do_usuniecia in baza["uzytkownicy"]:
        del baza["uzytkownicy"][login_do_usuniecia]

        for z in baza["zajecia"]:
            if login_do_usuniecia in z["zapisani"]:
                z["zapisani"].remove(login_do_usuniecia)

        zapisz_baze(baza)
        print(f"Konto '{login_do_usuniecia}' zostało trwale usunięte.")
