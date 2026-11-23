"""Sakārto UCI Heart Disease (Cleveland) datus, neskarot oriģinālu."""

import json
from pathlib import Path

import pandas as pd

MAPE = Path(__file__).resolve().parent
AVOTS = MAPE / "dati" / "processed.cleveland.data"
TIRAIS_FAILS = MAPE / "tirs.csv"
STATISTIKA = MAPE / "tirisanas_statistika.json"

# UCI oriģinālajā failā nav galvenes, tāpēc kolonnu nosaukumi jānorāda pašiem.
KOLONNAS = [
    "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
    "thalach", "exang", "oldpeak", "slope", "ca", "thal", "num",
]


def main() -> None:
    if not AVOTS.is_file():
        raise FileNotFoundError(f"Nav atrasts sākotnējais datu fails: {AVOTS}")

    # Nolasa visas Cleveland CSV vērtības kā tekstu, lai '?' pazīmes nepazustu pirms pārbaudes.
    sakotnejie = pd.read_csv(
        AVOTS, header=None, names=KOLONNAS, dtype=str, keep_default_na=False
    )
    pirms = len(sakotnejie)

    # Pievieno oriģinālā faila rindas numuru, lai vēlāk varētu atrast konkrētu kļūdainu piemēru.
    sakotnejie.insert(0, "avota_rinda", range(1, pirms + 1))

    # Aizstāj '?' un tukšās vērtības ar trūkstošu datu marķieri, jo UCI failā nezināmas vērtības ir norādītas ar '?'.
    teksts = sakotnejie[KOLONNAS].replace({"?": pd.NA, "": pd.NA})

    # Pārvērš medicīnisko pazīmju vērtības skaitļos, lai modelis varētu tās apstrādāt.
    skaitli = teksts.apply(pd.to_numeric, errors="coerce")

    # Atzīmē rindas ar citu nederīgu tekstu, lai tās nenoņemtu pie '?' trūkumu skaita.
    nederigas = (teksts.notna() & skaitli.isna()).any(axis=1)
    izmestas_nederigas = int(nederigas.sum())

    # Izņem nekonvertējamās rindas, jo modelim nedrīkst nodot kļūdainus skaitļus.
    skaitli = skaitli.loc[~nederigas].copy()

    # Atzīmē rindas ar nezināmu mērījumu, jo šajā mācību projektā izmantosim tikai pilnus ierakstus.
    trukst = skaitli.isna().any(axis=1)
    izmestas_trukstosas = int(trukst.sum())

    # Izņem rindas ar trūkstošiem mērījumiem, nepārveidojot oriģinālo failu.
    skaitli = skaitli.loc[~trukst].copy()

    # Atrod pilnīgi vienādus ierakstus pēc 14 sākotnējām kolonnām, neņemot vērā rindas numuru.
    dublikati = skaitli.duplicated(subset=KOLONNAS)
    izmesti_dublikati = int(dublikati.sum())

    # Izņem konstatētos dublikātus, lai viens pilnīgi identisks ieraksts neatkārtotos datu kopā.
    skaitli = skaitli.loc[~dublikati].copy()

    # Pārbauda mērķa etiķetes, jo UCI Cleveland 'num' ir atļautas tikai vērtības no 0 līdz 4.
    if not skaitli["num"].isin([0, 1, 2, 3, 4]).all():
        raise ValueError("Kolonnā 'num' ir neparedzēta mērķa vērtība.")

    # Saglabā sākotnējās rindas numuru, lai tīrajos datos būtu atsauce uz avota ierakstu.
    skaitli.insert(0, "avota_rinda", sakotnejie.loc[skaitli.index, "avota_rinda"])

    # Izveido divu klašu mērķi: 0 nozīmē slimības neesamību, bet 1 apvieno sākotnējās vērtības 1–4.
    skaitli["sirds_slimiba"] = (skaitli["num"] > 0).astype(int)

    # Izņem sākotnējo 'num' kolonnu, lai modelis neredzētu atbildi ievades pazīmēs.
    skaitli = skaitli.drop(columns=["num"])

    # Saglabā sakārtotos ierakstus atsevišķā CSV failā, neaiztiekot UCI oriģinālu mapē 'dati'.
    skaitli.to_csv(TIRAIS_FAILS, index=False)

    pec = len(skaitli)
    skaitijums = {
        "sakuma": pirms,
        "izmestas_nederigas": izmestas_nederigas,
        "izmestas_trukstosas": izmestas_trukstosas,
        "izmesti_dublikati": izmesti_dublikati,
        "beigas": pec,
    }

    # Saglabā tīrīšanas rindu skaitu JSON failā, lai secinājumu skaitļus varētu pārbaudīt.
    STATISTIKA.write_text(
        json.dumps(skaitijums, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(f"Rindu skaits sākumā: {pirms}")
    print(f"Izmestas rindas ar nekonvertējamām vērtībām: {izmestas_nederigas}")
    print(f"Izmestas rindas ar trūkstošām vērtībām: {izmestas_trukstosas}")
    print(f"Izmestas dublētas rindas: {izmesti_dublikati}")
    print(f"Kopā izmestas rindas: {pirms - pec}")
    print(f"Rindu skaits beigās: {pec}")
    print(f"Saglabāts: {TIRAIS_FAILS.name}")


if __name__ == "__main__":
    main()
