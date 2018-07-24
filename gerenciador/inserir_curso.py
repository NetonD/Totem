from tkinter import *
from tkinter import messagebox
import sqlite3
import datetime
from auxiliares import tratarResultado


con = sqlite3.connect('../dados.db')

app = Tk()

Label(text='Area:',font = ('Arial',16)).pack(fill=X)
area = StringVar()
ent_area = Entry(app,textvariable=area,width=50,font = ('Arial',16)).pack(fill=X)

Label(text='Nome:',font = ('Arial',16)).pack(fill=X)
nome = StringVar()
ent_nome = Entry(app,textvariable=nome,width=50,font = ('Arial',16)).pack(fill=X)

Label(text='Faculdade:',font = ('Arial',16)).pack(fill=X)
cabeca = StringVar()
cabeca.set('Nenhum selecionado')

lista_faculdades = tratarResultado(con.execute('select nome_faculdade from instituicao').fetchall())

lista = OptionMenu(app,cabeca,*lista_faculdades)
lista.config(font="Arial, 16",width=37)
lista.pack(fill=X)

subitem = app.nametowidget(lista.menuname)
subitem.config(font="Arial, 15")

Button(text='Confirmar',font=('Arial',16),height=2,bg='blue',command=lambda:inserir()).pack(fill=X)

def inserir():
    try:
        id_facul = int(tratarResultado(con.execute('select id from instituicao where nome_faculdade = "%s";'%cabeca.get()))[0])

        con.execute('insert into cursos(nome,faculdade,area) values(?,?,?)',(nome.get(),id_facul,area.get()))
        con.commit()
        messagebox.showinfo('Sucesso','Cadastro feito coom sucesso')
        exit()
    except Exception as e:
        raise e
app.mainloop()
