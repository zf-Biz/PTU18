"""
Šiame controller.py faile aprašytos funkcijos, kurios įrašo duomenis į duomenu bazę arba juos nuskaito.

This controller.py file describes the functions that write data to database or read data from it.
"""
from sqlalchemy.orm import sessionmaker
from Base import engine, Vartotojai, Testai, Iteracijos, Klausimai, Atsakymai
from tkinter.messagebox import showinfo
import tkinter as tk

Session = sessionmaker(bind=engine)
sesija = Session()


def naujas_vartotojas(sesija, vartotojo_vardas):
    """
    Funkcija sukuria naują vartotojo slapyvardį ir jį įrašo į duomenu bazę.

    Function creates new user and writes it into database.
    """
    irasas = Vartotojai(vardas=vartotojo_vardas)
    sesija.add(irasas)
    sesija.commit()


def vartotoju_sarasas(sesija):
    """
    Funkcija nuskaito duomenų bazės Vartotojai lentelę ir gražino jus duomenis sąraše.


    Function read data from Vartotojai (User) table and return a list with data.
    """
    sarasas = []
    vartotojai = sesija.query(Vartotojai).all()
    for v in vartotojai:
        sarasas.append(v.vardas)
    return sarasas


def testu_variantai(sesija):
    """
    Funkcija nuskaito lentelę Iteracijos ir gražina jos duomenis sąraše.

    Function reads data from Iteracijos (Iterations) table and return a list with data.
    """
    variantai = []
    variantas = sesija.query(Iteracijos).all()
    for i in variantas:
        variantai.append(i.id)
    return variantai


def klausimai(sesija, iteracijos_id):
    """
    Funkcija nuskaito lentelę Klausimai ir grąžina duomenis sąraše pagal testo varianto numerį.

    Function reads data from Klausimai (Questions) table and return list with data filtered by test variant.
    """
    kl = []
    klausimai_rinkinys = sesija.query(Klausimai).filter_by(iteracijos_id=iteracijos_id).all()
    for k in klausimai_rinkinys:
        kl.append([k.id, k.klausimas])
    return kl


def atsakymai(sesija, klausimai_id):
    """
    Funkcija nuskaito lentelę Atsakymai ir grąžina duomenis su atsakymo variantais pagal klausimo numerį bei
    teisingo/neteisingo atsakymo varte sąraše.

    Function reads data from Atsakymai (Questions) table and return a list with answer options filtered by question id
    and with true/false value.
    """
    ats = []
    atsakymai_rinkinys = sesija.query(Atsakymai).filter_by(klausimai_id=klausimai_id).all()
    for a in atsakymai_rinkinys:
        ats.append((a.atsakymas, a.tiesa_netiesa))
    return ats

# for i in questions:
#     klausimas_label = ttk.Label(fr_testas, text=i[1])
#     klausimas_label.grid(row=x, column=0, sticky=tk.N)
#     answers = atsakymai(sesija, klausimai_id=i[0])
#     for n in answers:
#         ats = tk.IntVar()
#         b_check = (tk.Checkbutton(fr_testas,
#                                   text=n[0],
#                                   variable=ats,
#                                   onvalue=1,
#                                   offvalue=0,
#                                   command=lambda: print(ats.get())
#                                   ))
#         b_check.grid(row=x + 1, column=0, sticky=tk.N)
#         x += 1
#     x += 1
