from baza import wczytaj_baze
from konta import logowanie, rejestracja
from panel import panel_uzytkownika
from zajecia import wyswietl_harmonogram


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
