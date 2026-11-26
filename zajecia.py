from baza import zapisz_baze


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
