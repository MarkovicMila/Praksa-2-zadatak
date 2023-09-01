from tkinter import *
from python import *
from functools import partial
from PIL import Image,ImageTk


root=Tk()
root.title("E-banking")

def quit(text):
    pyauto.alert(text)
    return root.quit()

def novi_prozor(ime_prezime,pin,broj_racuna,stanje_racuna):
	t=Toplevel(root)
	
	#Load an image in the script
	img= (Image.open("copy.png"))

	#Resize the Image using resize method
	resized_image= img.resize((50,50), Image.ANTIALIAS)
	new_image= ImageTk.PhotoImage(resized_image)

	Label(t,text='Broj racuna: ').grid(row=0,column=0)
	broj_racuna=Label(t,text=broj_racuna).grid(row=0,column=1)
	copy_button=Button(t,text='Copy',image=new_image,command=lambda:copy(broj_racuna))
	copy_button.grid(row=0,column=2)

	Label(t,text='Stanje racuna: ').grid(row=1,column=0)
	stanje_racuna_label=Label(t,text=str(stanje_racuna)+' dinara').grid(row=1,column=1)
	
	uplati_button=Button(t,text="Uplati na racun",command=lambda:uplati_na_racun(broj_racuna,stanje_racuna,ime_prezime))
	uplati_button.grid(row=2,column=2)
    
	export_izvod=Button(t,text="Izvesti izvod",command=lambda:[tr.export_transakcije(broj_racuna),quit('Formiran je excel file sa svim transakcijama! Ok za izlazak')])
	export_izvod.grid(row=3,column=2)

	logout_button=Button(t,text="Izlogujte se",command=t.destroy)
	logout_button.grid(row=4,column=2)

def copy(broj_racuna):
	broj_racuna=broj_racuna

def uplati_na_racun(broj_racuna,stanje_racuna,naziv_posiljaoca):
	t=Toplevel(root)

	broj_racuna_primaoca=Label(t, text="Broj racuna primaoca").grid(row=0, column=0)
	broj_racuna_primaoca=Entry(t)
	broj_racuna_primaoca.grid(row=0, column=1)

	iznos=Label(t, text="Iznos uplate").grid(row=1, column=0)
	iznos=Entry(t)
	iznos.grid(row=1, column=1)
	
	uplati=Button(t,text='Izvrsi uplatu',command=lambda:k.uplata(broj_racuna,float(stanje_racuna),str(broj_racuna_primaoca.get()),float(iznos.get()),naziv_posiljaoca))
	uplati.grid(row=2,column=1)										


username = Label(root, text="Ime i prezime").grid(row=0, column=0)
username = Entry(root)  
username.grid(row=0, column=1)

password = Label(root,text="Pin").grid(row=1, column=0)  
password = Entry(root, show='*')
password.grid(row=1, column=1)  
# validateLogin = partial(validateLogin, username, password)

loginButton = Button(root, text="Ulogujte se", command=lambda:novi_prozor(username.get(), password.get(), k.validate(username.get(),password.get())[0],k.validate(username.get(),password.get())[1]))
loginButton.grid(row=4, column=1)  

mainloop()