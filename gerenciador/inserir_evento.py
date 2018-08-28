#!/usr/bin/python
# -*- coding: utf-8 -*-
from tkinter import *
import sqlite3
from auxiliares import tratarResultado
from tkinter import messagebox
con = sqlite3.connect('../dados.db')
app = Tk()


Label(app,text='Nome:',font=('Arial',16)).pack(fill=X)
nome = StringVar()
Entry(app,textvariable=nome,width=25,font=('Arial',16)).pack(fill=X)

Label(app,text='Data:',font=('Arial',16)).pack(fill=X)
data = StringVar()
Entry(app,textvariable=data,width=25,font=('Arial',16)).pack(fill=X)

Label(app,text='Formato: DD/MM/AAA',font=('Arial',8)).pack(fill=X)

Label(app,text='Faculdade',font=('Arial',16)).pack(fill=X)
selecionado = StringVar()
selecionado.set('Nenhuma selecionada')

faculdades= tratarResultado(con.execute('select nome_faculdade from instituicao').fetchall())
lista = OptionMenu(app,selecionado,*faculdades)
lista.config(font=('Arial',16),activebackground='green')
lista.pack(fill=X)

subitem = app.nametowidget(lista.menuname)
subitem.config(font=('Arial',16),activebackground='yellow')

Label(app,text='Inicio',font=('Arial',16)).pack(fill=X)
inicio = StringVar()
Entry(app,textvariable=inicio,width=25,font=('Arial',16)).pack(fill=X)
Label(app,text='Formato: HH:MM',font=('Arial',8)).pack(fill=X)

Label(app,text='Final',font=('Arial',16)).pack(fill=X)
final = StringVar()
Entry(app,textvariable=final,width=25,font=('Arial',16)).pack(fill=X)
Label(app,text='Formato: HH:MM',font=('Arial',8)).pack(fill=X)

Button(app,text='Confirmar',font=('Arial',16),height=2,bg='blue',command=lambda:criar()).pack(fill=X)

def criar():
    try:
        id_facul = int(tratarResultado(con.execute('select id from instituicao where nome_faculdade = "%s";'%selecionado.get()))[0])
        con.execute('insert into eventos(inicio,final,data,nome,faculdade) values (?,?,?,?,?)',(inicio.get(),final.get(),data.get(),nome.get(),id_facul))
        con.execute('''
        CREATE TABLE "%s" (
            aluno      INTEGER REFERENCES alunos (id)
                               NOT NULL ON CONFLICT FAIL
                               UNIQUE ON CONFLICT FAIL,
            nome_aluno VARCHAR NOT NULL ON CONFLICT FAIL,
            checkin    BOOLEAN NOT NULL
                               DEFAULT false,
            checkout   BOOLEAN NOT NULL
                               DEFAULT false
        );
        '''%nome.get())
        con.commit()
        messagebox.showinfo('Sucesso','Cadastro feito com sucesso!')
    except Exception as e:
        print('falha ao criar evento')
        raise e
app.mainloop()
