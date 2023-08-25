import psycopg2 as pg
import openpyxl as op
import pandas as pd
import matplotlib.pyplot as plt
import pyautogui as pyauto

class Korisnici:
    def __init__(self):
        self.con=pg.connect(
            database='E-banking',
            password='itoip',
            user='postgres',
            host='localhost',
            port='5432'
        )
        self.korisnici_df=None

    def import_from_sql(self):
        self.korisnici_df=pd.read_sql('SELECT * FROM KORISNICI',con=self.con)
        return self.korisnici_df

    
    def validate(self,username,password):
        pom_ime_prezime=k.import_from_sql().iloc[:,1]
        pom_pin=k.import_from_sql().iloc[:,3]
        ime_prezime=[]     
        pin=[] 
        for i in pom_ime_prezime:
            ime_prezime.append(i)
        for i in pom_pin:
            pin.append(i)
        # print(ime_prezime)
        # print(pin)
        pom=0
        for i in range(len(ime_prezime)):
            if username==ime_prezime[i] and password==pin[i]:
                pom=1
                i_pom=i
        if pom==0:
            pyauto.alert('Lose uneti Ime i Prezime ili pin! Ok za exit')
            return exit()
        
        else:
            broj_racuna=k.import_from_sql().iloc[i_pom][0]
            # broj_racuna=broj_racuna.astype(str)
            stanje_racuna=k.import_from_sql().iloc[i_pom][2]
            # stanje_racuna=stanje_racuna.astype(float)
            return broj_racuna,stanje_racuna

    def uplata(self,broj_racuna,stanje_racuna,broj_racuna_primaoca,iznos):
        pass
    
    def close_connection(self):
        self.con.close()
    
class Transakcije:
    def __init__(self):
        self.con=pg.connect(
            database='E-banking',
            password='itoip',
            user='postgres',
            host='localhost',
            port='5432'
        )
        self.transakcije_df=None

    def import_from_sql(self):
        self.transakcije_df=pd.read_sql('SELECT * FROM TRANSAKCIJE',con=self.con)
        return self.transakcije_df
    
    def export_transakcije(self,broj_racuna):
        self.transakcije_df=pd.read_sql('''SELECT * FROM TRANSAKCIJE WHERE RACUN_POSILJAOC='{}' '''.format(broj_racuna),con=self.con)
        self.transakcije_df.to_excel('Transakcije.xlsx',index=False)
        return 'File succesfully exported'
    
    def dodaj_transakciju(self,broj_racuna,stanje_racuna,broj_racuna_primaoca,iznos):
        pass
    
    def close_connection(self):
        self.con.close()



k=Korisnici()
tr=Transakcije()

# print(k.validate('Mila Markovic','7777'))
# print(a.export_agencija('Rapsody Travel'))