# Opis Projekta

Projekt `pa1` je spletni pajek (crawler), ki se uporablja za obiskovanje in analizo spletnih strani. Namenjen je iskanju in shranjevanju informacij z različnih spletnih mest.

## Navodila za namestitev in zagon

### Predpogoji

Za zagon projekta `pa1` morate imeti nameščen Python in PostgreSQL. Poskrbite, da so na sistemu nameščene vse potrebne knjižnice.

### Namestitev

Namestite PostgreSQL na vaš sistem in ustvarite podatkovno bazo z naslednjimi parametri:

- Ime podatkovne baze: `postgres`
- Uporabniško ime: `postgres`
- Geslo: `12345`
- Gostitelj: `localhost`
- Vrata: `5432`

Bazo je potrebno tudi spremeniti z naslednjima dvema ukazoma:
- `ALTER TABLE crawldb.page ADD COLUMN content_hash VARCHAR(32);`
- `INSERT INTO crawldb.data_type (code) VALUES ('UNKNOWN');`

Odprite ukazno vrstico ali terminal in navigirajte do mape projekta.

Za namestitev potrebnih Python knjižnic izvedite naslednji ukaz:
`pip install psycopg2 requests bs4`

Ta ukaz bo namestil vse knjižnice, ki so potrebne za izvajanje pajka, vključno s podporo za delo z bazo podatkov, zahtevki HTTP in obdelavo HTML vsebine.

Za zagon pajka uporabite naslednji ukaz:
`python crawler.py`

