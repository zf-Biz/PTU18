"""
Šiame GUI.py faile aprašytas grafinės sąsajos kodas.

This GUI.py file describes graphic user interface.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Base import engine, Vartotojai, Testai, Iteracijos, Klausimai, Atsakymai
from controller import (sesija, naujas_vartotojas, vartotoju_sarasas, testu_variantai, klausimai, atsakymai)

FONTS = ["Tenor Sans", "Consolas"]


def popup_vartotojas():
    """
    Funkcijos kodas, aprašantis naujo vartotojo sukūrimo langą.

    Function describes window that creates new user.
    """
    win2 = tk.Toplevel()
    win2.title("Naujas vartotojas")
    fr2_controls = tk.Frame(win2)
    l_naujas = tk.Label(fr2_controls, text="Naujas varotojo vardas: ")
    e_naujas = tk.Entry(fr2_controls)

    def vartotojo_issaugojimas():
        """
        Funkcija tikrina, ar vartotojo vardo langelis netuščias, jei ne - įrašo naują vartotoją į duomenų bazę.

        Function checks, if entry field is not empty, if not - writes new user into database.
        """
        if len(e_naujas.get()) == 0:
            messagebox.showinfo('Informacija', 'Tuščias langelis')
        else:
            vardas = e_naujas.get()
            naujas_vartotojas(sesija=sesija, vartotojo_vardas=vardas)
            combobox['values'] = vartotoju_sarasas(sesija=sesija)
            return combobox

    b_save = ttk.Button(fr2_controls, text="Išsaugoti", command=vartotojo_issaugojimas)
    b_iseiti = ttk.Button(fr2_controls, text='Išeiti', command=win2.destroy)
    l_naujas.grid(row=0, column=0)
    e_naujas.grid(row=0, column=1)
    b_save.grid(row=1, column=0)
    b_iseiti.grid(row=1, column=1)
    fr2_controls.pack()


def popup_testas_meniu():
    """
    Funkcija aprašo pagrindinį programos meniu langą.

    Function describes main menu window.
    """
    global pasirinkimas

    def toliau():
        if pasirinkimas.get() == 1:
            popup_testas1(vartotojas=vartotojas,
                          pasirinkimas=pasirinkimas.get())
        elif pasirinkimas.get() == 2:
            popup_testas2(vartotojas=vartotojas,
                          pasirinkimas=pasirinkimas.get())
        else:
            messagebox.showerror('Klaida', 'Nepasirinktas testas!')

    vartotojas = combobox.get()
    if vartotojas not in vartotoju_sarasas(sesija):
        print(vartotojas)
        messagebox.showerror('Klaida', 'Pasirinkite vartotojo vardą!')
    else:
        win_testas = tk.Tk()
        win_testas.title(f'Testas Meniu. Vartotojas: {vartotojas}')
        win_testas.geometry('350x200')
        win_testas.option_add("*Font", (FONTS[0], 11))
        fr_testas_controls = tk.Frame(win_testas)
        pasirinkimas = tk.IntVar(win_testas)
        label = ttk.Label(fr_testas_controls, text="Išsirinkite testą:")
        label.grid(row=0, column=0, sticky=tk.N)

        for d in testu_variantai(sesija):
            r = ttk.Radiobutton(
                fr_testas_controls,
                text=f'Testas {d}',
                value=d,
                variable=pasirinkimas
            )
            r.grid(row=d, column=0, sticky=tk.N)

        b_toliau = ttk.Button(fr_testas_controls, text="Toliau >", command=toliau)
        b_toliau.grid(row=len(testu_variantai(sesija)) + 1, column=0, sticky=tk.N)
        fr_testas_controls.pack()
        win_testas.eval("tk::PlaceWindow . center")
        win_testas.mainloop()


def popup_testas1(vartotojas, pasirinkimas):
    """
    Funkcija aprašo pirmo testo varianto langą

    Function describes window of first test variant.
    """
    win_testas_main = tk.Toplevel()
    fr_testas = tk.Frame(win_testas_main)
    sc_scrollas = tk.Scrollbar(win_testas_main)
    sc_scrollas.config(command=bx_boxas.yview)

    def tikrinimas():
        """
        Įvesties teisingumo tikrinimo funkcija.

        Input check function.
        """
        if var1.get() + var2.get() > 1:
            messagebox.showerror('Klaida', 'Pažymėta per daug atsakymo variantų')
        if var1.get() + var2.get() < 1:
            messagebox.showerror('Klaida', 'Neatsakyta į 1 klausimą')
        elif var3.get() + var4.get() > 1:
            messagebox.showerror('Klaida', 'Pažymėta per daug atsakymo variantų')
        elif var3.get() + var4.get() < 1:
            messagebox.showerror('Klaida', 'Neatsakyta į 2 klausimą')
        else:

            rezultatai()

    def rezultatai():
        """
        Ši funkcija palygina pateiktus vartotojo atsakymo variantus su teisingais ir parodo rezultatą naujame lange.

        This function compares users' answers with correct ones and shows the result in a new window.
        """
        t_atsakymai = []
        laikinas = [ats1, ats2]
        for q in laikinas:
            for t in q:
                if t[1] == 1:
                    t_atsakymai.append(t[0])

        tekstiniai = [ats1[0][0], ats1[1][0], ats2[0][0], ats2[1][0]]
        atsakymas = [var1.get(), var2.get(), var3.get(), var4.get()]
        taskai = []
        for i in range(len(atsakymas)):
            if len(tekstiniai[i] * atsakymas[i]) > 0:
                taskai.append(tekstiniai[i] * atsakymas[i])

        u = 0
        for p in range(len(taskai)):
            if t_atsakymai[p] == taskai[p]:
                u += 1
        messagebox.showinfo('Pabaiga', f'Jūs surinkote {u} iš {len(taskai)} taškų!')

        vartotojo_id = sesija.query(Vartotojai).filter_by(vardas=vartotojas).all()
        iteracija_plius = sesija.query(Iteracijos).filter_by(id=pasirinkimas).all()

        for t in range(len(taskai)):
            testo_rezultatas = Testai(vartotojai_id=vartotojo_id[0].id,
                                      klausimai_id=questions[t][1],
                                      taskas=taskai[t],
                                      iteracijos_iteracija=iteracija_plius[0].iteracija)
            sesija.add(testo_rezultatas)
            sesija.commit()

        iteracija_plius[0].iteracija += 1
        sesija.commit()
        win_testas_main.destroy()

    var1 = tk.IntVar()
    var2 = tk.IntVar()
    var3 = tk.IntVar()
    var4 = tk.IntVar()

    questions = klausimai(sesija, iteracijos_id=pasirinkimas)
    ats1 = atsakymai(sesija, klausimai_id=questions[0][0])
    ats2 = atsakymai(sesija, klausimai_id=questions[1][0])
    klausimas1_label = ttk.Label(fr_testas, text=questions[0][1], font=('Arial Black', 12))
    ats1_1 = tk.Checkbutton(fr_testas, text=ats1[0][0], onvalue=1, offvalue=0, variable=var1)
    ats1_2 = tk.Checkbutton(fr_testas, text=ats1[1][0], onvalue=1, offvalue=0, variable=var2)
    klausimas2_label = ttk.Label(fr_testas, text=questions[1][1], font=('Arial Black', 12))
    ats2_1 = tk.Checkbutton(fr_testas, text=ats2[0][0], onvalue=1, offvalue=0, variable=var3)
    ats2_2 = tk.Checkbutton(fr_testas, text=ats2[1][0], onvalue=1, offvalue=0, variable=var4)
    klausimas1_label.grid(row=0, column=0, sticky=tk.N)
    ats1_1.grid(row=1, column=0, sticky=tk.N)
    ats1_2.grid(row=2, column=0, sticky=tk.N)
    klausimas2_label.grid(row=3, column=0, sticky=tk.N)
    ats2_1.grid(row=4, column=0, sticky=tk.N)
    ats2_2.grid(row=5, column=0, sticky=tk.N)

    b_pateikti_atsakymus = ttk.Button(fr_testas, text='Pateikti atsakymus', command=tikrinimas)
    b_pateikti_atsakymus.grid(sticky=tk.S, padx=4, pady=4)
    fr_testas.pack(side=tk.LEFT)
    sc_scrollas.pack(side=tk.RIGHT, fill=tk.Y)
    win_testas_main.mainloop()


def popup_testas2(vartotojas, pasirinkimas):
    """
    Funkcija aprašo antro testo varianto langą

    Function describes window of second test variant.
    """
    win_testas_main = tk.Toplevel()
    fr_testas = tk.Frame(win_testas_main)
    sc_scrollas = tk.Scrollbar(win_testas_main)
    sc_scrollas.config(command=bx_boxas.yview)

    def tikrinimas():
        """
        Įvesties teisingumo tikrinimo funkcija.

        Input check function.
        """
        if var1.get() + var2.get() + var3.get() > 1:
            messagebox.showerror('Klaida', 'Pažymėta per daug atsakymo variantų')
        if var1.get() + var2.get() + var3.get() < 1:
            messagebox.showerror('Klaida', 'Nepažymėtas atsakymas į 1 klausimą')
        elif var4.get() + var5.get() + var6.get() > 1:
            messagebox.showerror('Klaida', 'Pažymėta per daug atsakymo variantų')
        elif var4.get() + var5.get() + var6.get() < 1:
            messagebox.showerror('Klaida', 'Nepažymėtas atsakymas į 2 klausimą')
        elif var7.get() + var8.get() + var9.get() > 1:
            messagebox.showerror('Klaida', 'Pažymėta per daug atsakymo variantų')
        elif var7.get() + var8.get() + var9.get() < 1:
            messagebox.showerror('Klaida', 'Nepažymėtas atsakymas į 3 klausimą')
        elif var10.get() + var11.get() + var12.get() > 1:
            messagebox.showerror('Klaida', 'Pažymėta per daug atsakymo variantų')
        elif var10.get() + var11.get() + var12.get() < 1:
            messagebox.showerror('Klaida', 'Nepažymėtas atsakymas į 4 klausimą')
        elif var13.get() + var14.get() + var15.get() > 1:
            messagebox.showerror('Klaida', 'Pažymėta per daug atsakymo variantų')
        elif var13.get() + var14.get() + var15.get() < 1:
            messagebox.showerror('Klaida', 'Nepažymėtas atsakymas į 5 klausimą')
        else:
            rezultatai()

    def rezultatai():
        """
        Ši funkcija palygina pateiktus vartotojo atsakymo variantus su teisingais ir parodo rezultatą naujame lange.

        This function compares users' answers with correct ones and shows the result in a new window.
        """
        t_atsakymai = []
        laikinas = [ats1, ats2, ats3, ats4, ats5]
        for q in laikinas:
            for t in q:
                if t[1] == 1:
                    t_atsakymai.append(t[0])

        tekstiniai = [ats1[0][0], ats1[1][0], ats1[2][0],
                      ats2[0][0], ats2[1][0], ats2[2][0],
                      ats3[0][0], ats3[1][0], ats3[2][0],
                      ats4[0][0], ats4[1][0], ats4[2][0],
                      ats5[0][0], ats5[1][0], ats5[2][0],
                      ]

        atsakymas = [var1.get(), var2.get(), var3.get(), var4.get(), var5.get(),
                     var6.get(), var7.get(), var8.get(), var9.get(), var10.get(),
                     var11.get(), var12.get(), var13.get(), var14.get(), var15.get()]
        taskai = []
        for i in range(len(atsakymas)):
            if len(tekstiniai[i] * atsakymas[i]) > 0:
                taskai.append(tekstiniai[i] * atsakymas[i])

        u = 0
        for p in range(len(taskai)):
            if t_atsakymai[p] == taskai[p]:
                u += 1
        messagebox.showinfo('Pabaiga', f'Jūs surinkote {u} iš {len(taskai)} taškų!')

        vartotojo_id = sesija.query(Vartotojai).filter_by(vardas=vartotojas).all()
        iteracija_plius = sesija.query(Iteracijos).filter_by(id=pasirinkimas).all()

        for t in range(len(taskai)):
            testo_rezultatas = Testai(vartotojai_id=vartotojo_id[0].id,
                                      klausimai_id=questions[t][1],
                                      taskas=taskai[t],
                                      iteracijos_iteracija=iteracija_plius[0].iteracija)
            sesija.add(testo_rezultatas)
            sesija.commit()

        iteracija_plius[0].iteracija += 1
        sesija.commit()
        win_testas_main.destroy()

    var1 = tk.IntVar()
    var2 = tk.IntVar()
    var3 = tk.IntVar()
    var4 = tk.IntVar()
    var5 = tk.IntVar()
    var6 = tk.IntVar()
    var7 = tk.IntVar()
    var8 = tk.IntVar()
    var9 = tk.IntVar()
    var10 = tk.IntVar()
    var11 = tk.IntVar()
    var12 = tk.IntVar()
    var13 = tk.IntVar()
    var14 = tk.IntVar()
    var15 = tk.IntVar()

    questions = klausimai(sesija, iteracijos_id=pasirinkimas)
    ats1 = atsakymai(sesija, klausimai_id=questions[0][0])
    ats2 = atsakymai(sesija, klausimai_id=questions[1][0])
    ats3 = atsakymai(sesija, klausimai_id=questions[2][0])
    ats4 = atsakymai(sesija, klausimai_id=questions[3][0])
    ats5 = atsakymai(sesija, klausimai_id=questions[4][0])

    tuscias_label1 = ttk.Label(fr_testas)
    tuscias_label2 = ttk.Label(fr_testas)
    tuscias_label3 = ttk.Label(fr_testas)
    tuscias_label4 = ttk.Label(fr_testas)
    klausimas1_label = ttk.Label(fr_testas, text=questions[0][1], font=('Arial Black', 12))
    ats1_1 = tk.Checkbutton(fr_testas, text=ats1[0][0], onvalue=1, offvalue=0, variable=var1)
    ats1_2 = tk.Checkbutton(fr_testas, text=ats1[1][0], onvalue=1, offvalue=0, variable=var2)
    ats1_3 = tk.Checkbutton(fr_testas, text=ats1[2][0], onvalue=1, offvalue=0, variable=var3)
    klausimas2_label = ttk.Label(fr_testas, text=questions[1][1], font=('Arial Black', 12))
    ats2_1 = tk.Checkbutton(fr_testas, text=ats2[0][0], onvalue=1, offvalue=0, variable=var4)
    ats2_2 = tk.Checkbutton(fr_testas, text=ats2[1][0], onvalue=1, offvalue=0, variable=var5)
    ats2_3 = tk.Checkbutton(fr_testas, text=ats2[2][0], onvalue=1, offvalue=0, variable=var6)
    klausimas3_label = ttk.Label(fr_testas, text=questions[2][1], font=('Arial Black', 12))
    ats3_1 = tk.Checkbutton(fr_testas, text=ats3[0][0], onvalue=1, offvalue=0, variable=var7)
    ats3_2 = tk.Checkbutton(fr_testas, text=ats3[1][0], onvalue=1, offvalue=0, variable=var8)
    ats3_3 = tk.Checkbutton(fr_testas, text=ats3[2][0], onvalue=1, offvalue=0, variable=var9)
    klausimas4_label = ttk.Label(fr_testas, text=questions[3][1], font=('Arial Black', 12))
    ats4_1 = tk.Checkbutton(fr_testas, text=ats4[0][0], onvalue=1, offvalue=0, variable=var10)
    ats4_2 = tk.Checkbutton(fr_testas, text=ats4[1][0], onvalue=1, offvalue=0, variable=var11)
    ats4_3 = tk.Checkbutton(fr_testas, text=ats4[2][0], onvalue=1, offvalue=0, variable=var12)
    klausimas5_label = ttk.Label(fr_testas, text=questions[4][1], font=('Arial Black', 12))
    ats5_1 = tk.Checkbutton(fr_testas, text=ats5[0][0], onvalue=1, offvalue=0, variable=var13)
    ats5_2 = tk.Checkbutton(fr_testas, text=ats5[1][0], onvalue=1, offvalue=0, variable=var14)
    ats5_3 = tk.Checkbutton(fr_testas, text=ats5[2][0], onvalue=1, offvalue=0, variable=var15)

    klausimas1_label.grid(row=0, column=0, sticky=tk.N, padx=4, pady=4)
    ats1_1.grid(row=1, column=0, sticky=tk.N)
    ats1_2.grid(row=2, column=0, sticky=tk.N)
    ats1_3.grid(row=3, column=0, sticky=tk.N)
    tuscias_label1.grid(row=4, column=0, sticky=tk.N)
    klausimas2_label.grid(row=5, column=0, sticky=tk.N, padx=4, pady=4)
    ats2_1.grid(row=6, column=0, sticky=tk.N)
    ats2_2.grid(row=7, column=0, sticky=tk.N)
    ats2_3.grid(row=8, column=0, sticky=tk.N)
    tuscias_label2.grid(row=9, column=0, sticky=tk.N)
    klausimas3_label.grid(row=10, column=0, sticky=tk.N, padx=4, pady=4)
    ats3_1.grid(row=11, column=0, sticky=tk.N)
    ats3_2.grid(row=12, column=0, sticky=tk.N)
    ats3_3.grid(row=13, column=0, sticky=tk.N)
    tuscias_label3.grid(row=14, column=0, sticky=tk.N)
    klausimas4_label.grid(row=15, column=0, sticky=tk.N, padx=4, pady=4)
    ats4_1.grid(row=16, column=0, sticky=tk.N)
    ats4_2.grid(row=17, column=0, sticky=tk.N)
    ats4_3.grid(row=18, column=0, sticky=tk.N)
    tuscias_label4.grid(row=19, column=0, sticky=tk.N)
    klausimas5_label.grid(row=20, column=0, sticky=tk.N, padx=4, pady=4)
    ats5_1.grid(row=21, column=0, sticky=tk.N)
    ats5_2.grid(row=22, column=0, sticky=tk.N)
    ats5_3.grid(row=23, column=0, sticky=tk.N)

    b_pateikti_atsakymus = ttk.Button(fr_testas, text='Pateikti atsakymus', command=tikrinimas)
    b_pateikti_atsakymus.grid(sticky=tk.S, padx=4, pady=4)
    fr_testas.pack(side=tk.LEFT)
    sc_scrollas.pack(side=tk.RIGHT, fill=tk.Y)
    win_testas_main.mainloop()


def hide_widgets(frame):
    """
    Ši funkcija panaikina lango elementus.

    This function erases window widgets.
    """
    frame.destroy()


class Rezultatai(tk.Tk):
    """
    Ši klasė iššaukiama paspaudus mygtuką 'Rezultatai'; vaizduojami vartotojų testų rezultatai naujame lange.

    Class is initiated when button 'Rezultatai' is pressed; shows all test results.
    """

    def __init__(self):
        super().__init__()
        self.title('Rezultatai')
        self.tree = self.create_tree_widget()

    def create_tree_widget(self):
        columns = ('1', '2', '3', '4', '5')
        tree = ttk.Treeview(self, columns=columns, show='headings')

        tree.heading('1', text='Id')
        tree.heading('2', text='Vartotojas')
        tree.heading('3', text='Klausimas')
        tree.heading('4', text='Atsakymas')
        tree.heading('5', text='Iteracijos numeris')

        tree.grid(row=0, column=0, sticky=tk.NSEW)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        info = sesija.query(Testai).all()
        irasas = []
        for i in info:
            irasas.append(
                [i.id, [i.vartotojai_id, i.vartotojai.vardas], i.klausimai_id, i.taskas, i.iteracijos_iteracija])
        for j in irasas:
            tree.insert('', tk.END, values=j)
        return tree


def rez_issaukimas():
    app = Rezultatai()
    app.mainloop()


class Teisingi_atsakymai(tk.Tk):
    """
    Klasė, sukurianti langą su testo klausimais ir teisingais atsakymais į juos.

    Class creates window with test questions and correct answers to them.
    """

    def __init__(self):
        super().__init__()
        self.title('Teisingi atsakymai')
        self.tree = self.create_tree_widget()
        self.geometry('800x250')
        self.grid_columnconfigure(0, weight=1)

    def create_tree_widget(self):
        columns = ('1', '2')
        tree = ttk.Treeview(self, columns=columns, show='headings')

        tree.heading('1', text='Klausimas')
        tree.heading('2', text='Atsakymas')

        tree.grid(row=0, column=0, sticky=tk.NSEW)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        info = sesija.query(Atsakymai).filter_by(tiesa_netiesa=1).all()
        irasas = []
        for i in info:
            irasas.append([i.klausimas.klausimas, i.atsakymas])
        for j in irasas:
            tree.insert('', tk.END, values=j)
        return tree


def rez_issaukimas_ats():
    app = Teisingi_atsakymai()
    app.mainloop()


win = tk.Tk()
win.title('ORM finalinė užduotis')
win.geometry('350x400')
win.option_add("*Font", (FONTS[0], 11))

fr_controls = tk.Frame(win)

sc_scrollas = tk.Scrollbar(win)
bx_boxas = tk.Listbox(win, yscrollcommand=sc_scrollas.set)
sc_scrollas.config(command=bx_boxas.yview)

b_naujas_vartotojas = ttk.Button(fr_controls, text='Įvesti naują vartotoją', command=popup_vartotojas)
l_vartotojas = ttk.Label(fr_controls, text='Pasirinkti vartotojo vardą: ')
vartotojai = tk.StringVar()
combobox = ttk.Combobox(fr_controls, textvariable=vartotojai)
combobox['values'] = vartotoju_sarasas(sesija=sesija)
combobox['state'] = 'readonly'
b_spresti_testa = ttk.Button(fr_controls, text='Spręsti testą', command=popup_testas_meniu)
b_rezultatai = ttk.Button(fr_controls, text='Rezultatai', command=rez_issaukimas)
b_teisingi_atsakymai = ttk.Button(fr_controls, text='Teisingi atsakymai', command=rez_issaukimas_ats)

l_vartotojas.grid(row=0, column=0)
combobox.grid(row=1, column=0)
b_naujas_vartotojas.grid(row=2, column=0, sticky=tk.W + tk.E)
b_spresti_testa.grid(row=3, column=0, sticky=tk.W + tk.E)
b_rezultatai.grid(row=4, column=0, sticky=tk.W + tk.E)
b_teisingi_atsakymai.grid(row=5, column=0, sticky=tk.W + tk.E)

fr_controls.pack()

win.eval("tk::PlaceWindow . center")
win.mainloop()
