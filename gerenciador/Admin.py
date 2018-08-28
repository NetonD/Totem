#!/usr/bin/python
# -*- coding: utf-8  -*-
import os
from tkinter import *


app = Tk()


btn_curso = Button(app,text='Inserir Curso',command = lambda:executar(btn_curso['text']),font=('Arial',16),bg='red')
btn_faculdade = Button(app,text = 'Inserir Faculdade',command = lambda:executar(btn_faculdade['text']),font=('Arial',16),bg='yellow')
btn_evento = Button(app, text = 'Inserir Evento',command = lambda:executar(btn_evento['text']),font=('Arial',16),bg='green')

btn_curso.pack(fill=X)
btn_faculdade.pack(fill=X)
btn_evento.pack(fill=X)

def executar(nome):
    try:
        app.destroy()
        os.system('python %s.py' % nome.lower().replace(' ','_'))

    except Exception as e:
        os.system('python3 %s.py' % nome.lower().replace(' ','_'))
        app.destroy()
        
    finally:
    	print('Não esqueça de verificar o nome para executar python: 1)python ou 2) python3')


app.mainloop()
