#!/bin/bash/python3 python

import sqlite3

# trieda pre inicializaciu a pripojenie k databaze
class Databaza:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.otvor_spojenie()
        self.init_db()
            
    # inicializacia databazy - vytvorenie tabulky pre ukladanie nameranych oneskoreni
    # ak este neexistuje tabulka tak sa vytvori nova
    def init_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS oneskorenia (
                id INTEGER PRIMARY KEY,
                adresa_servera TEXT,
                oneskorenie_ms REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
        
    # funkcia na ulozenie udajov do databazy
    def uloz_do_db(self, adresa_servera, oneskorenie):
        if self.conn is None:
            self.otvor_spojenie()
        else:
            self.cursor.execute('INSERT INTO oneskorenia (adresa_servera, oneskorenie_ms) VALUES (?, ?)', (adresa_servera, oneskorenie))
            self.conn.commit()
        
    # funkcia na ziskanie vsetkych udajov z databazy
    def ziskaj_udaje_db(self):
        self.cursor.execute("SELECT * FROM oneskorenia")
        
    # pomocna funkcia na ziskanie udajov
    def fetchall_udaje_db(self):
        return self.cursor.fetchall()
    
    # funkcia na otvorenie spojenia s databazou
    def otvor_spojenie(self):
        if self.conn is None:
            self.conn = sqlite3.connect("db/udaje_oneskorenia.db", check_same_thread=False)
            self.cursor = self.conn.cursor()
    
    # funkcia na zatvorenie spojenia s databazou
    def zatvor_spojenie(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None