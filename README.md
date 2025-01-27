# Sieťový Asistent

## O aplikácii
Sieťový Asistent je aplikácia vyvinutá v Pythone, ktorá slúži na správu a analýzu sieťových informácií.

Cieľom tejto aplikácie je poskytnúť užívateľom - najmä sieťarom, jednoduché ale praktické nástroje v oblasti sietí, ktoré sú schopné aj graficky vykresliť namerané údaje a spravovať tieto údaje, tiež aj ukladanie a exportovanie týchto údajov.

Aplikácia je navrhnutá tak, aby bola hlavne užívateľsky prívetivá a nenáročná na ovládanie, a to najmä vďaka využitiu grafického rozhrania knižnice `Tkinter`.

### Funkcie aplikácie
- **IPv4 kalkulačka**: Aplikácia pomocou jednoduchej kalkulačky IPv4 adries vie vypočítať na základe vstupu užívateľa adresu siete, prvú a poslednú použiteľnú IP adresu, broadcastovú adresu a počet hostov v podsieti

- **Validácia IP adresy**: Aplikácia vie na základe vstupu užívateľa overiť, či užívateľ zadal platnú IPv4 adresu alebo nie a informovať ho o výsledku overenia

- **Vizualizácia údajov**: Pomocou knižnice `Matplotlib` aplikácia vie vykresliť vo forme grafu získané sieťové údaje

- **Ukladanie údajov**: Namerané údaje oneskorení serverov sa ukladajú do lokálnej `SQLite3` databázy, vďaka čomu je ich jednoduché spravovať a pristupovať k ním

- **Exportovanie údajov**: Výsledky výpočtov z IPv4 kalkulačky je možné exportovať do `.txt` súboru

- **Multithreading**: Aplikácia využíva multithreading na spracovanie sieťových operácií, čím zabezpečuje plynulý chod aplikácie a vykreslenie užívateľského rozhrania bez zadržiavania

- **Práca so sieťovými protokolmi**: Pomocou knižnice `Socket` aplikácia umožňuje interakciu so sieťovými protokolmi a analýzu sieťovej komunikácie

- **Zobrazenie aktuálneho času a dátumu**: Aplikácia využíva knižnicu `datetime` na zobrazenie aktuálneho času a dátumu v úvodnom okne

### Použité knižnice a technológie
- **Python**: Programovací jazyk pre vývoj aplikácie

- **Tkinter**: Knižnica na vytvorenie grafického užívateľského rozhrania (GUI)

- **SQLite3**: Databázový systém na ukladanie a správu údajov

- **ipaddress**: Knižnica na manipuláciu s IP adresami a podsieťami

- **Pandas**: Knižnica na analýzu a manipuláciu s dátami

- **Matplotlib**: Knižnica na vizualizáciu a vykresľovanie údajov vo forme grafu

- **Socket**: Knižnica na prácu so sieťovými protokolmi

- **Threading**: Knižnica na implementáciu multithreadingu

- **Time**: Knižnica na prácu s časom

- **datetime**: Knižnica na prácu s dátumom a časom

- **re**: Knižnica na prácu s regulárnymi výrazmi

### Inštalácia a spustenie aplikácie
1. Klonujte repozitár:
```bash
git clone https://github.com/xpal1/SietovyAsistent.git
```

2. Prejdite do adresára projektu:
```bash
cd SietovyAsistent/python
```

3. Spustite aplikáciu pomocou nasledujúceho príkazu (za predpokladu, že máte nainštalované potrebné knižnice pre spustenie aplikácie):
```bash
python main.py
```