# Pirmais modelis no nulles

Mācību projekts, kurā no **reāliem, nepilnīgiem datiem** izveidoju vienkāršu
klasifikācijas modeli, pārbaudu tā precizitāti un izskaidroju ierobežojumus.

## Ko projekts dara?

- Nolasa UCI **Heart Disease (Cleveland)** datu kopu ar 303 rindām un 14 kolonnām.
- Atrod `?` trūkstošās vērtības, pārbauda datu tipus un dublikātus.
- Izņem 6 nepilnīgas rindas un izveido `tirs.csv` ar 297 ierakstiem.
- Apmāca **Random Forest** klasifikatoru, kas prognozē atzīmi par sirds slimības klātbūtni (`0` vai `1`).
- Salīdzina modeļa precizitāti ar bāzes līniju — vienmēr minēt biežāko apmācības klasi.
- Parāda divas svarīgākās kolonnas un konkrētu kļūdainu testa rindu.

**Tas ir mācību piemērs, nevis medicīnisks diagnostikas rīks.**

## Failu struktūra

```text
Pirmais_modelis_no_nulles/
├── dati/
│   ├── processed.cleveland.data   # Oriģināls, bez izmaiņām
│   └── AVOTS.txt                  # Avots, lejupielādes datums un licence
├── 01_tirisana.py                # Datu tīrīšana
├── 02_modelis.py                 # Modeļa apmācība un novērtēšana
├── tirs.csv                      # Iztīrītie dati
├── tirisanas_statistika.json     # Tīrīšanas rindu skaits
├── rezultati.md                  # Rezultātu interpretācija un pašvērtējums
├── requirements.txt             # Python bibliotēkas
├── .gitignore                    # Faili, kurus neiekļaut Git
└── README.md                     # Šī instrukcija
```

## Nepieciešamais

- Python **3.11–3.13**
- Bibliotēka **pandas** (CSV nolasīšanai un tīrīšanai)
- Bibliotēka **scikit-learn** (datu sadalīšanai, modelim un precizitātes mērīšanai)

### Kā palaist Windows datorā ar VS Code

Atver šo mapi VS Code, pēc tam atver termināli (`Terminal` → `New Terminal`).

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe 01_tirisana.py
.\.venv\Scripts\python.exe 02_modelis.py
```

Ja Python palaidējs `py` nav pieejams, pirmajā komandā izmanto `python -m venv .venv`.
Linux/macOS: izmanto `python3 -m venv .venv`, aktivizē vidi un izpildi skriptus ar
`.venv/bin/python`.

**Svarīgi:** vispirms palaid `01_tirisana.py`, pēc tam `02_modelis.py`.
Tīrīšanas skripts no jauna izveido `tirs.csv` un `tirisanas_statistika.json`.
Oriģinālais fails netiek pārrakstīts. Otrais skripts izdrukā rezultātus terminālī,
bet nepārraksta `rezultati.md`.

## Pārbaudīts rezultāts

Ar Python 3.13.5, pandas 2.2.3 un scikit-learn 1.8.0, izmantojot
`random_state=42`:

| Rādītājs | Rezultāts |
| --- | ---: |
| Rindas pirms / pēc tīrīšanas | 303 / 297 |
| Trūkstošu datu dēļ izmestās rindas | 6 |
| Apmācības / testa rindas | 222 / 75 |
| **Modeļa precizitāte** | **81,3 %** |
| **Bāzes līnija** | **53,3 %** |
| Divas svarīgākās kolonnas | `cp` un `thal` |

Citās saderīgu bibliotēku versijās rezultāts var nedaudz atšķirties.
Detalizēta analīze un viena nepareizi prognozētā rinda ir `rezultati.md`.

## Datu avots un izmantošana

Dati iegūti no UCI Machine Learning Repository:
https://archive.ics.uci.edu/dataset/45/heart-disease.
Licence: **CC BY 4.0**. Informācija un precīza oriģinālā faila saite ir
`dati/AVOTS.txt`. `.data` paplašinājums nemaina faktu, ka failā ir
ar komatiem atdalītas CSV vērtības bez galvenes.

Sākotnējās `num` vērtības ir no 0 līdz 4. Lai veiktu vienkāršu klasifikāciju,
tās pārveidotas par 0 (nav norādīta sirds slimība) un 1 (norādīta slimība).
`avota_rinda` un vecā `num` kolonna modelim netiek dotas, lai izvairītos
no atbildes noplūdes vai bezjēdzīga rindas numura izmantošanas.

## Ierobežojumi

- Datu ir maz; testa precizitāte ir novērtējums vienā konkrētā sadalījumā.
- Kategoriju kodi (`cp`, `thal` u. c.) modelī saglabāti kā skaitļi.
- Pazīmju svarīgums nenozīmē cēloņsakarību.
- Modeli **nedrīkst** izmantot pacientu diagnosticēšanai, ārstēšanas izvēlei vai šķirošanai.

## GitHub

Repozitorijā ir jāieliek **atsevišķi faili un mape `dati/`**, nevis ZIP arhīvs.
Darba izstrādes soļus var parādīt ar atsevišķiem Git kommitiem.
