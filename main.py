import hashlib
import json
import os

PLIK_BAZY = "baza_klubu.json"


# ==========================================
# #4: SCHEMAT STRUKTURY JSON I OBSŁUGA PLIKU
# ==========================================
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


# ==========================================
# #6: REJESTRACJA I LOGOWANIE UŻYTKOWNIKÓW
# ==========================================
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
        "karnet_aktywny": False if rola == "klubowicz" else None,
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


# ==========================================
# #7: PRZEGLĄDANIE HARMONOGRAMU ZAJĘĆ
# ==========================================
def wyswietl_harmonogram(baza: dict, aktualny_login: str = None):
    print("\n--- HARMONOGRAM ZAJĘĆ ---")
    zajecia = baza.get("zajecia", [])

    if not zajecia:
        print("Brak zaplanowanych zajęć w harmonogramie.")
        return

    for z in zajecia:
        zajete = len(z["zapisani"])
        limit = z["limit_miejsc"]
        wolne = limit - zajete
        status_zapisu = ""

        if aktualny_login and aktualny_login in z["zapisani"]:
            status_zapisu = " [JESTEŚ ZAPISANY/A]"

        print(
            f"[{z['id']}] {z['nazwa']} | Termin: {z['termin']} | "
            f"Trener: {z['trener']} | Wolne miejsca: {wolne}/{limit}{status_zapisu}"
        )


# ==========================================
# #8: REZERWACJA MIEJSCA NA ZAJĘCIACH
# ==========================================
def zarezerwuj_zajecia(login: str, baza: dict):
    wyswietl_harmonogram(baza, login)
    zajecia = baza.get("zajecia", [])

    if not zajecia:
        return

    try:
        wybrane_id = int(
            input("\nPodaj ID zajęć do rezerwacji (0 aby anulować): ").strip()
        )
    except ValueError:
        print("Błąd: Podaj poprawny numer ID.")
        return

    if wybrane_id == 0:
        return

    wybrane_zajecia = next((z for z in zajecia if z["id"] == wybrane_id), None)

    if not wybrane_zajecia:
        print("Błąd: Nie znaleziono zajęć o podanym ID.")
        return

    if login in wybrane_zajecia["zapisani"]:
        print("Już jesteś zapisany/a na te zajęcia.")
        return

    if len(wybrane_zajecia["zapisani"]) >= wybrane_zajecia["limit_miejsc"]:
        print("Brak wolnych miejsc na wybrane zajęcia.")
        return

    wybrane_zajecia["zapisani"].append(login)
    zapisz_baze(baza)
    print(
        f"Sukces! Zarezerwowano miejsce na: {wybrane_zajecia['nazwa']} ({wybrane_zajecia['termin']})."
    )


def anuluj_rezerwacje(login: str, baza: dict):
    moje_zajecia = [z for z in baza["zajecia"] if login in z["zapisani"]]

    if not moje_zajecia:
        print("\nNie jesteś zapisany/a na żadne zajęcia.")
        return

    print("\n--- TWOJE REZERWACJE ---")
    for z in moje_zajecia:
        print(f"[{z['id']}] {z['nazwa']} | {z['termin']}")

    try:
        wybrane_id = int(
            input("Podaj ID zajęć do odwołania (0 aby wrócić): ").strip()
        )
    except ValueError:
        print("Błąd: Podaj poprawny numer ID.")
        return

    if wybrane_id == 0:
        return

    zajecia_do_anulowania = next(
        (z for z in moje_zajecia if z["id"] == wybrane_id), None
    )
    if zajecia_do_anulowania:
        zajecia_do_anulowania["zapisani"].remove(login)
        zapisz_baze(baza)
        print(f"Odwołano rezerwację na: {zajecia_do_anulowania['nazwa']}.")
    else:
        print("Błąd: Nie masz rezerwacji na zajęcia o tym ID.")


def dodaj_zajecia_trener(login: str, baza: dict):
    print("\n--- DODAWANIE NOWYCH ZAJĘĆ ---")
    nazwa = input("Nazwa zajęć: ").strip()
    termin = input("Termin (np. Czwartek 18:00): ").strip()

    try:
        limit = int(input("Limit miejsc: ").strip())
        if limit <= 0:
            raise ValueError
    except ValueError:
        print("Błąd: Limit miejsc musi być liczbą dodatnią.")
        return

    nowe_id = max((z["id"] for z in baza["zajecia"]), default=0) + 1
    baza["zajecia"].append(
        {
            "id": nowe_id,
            "nazwa": nazwa,
            "termin": termin,
            "trener": login,
            "limit_miejsc": limit,
            "zapisani": [],
        }
    )
    zapisz_baze(baza)
    print(f"Dodano zajęcia '{nazwa}' (ID: {nowe_id}) do harmonogramu.")


# ==========================================
# PANEL UŻYTKOWNIKA I MENU GŁÓWNE
# ==========================================
def panel_uzytkownika(login: str, baza: dict):
    dane = baza["uzytkownicy"][login]

    while True:
        print(f"\n=== PANEL UŻYTKOWNIKA: {login.upper()} ({dane['rola']}) ===")
        if dane["rola"] == "klubowicz":
            status_karnetu = (
                "Aktywny" if dane["karnet_aktywny"] else "Brak aktywnego karnetu"
            )
            print(f"Status karnetu: {status_karnetu}")
            print("1. Przeglądaj harmonogram zajęć")
            print("2. Zarezerwuj miejsce na zajęciach")
            print("3. Moje rezerwacje / Odwołaj rezerwację")
            print("4. Kup / przedłuż karnet")
            print("5. Wyloguj")

            wybor = input("Wybór: ").strip()
            if wybor == "1":
                wyswietl_harmonogram(baza, login)
            elif wybor == "2":
                zarezerwuj_zajecia(login, baza)
            elif wybor == "3":
                anuluj_rezerwacje(login, baza)
            elif wybor == "4":
                dane["karnet_aktywny"] = True
                zapisz_baze(baza)
                print("Karnet został aktywowany!")
            elif wybor == "5":
                print("Wylogowano.")
                break
            else:
                print("Nieznana opcja.")

        elif dane["rola"] == "trener":
            print("1. Przeglądaj harmonogram i listy zapisanych")
            print("2. Dodaj nowe zajęcia do harmonogramu")
            print("3. Wyświetl listę klubowiczów")
            print("4. Wyloguj")

            wybor = input("Wybór: ").strip()
            if wybor == "1":
                wyswietl_harmonogram(baza, login)
                for z in baza["zajecia"]:
                    zapisani_str = (
                        ", ".join(z["zapisani"]) if z["zapisani"] else "brak"
                    )
                    print(
                        f"   -> Zapisani na [{z['id']}] {z['nazwa']}: {zapisani_str}"
                    )
            elif wybor == "2":
                dodaj_zajecia_trener(login, baza)
            elif wybor == "3":
                print("\nLista klubowiczów:")
                for u_login, u_dane in baza["uzytkownicy"].items():
                    if u_dane["rola"] == "klubowicz":
                        status = (
                            "Aktywny"
                            if u_dane["karnet_aktywny"]
                            else "Nieaktywny"
                        )
                        print(f"- {u_login} (karnet: {status})")
            elif wybor == "4":
                print("Wylogowano.")
                break
            else:
                print("Nieznana opcja.")


def main():
    baza = wczytaj_baze()

    print("Witamy w naszym klubie!")
    print("Czym mozemy pomóc?")

    while True:
        print("\n--- MENU GŁÓWNE ---")
        print("1. Rejestracja")
        print("2. Logowanie")
        print("3. Przeglądaj harmonogram zajęć")
        print("4. Wyjście")

        wybor = input("Twój wybór (1-4): ").strip()

        if wybor == "1":
            rejestracja(baza)
        elif wybor == "2":
            zalogowany_login = logowanie(baza)
            if zalogowany_login:
                panel_uzytkownika(zalogowany_login, baza)
        elif wybor == "3":
            wyswietl_harmonogram(baza)
        elif wybor == "4":
            print("Do zobaczenia w klubie!")
            break
        else:
            print("Nieznana opcja. Wybierz 1, 2, 3 lub 4.")


if __name__ == "__main__":
    main()