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

    def uplata(self,broj_racuna,stanje_racuna,broj_racuna_primaoca,iznos,naziv_posiljaoca):
        if stanje_racuna>=iznos:
            stanje_racuna-=iznos
            self.korisnici_df=pd.read_sql('SELECT * FROM KORISNICI',con=self.con)
            cursor=self.con.cursor()
            s="UPDATE KORISNICI SET STANJE = {} WHERE KORISNICI.BROJ_RACUNA = '{}';".format(stanje_racuna,broj_racuna)            
            cursor.execute(s)
            self.con.commit()
            cursor.close()


            tacno=broj_racuna_primaoca in set(self.korisnici_df['broj_racuna'])
            
            primalac = self.korisnici_df[self.korisnici_df['broj_racuna'] == broj_racuna_primaoca]
            primalac=pd.DataFrame(primalac)
            print(primalac)
            broj_racuna_primaoca=primalac.loc[0]['broj_racuna']
            stanje_racuna_primaoca=primalac.loc[2]['broj_racuna']
            naziv_primaoca=primalac.loc[1]['broj_racuna']

            
            # print(primalac[0])

            # stanje_racuna_primaoca = primalac[3]
            # print(tacno)
            # pom=0
            # for i in range(len(self.korisnici_df.index)):
            #     if broj_racuna== self.korisnici_df["broj_racuna"].values[i]:
            #         print(self.korisnici_df["broj_racuna"].values[i])
            #         print(broj_racuna)
            #         pom=1
            #         i_pom=i
            # if pom==0:
            #     pyauto.alert('Neispravan broj racuna za uplatu!')
            #     return exit()
        
            # else:
            #     broj_racuna_primaoca=k.import_from_sql().iloc[i_pom][0]
            #     print(broj_racuna_primaoca)
            #     stanje_racuna_primaoca=k.import_from_sql().iloc[i_pom][2]
            #     print(stanje_racuna_primaoca)
            #     naziv_primaoca=k.import_from_sql().iloc[i_pom][1]
            #     print(naziv_primaoca)

            
            if tacno:
                stanje_racuna_primaoca+=iznos
                self.korisnici_df=pd.read_sql('SELECT * FROM KORISNICI',con=self.con)
                cursor=self.con.cursor()
                s="UPDATE KORISNICI SET STANJE = {} WHERE KORISNICI.BROJ_RACUNA = '{}';".format(stanje_racuna_primaoca,broj_racuna_primaoca)            
                cursor.execute(s)
                self.con.commit()
                cursor.close()

                tr.dodaj_transakciju(naziv_posiljaoca,naziv_primaoca,broj_racuna,broj_racuna_primaoca,iznos)
                return 'Uspesno ste izvrsili uplatu!'
            else:
                return 'Nepostojeci broj racuna! OK za exit'
        else:
            return 'Nemate dovoljno sretstava na racunu!'
    
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
    
    def dodaj_transakciju(self,naziv_posiljaoca,naziv_primaoca,broj_racuna,broj_racuna_primaoca,iznos):
        self.transakcije_df=pd.read_sql('SELECT * FROM TRANSAKCIJE',con=self.con)
        cursor=self.con.cursor()
        s="INSERT INTO TRANSAKCIJE(naziv_posiljaoca,naziv_primaoca,broj_racuna,broj_racuna_primaoca,iznos) VALUES ('{}','{}','{}','{}',{});".format(naziv_posiljaoca,naziv_primaoca,broj_racuna,broj_racuna_primaoca,iznos)            
        cursor.execute(s)
        self.con.commit()
        cursor.close()

    
    def close_connection(self):
        self.con.close()



k=Korisnici()
tr=Transakcije()

# print(k.validate('Mila Markovic','7777'))
# print(a.export_agencija('Rapsody Travel'))