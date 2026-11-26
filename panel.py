from karnety import czy_karnet_aktywny, kup_karnet
from konta import usun_uzytkownika_z_bazy
from zajecia import (
    anuluj_rezerwacje,
    dodaj_zajecia_trener,
    wyswietl_harmonogram,
    zarezerwuj_zajecia,
)


def panel_uzytkownika(login: str, baza: dict):
    dane = baza["uzytkownicy"][login]

    while True:
        print(f"\n=== PANEL UŻYTKOWNIKA: {login.upper()} ({dane['rola']}) ===")
        if dane["rola"] == "klubowicz":
            if czy_karnet_aktywny(dane):
                status_karnetu = f"Aktywny (ważny do {dane['karnet_do']})"
            else:
                status_karnetu = "Brak aktywnego karnetu"

            print(f"Status karnetu: {status_karnetu}")
            print("1. Przeglądaj harmonogram zajęć")
            print("2. Zarezerwuj miejsce na zajęciach")
            print("3. Moje rezerwacje / Odwołaj rezerwację")
            print("4. Kup karnet")
            print("5. Usuń moje konto")
            print("6. Wyloguj")

            wybor = input("Wybór: ").strip()
            if wybor == "1":
                wyswietl_harmonogram(baza, login)
            elif wybor == "2":
                zarezerwuj_zajecia(login, baza)
            elif wybor == "3":
                anuluj_rezerwacje(login, baza)
            elif wybor == "4":
                kup_karnet(dane, baza)
            elif wybor == "5":
                potwierdzenie = (
                    input("Czy na pewno chcesz usunąć konto? (tak/nie): ")
                    .strip()
                    .lower()
                )
                if potwierdzenie == "tak":
                    usun_uzytkownika_z_bazy(login, baza)
                    break
            elif wybor == "6":
                print("Wylogowano.")
                break
            else:
                print("Nieznana opcja.")

        elif dane["rola"] == "trener":
            print("1. Przeglądaj harmonogram i listy zapisanych")
            print("2. Dodaj nowe zajęcia do harmonogramu")
            print("3. Wyświetl listę klubowiczów")
            print("4. Usuń klubowicza")
            print("5. Wyloguj")

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
                            f"Aktywny (do {u_dane['karnet_do']})"
                            if czy_karnet_aktywny(u_dane)
                            else "Nieaktywny"
                        )
                        print(f"- {u_login} (karnet: {status})")
            elif wybor == "4":
                cel = input(
                    "Podaj login klubowicza do usunięcia: "
                ).strip()
                if cel not in baza["uzytkownicy"]:
                    print("Błąd: Nie ma takiego użytkownika.")
                elif baza["uzytkownicy"][cel]["rola"] != "klubowicz":
                    print("Błąd: Możesz usuwać tylko konta klubowiczów.")
                else:
                    usun_uzytkownika_z_bazy(cel, baza)
            elif wybor == "5":
                print("Wylogowano.")
                break
            else:
                print("Nieznana opcja.")
