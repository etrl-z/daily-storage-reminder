import json
import openpyxl
import emailhelper

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "config.json"


def carica_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def carica_soglie(sheet_soglie, config):

    soglie = {}
    indexes = config["indexes_soglie"]

    for row in sheet_soglie.iter_rows(
        min_row=indexes["first_row"],
        values_only=True
    ):
        articolo = row[indexes["index_articolo"]]
        soglia = row[indexes["index_soglia"]]

        if articolo is None:
            continue

        if soglia is None:
            continue

        soglie[articolo] = soglia

    return soglie


def controlla_giacenza(config):

    excel_file = config["excel_file_path"]

    workbook = openpyxl.load_workbook(
        excel_file,
        data_only=True
    )

    sheet_magazzino = workbook[
        config["sheet_name_magazzino"]
    ]

    sheet_soglie = workbook[
        config["sheet_name_soglie"]
    ]

    indexes = config["indexes_magazzino"]

    # Carico tutte le soglie
    soglie = carica_soglie(sheet_soglie, config)

    articoli_da_riordinare = []

    # Controllo il magazzino
    for row in sheet_magazzino.iter_rows(
        min_row=indexes["first_row"],
        values_only=True
    ):

        articolo = row[indexes["index_articolo"]]
        giacenza = row[indexes["index_giacenza"]]

        if not articolo:
            continue

        if giacenza is None:
            continue

        # Cerco la soglia dell'articolo
        soglia = soglie.get(articolo)

        if soglia is None:
            print(
                f"[ATTENZIONE] "
                f"Nessuna soglia trovata per {articolo}"
            )
            continue

        print(
            f"{articolo}: "
            f"giacenza={giacenza}, "
            f"soglia={soglia}"
        )

        # Articolo sotto soglia
        if giacenza <= soglia:

            articoli_da_riordinare.append({
                "articolo": articolo,
                "giacenza": giacenza,
                "soglia": soglia
            })

    workbook.close()

    # Se ci sono articoli da riordinare
    if articoli_da_riordinare:

        try:

            emailhelper.invia_email(
                config,
                articoli_da_riordinare
            )

        except Exception as e:

            print(
                f"[ERRORE EMAIL] {e}"
            )

    else:

        print(
            "Nessun articolo necessita di rifornimento."
        )


def main():

    print("================================")
    print(" Controllo Magazzino")
    print("================================")

    config = carica_config()

    try:
        print("\nControllo magazzino...")

        controlla_giacenza(config)

        print("\nControllo completato.")

    except Exception as e:

        print(
            f"[ERRORE] {e}"
        )


if __name__ == "__main__":
    main()
