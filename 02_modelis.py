"""Apmāca vienu Random Forest modeli un salīdzina to ar bāzes līniju."""

from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split

MAPE = Path(__file__).resolve().parent
DATI = MAPE / "tirs.csv"
MERKIS = "sirds_slimiba"
PAZIMES = [
    "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
    "thalach", "exang", "oldpeak", "slope", "ca", "thal",
]


def main() -> None:
    if not DATI.is_file():
        raise FileNotFoundError("Nav tirs.csv. Vispirms palaid: python 01_tirisana.py")

    # Nolasa tikai tīros datus, ko izveidoja pirmais skripts.
    dati = pd.read_csv(DATI)
    if dati[PAZIMES + [MERKIS]].isna().any().any():
        raise ValueError("Tīrajā failā ir trūkstošas vērtības.")

    # Izmanto tikai 13 mērījumus, jo mērķa klase un avota rindas numurs nedrīkst būt modeļa ievade.
    X = dati[PAZIMES]
    y = dati[MERKIS].astype(int)
    rindas = dati["avota_rinda"].astype(int)

    # Sadala datus 75 % apmācībai un 25 % testēšanai, saglabājot klašu proporciju.
    X_train, X_test, y_train, y_test, _, rindas_test = train_test_split(
        X, y, rindas, test_size=0.25, random_state=42, stratify=y
    )

    # Nosaka biežāko klasi tikai apmācības datos, lai testa atbildes neietekmētu bāzes līniju.
    biezaka_klase = int(y_train.value_counts().idxmax())

    # Bāzes līnija katrai testa rindai min vienu un to pašu apmācības kopas biežāko klasi.
    bazes_precizitate = accuracy_score(y_test, [biezaka_klase] * len(y_test))

    # Apmāca vienu scikit-learn Random Forest klasifikatoru ar fiksētu nejaušības sēklu.
    modelis = RandomForestClassifier(
        n_estimators=300,
        max_depth=5,
        min_samples_leaf=3,
        class_weight="balanced",
        random_state=42,
    )
    modelis.fit(X_train, y_train)

    # Pārbauda modeli tikai ar testa kopu, kas netika izmantota tā apmācībai.
    prognozes = modelis.predict(X_test)
    precizitate = accuracy_score(y_test, prognozes)

    # Nosaka divas svarīgākās ievades kolonnas pēc Random Forest aprēķinātā nozīmīguma.
    svarigums = pd.Series(
        modelis.feature_importances_, index=PAZIMES
    ).sort_values(ascending=False)

    # Atrod pirmo kļūdaino testa rindu, lai varētu izskaidrot vienu konkrētu kļūdu.
    kludas_pozicijas = [
        i for i, (istais, minetais) in enumerate(zip(y_test, prognozes))
        if istais != minetais
    ]

    print("=== MODEĻA REZULTĀTI ===")
    print(f"Apmācības rindas: {len(X_train)}, testa rindas: {len(X_test)}")
    print(f"Biežākā apmācības klase (bāzes līnija): {biezaka_klase}")
    print(f"Modeļa precizitāte: {precizitate:.4f} ({precizitate:.1%})")
    print(f"Bāzes līnijas precizitāte: {bazes_precizitate:.4f} ({bazes_precizitate:.1%})")
    print(f"Atšķirība: {(precizitate - bazes_precizitate) * 100:+.1f} procentpunkti")
    if precizitate > bazes_precizitate:
        print("Secinājums: modelis pārspēj bāzes līniju šajā testa kopā.")
    else:
        print("Secinājums: modelis bāzes līniju šajā testa kopā nepārspēj.")

    print("Divas svarīgākās kolonnas:")
    for nosaukums, vertiba in svarigums.head(2).items():
        print(f"  {nosaukums}: {vertiba:.4f}")

    print(f"Kļūdaino testa prognožu skaits: {len(kludas_pozicijas)}")
    print("Jucekļa matrica [faktiskā klase x prognozētā klase] (0, 1):")
    print(confusion_matrix(y_test, prognozes, labels=[0, 1]))

    if kludas_pozicijas:
        i = kludas_pozicijas[0]
        print(f"Kļūdas piemērs — oriģinālā CSV rinda: {int(rindas_test.iloc[i])}")
        print(f"  Faktiskā klase: {int(y_test.iloc[i])}")
        print(f"  Modeļa prognoze: {int(prognozes[i])}")
        print("  Pazīmes:")
        for nosaukums, vertiba in X_test.iloc[i].items():
            print(f"    {nosaukums}: {vertiba:g}")
    else:
        print("Šajā testa sadalījumā kļūdainu prognožu nav.")


if __name__ == "__main__":
    main()
