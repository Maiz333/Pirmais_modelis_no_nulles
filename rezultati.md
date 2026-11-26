# Rezultātu interpretācija — Pirmais modelis no nulles

## 1. Kas ir šie dati un no kurienes tie nāk?

Izmantoju **Heart Disease (Cleveland)** datu kopu no **UCI Machine Learning Repository**.
Tajā ir 303 ieraksti un 14 sākotnējās kolonnas: 13 pacienta mērījumi vai
pazīmes un viena atbildes kolonna `num`. Tādas pazīmes kā `age`, `cp` un
`thalach` raksturo vecumu, sāpju veidu krūtīs un maksimālo sasniegto pulsu.

Avots: https://archive.ics.uci.edu/dataset/45/heart-disease.
Oriģinālais fails ir `dati/processed.cleveland.data`, un plašāka informācija par
avotu, lejupielādes datumu un licenci ir failā `dati/AVOTS.txt`.
Fails ir CSV formātā (komatu atdalītas vērtības), kaut gan tā paplašinājums ir `.data`.

## 2. Kas ar datiem bija nepareizi un ko es izdarīju?

Oriģinālajā datu kopā dažas vērtības ir aizstātas ar `?`. Tā ir reāla datu
kvalitātes problēma: **6 rindās trūkst viena mērījuma** — četras reizes kolonnā
`ca` un divas reizes kolonnā `thal`. Es pārvērtu `?` par trūkstošām vērtībām,
pārbaudīju, vai kolonnas var pārvērst skaitļos, un izņēmu nepilnās rindas.
Šajā vienkāršajā mācību darbā es necentos minēt nezināmus medicīniskos mērījumus.

| Tīrīšanas solis | Rindu skaits |
| --- | ---: |
| Sākotnējās rindas | 303 |
| Izmestas nekonvertējama teksta dēļ | 0 |
| Izmestas trūkstošu vērtību dēļ | 6 |
| Izmesti pilnīgi dublēti ieraksti | 0 |
| **Rindas pēc tīrīšanas** | **297** |

Izveidoju jaunu mērķa kolonnu `sirds_slimiba`: sākotnējo `num=0` pārvērtu
par **0**, bet `num=1`, `2`, `3` un `4` apvienoju kā **1**. Sākotnējo `num`
kolonnu izņēmu, jo citādi modelis jau redzētu pareizo atbildi. Kolonna
`avota_rinda` palīdz atrast ierakstu oriģinālajā failā, taču netiek izmantota
modeļa trenēšanai. Oriģinālais fails nav mainīts; rezultāts saglabāts `tirs.csv`.

## 3. Ko modelis prognozē un cik labi?

Modelis prognozē **sirds slimības klātbūtnes atzīmi datu kopā**: `0` — nav
norādīta, `1` — ir norādīta. Izmantoju vienu **RandomForestClassifier** modeli
no `scikit-learn` un 13 ievades pazīmes.

Datu sadalījums: **222 rindas apmācībai (75 %) un 75 rindas testam (25 %)**.
Sadalījums bija stratificēts, lai abu klašu proporcijas būtu līdzīgas.

| Rādītājs | Rezultāts |
| --- | ---: |
| Random Forest precizitāte uz testa datiem | **81,3 % (61/75)** |
| Bāzes līnija — vienmēr min biežāko apmācības klasi `0` | **53,3 % (40/75)** |
| Starpība | **+28,0 procentpunkti** |
| Nepareizas modeļa prognozes | **14 no 75** |

Bāzes līnijai nav vajadzīgs atsevišķs modelis: tā vienmēr min vienu un to
pašu biežāko klasi no apmācības datiem. **Modelis šo bāzes līniju pārsniedza**.
Starpība 28 procentpunkti ir pamanāma tieši šajā testa kopā, taču ar vienu
nelielu datu sadalījumu nevar garantēt tādu pašu precizitāti citos datos.

Jucekļa matrica (rindas — īstā klase 0/1, kolonnas — prognoze 0/1):

```text
[[35  5]
 [ 9 26]]
```

Tātad 35 un 26 prognozes ir pareizas, bet 5 un 9 — nepareizas.

## 4. Kuras divas kolonnas modelim bija svarīgākās?

1. **`cp` — 0,1630.** Sāpju veids krūtīs.
2. **`thal` — 0,1621.** Izmeklējuma rezultāta kategorija.

Tas šķiet loģiski, jo šie medicīniskie rādītāji var būt saistīti ar
atzīmi par sirds slimību. Tomēr šis ir **modeļa aprēķināts pazīmju svarīgums**,
nevis pierādījums par slimības cēloni. `cp` un `thal` satur skaitliskus
**kategoriju kodus**, nevis parastus nepārtrauktus skaitļus; šajā vienkāršajā
projektā tos atstāju skaitliskus. Tas ir viens no pieejas ierobežojumiem.

## 5. Konkrēta rinda, kurā modelis kļūdījās

**Oriģinālā faila 28. rinda**, kura pēc tīrīšanas palika testa kopā.
Tās vērtības:

| Kolonna | Vērtība | Kolonna | Vērtība |
| --- | ---: | --- | ---: |
| age | 66 | sex | 0 |
| cp | 1 | trestbps | 150 |
| chol | 226 | fbs | 0 |
| restecg | 0 | thalach | 114 |
| exang | 0 | oldpeak | 2,6 |
| slope | 3 | ca | 0 |
| thal | 3 | | |

- **Pareizā klase:** `0` (ierakstā nav norādīta slimības klātbūtne).
- **Modeļa prognoze:** `1` (ierakstā ir norādīta slimības klātbūtne).

**Iespējamais skaidrojums:** šīs rindas pazīmju kombinācija var līdzināties
citiem apmācības ierakstiem ar atzīmi `1`, piemēram, vecums ir 66 gadi un
maksimālais pulss ir 114. Vienlaikus citas pazīmes, piemēram, `ca=0` un
`thal=3`, var liecināt par citādu ainu. Modelis neprot pilnīgi droši atšķirt
šādus gadījumus. Tas ir iespējamais, nevis pierādīts konkrētās kļūdas cēlonis.

## 6. Ko ar šo modeli NEDRĪKST darīt?

**Šo modeli nedrīkst izmantot, lai īstam pacientam noteiktu diagnozi vai
pieņemtu lēmumu par ārstēšanu.** Tam izmantota neliela, vēsturiska datu kopa,
un nav pārbaudīts, vai modelis darbojas ar mūsdienu pacientiem dažādās
slimnīcās. Precizitāte vienā mācību testa kopā nav medicīniska drošuma
pierādījums.

## Pašvērtējums

Man izdevās saglabāt sākotnējos datus, iztīrīt sešas nepilnīgas rindas un apmācīt modeli, kas testā pārspēja bāzes līniju.
Sarežģītāk bija saprast, kā pareizi pārbaudīt datus un izskaidrot vienu kļūdainu prognozi.
Nākamreiz es pārbaudītu arī citus datu sadalījumus un atsevišķi apstrādātu kategoriskās pazīmes.
