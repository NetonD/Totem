from tkinter import *
import sqlite3
from tkinter import messagebox
con = sqlite3.connect('../dados.db')
app = Tk()


Label(app,text='Nome:',font=('Arial',16)).pack(fill=X)
nome = StringVar()
Entry(app,textvariable=nome,width=25,font=('Arial',16)).pack(fill=X)

Label(app,text='Endereço:',font=('Arial',16)).pack(fill=X)
address = StringVar()
Entry(app,textvariable=address,width=25,font=('Arial',16)).pack(fill=X)

Button(text='Confirmar',font=('Arial',16),height=2,bg='blue',command=lambda:inserir()).pack(fill=X)

def inserir():
    try:
        con.execute('insert into instituicao(nome_faculdade,endereco) values(?,?)',(nome.get(),address.get()))
        con.commit()
        messagebox.showinfo('Sucesso','Cadastro feito coom sucesso')
        exit()
    except Exception as e:
        raise e
app.mainloop()
