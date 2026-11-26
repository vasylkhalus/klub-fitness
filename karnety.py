from datetime import date, timedelta

from baza import zapisz_baze


def czy_karnet_aktywny(dane_uzytkownika: dict) -> bool:
    """Sprawdza, czy użytkownik posiada ważny karnet."""
    karnet_do = dane_uzytkownika.get("karnet_do")
    if not karnet_do:
        return False
    return date.today() <= date.fromisoformat(karnet_do)


def kup_karnet(dane: dict, baza: dict):
    if czy_karnet_aktywny(dane):
        print(f"\nMasz już aktywny karnet ważny do {dane['karnet_do']}.")
        print("Nowy karnet możesz kupić dopiero po wygaśnięciu obecnego.")
        return

    print("\n--- ZAKUP KARNETU ---")
    print("1. Karnet miesięczny (30 dni)")
    print("2. Karnet roczny (365 dni)")
    print("0. Anuluj")

    wybor = input("Wybierz rodzaj karnetu: ").strip()

    if wybor == "1":
        dni = 30
        typ = "miesięczny"
    elif wybor == "2":
        dni = 365
        typ = "roczny"
    elif wybor == "0":
        return
    else:
        print("Błąd: Nieprawidłowy wybór.")
        return

    data_konca = date.today() + timedelta(days=dni)
    dane["karnet_do"] = data_konca.isoformat()
    zapisz_baze(baza)
    print(f"Kupiono karnet {typ}! Ważny do: {dane['karnet_do']}.")
