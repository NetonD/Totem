from tkinter import *
import pyodbc
from auxiliares import tratarResultado, isNumber
from PIL import Image, ImageTk
from tkinter import messagebox
from datetime import datetime


class Presenca(Toplevel):
    def __init__(self, original):
        self.original_frame = original
        Toplevel.__init__(self)
        self.title("Inscricao")
        self.geometry("940x780+30+30")
        self.img = []
        self.arq = None
        self.cur = None
        self.config(padx=160, pady=200)
        self.conectarBanco()
        self.matricula = None
        ####### Label
        lbl_matricula = Label(self, text="Matrícula:", font="Arial, 23", pady=62).grid(column=0, row=0, sticky=W)
        lbl_nome = Label(self, text="Nome:", font="Arial, 23", pady=5).grid(column=0, row=3, columnspan=3, sticky=W)
        lbl_facul = Label(self, text="Instituição:", font="Arial, 23").grid(column=0, row=5, columnspan=1, sticky=W)
        lbl_curso = Label(self, text="Curso:", font="Arial, 23").grid(column=2, row=5, columnspan=2, sticky=W)
        lbl_evento = Label(self, text="Evento:", font="Arial, 23", pady=5).grid(column=0, row=7, columnspan=3, sticky=W)

        ####### Canvas
        self.canvas1 = Canvas(self, width=670, height=5, bg='dodgerblue')
        self.canvas1.grid(row=2, column=0, columnspan=3)

        ####### Entry
        self.varMatricula = StringVar()
        ent_matricula = Entry(self, width=16, textvariable=self.varMatricula, font="Arial, 16").grid(column=1, row=0,
                                                                                                     padx=20, sticky=W)
        self.varCurso = StringVar()
        ent_curso = Entry(self, state='disabled', textvariable=self.varCurso, width=23, font="Arial, 18").grid(column=2,
                                                                                                               row=6,
                                                                                                               columnspan=2,
                                                                                                               sticky=W)
        self.varFacul = StringVar()
        ent_facul = Entry(self, state='disabled', textvariable=self.varFacul, width=23, font="Arial, 18").grid(column=0,
                                                                                                               row=6,
                                                                                                               columnspan=2,
                                                                                                               sticky=W)
        self.varNome = StringVar()
        ent_nome = Entry(self, state='disabled', textvariable=self.varNome, width=23, font="Arial, 18").grid(column=0,
                                                                                                             row=4,
                                                                                                             columnspan=2,
                                                                                                             sticky=W)

        ####### Menu Option
        self.variavel = StringVar()
        self.variavel.set("Nenhum Selecionado")
        opcoes = {str(i) for i in tratarResultado(self.getEventos())}
        menuOption = OptionMenu(self, self.variavel, *opcoes)
        menuOption.config(width=59, font="Arial, 15")
        menuOption.grid(row=8, column=0, columnspan=3, sticky=W)
        menu = self.nametowidget(menuOption.menuname)
        menu.config(font="Arial, 15")

        ####### Button
        btn_checkin = self.make_button_img(180, 87, "imagens\\checkin_button.png", self.checkin, 0, 0, 9, W)
        btn_checkout = self.make_button_img(180, 87, "imagens\\checkout_button.png", self.checkout, 1, 2, 9, W)
        btn_cancel = self.make_button_img(180, 87, "imagens\\cancel_button.png", self.onClose, 2, 1, 9, W)
        btn_buscar = self.make_button_img(180, 87, "imagens\\search_button.png", self.completarCampos, 3, 2, 0, W)

    def buscar(self):
        aluno = self.cur.execute("select Alunos.nome,Instituição.nome,cursos.nome "
                                 "from Alunos, Instituição,cursos "
                                 "where Alunos.id_instituição = Instituição.id_faculdade "
                                 "and Alunos.id_cursos = cursos.id_curso "
                                 "and Alunos.matricula = %i" % int(self.varMatricula.get())).fetchall()
        self.matricula = int(self.varMatricula.get())
        return aluno[0]

    def completarCampos(self):
        try:
            if not self.varMatricula.get(): raise Exception
            isNumber(self.varMatricula.get())
            dados = self.buscar()
            self.varNome.set(dados[0])
            self.varFacul.set(dados[1])
            self.varCurso.set(dados[2])

        except ValueError:
            messagebox.showinfo("Alerta", "Insira somente numeros")
        except:
            messagebox.showinfo("Alerta", "Campo obrigatorio para busca")

    def conectarBanco(self):
        self.cur = pyodbc.connect(
            "Driver={ODBC Driver 13 for SQL Server};server=DESKTOP-CO1I2QA;database=teste;uid=sa;pwd=150971nt").cursor()

    def checkin(self):
        try:
            veri = self.cur.execute("select %s.id_aluno "
                                    "from alunos,%s "
                                    "where %s.id_aluno = %i" % (self.variavel.get(), self.variavel.get(), self.variavel.get(), self.matricula))
            dado = veri.fetchone()
            if not dado:
                messagebox.showinfo("Alerta", "Voce não está inscrito nesse evento")
            elif datetime.now().time() > self.getHora('inicio'):
                self.cur.execute("update %s set checkin=1 where %s.id_aluno = %i" % (
                    self.variavel.get(), self.variavel.get(), self.matricula))
                self.cur.execute("commit")
                messagebox.showinfo("Sucesso", "Checkin realizado com sucesso")
                self.onClose()
            else:
                messagebox.showinfo("Alerta", "Aguarde o horario correto")
        except pyodbc.ProgrammingError:
            messagebox.showinfo("Alerta","Selecione um evento")


    def checkout(self):
        try:
            veri = self.cur.execute("select %s.id_aluno "
                                    "from alunos,%s "
                                    "where %s.id_aluno = %i" % (self.variavel.get(), self.variavel.get(), self.variavel.get(), self.matricula))
            dado = veri.fetchone()
            if not dado:
                messagebox.showinfo("Alerta", "Voce não está inscrito nesse evento")
            elif datetime.now().time() < self.getHora('final'):
                self.cur.execute("update %s set checkout=1 where %s.id_aluno = %i" % (
                    self.variavel.get(), self.variavel.get(), self.matricula))
                self.cur.execute("commit")
                messagebox.showinfo("Sucesso","Checkout realizado com sucesso")
                self.onClose()
            else:
                messagebox.showinfo("Alerta", "Aguarde o horario correto")
        except pyodbc.ProgrammingError:
            messagebox.showinfo("Alerta","Selecione um evento")

    #################################### FAZER BUTTON CHECKOUT
    def getEventos(self):
        try:
            eventos = self.cur.execute("select nome from Eventos").fetchall()
            return eventos
        except:
            log = open("logerro.txt", 'w')
            log.write("Erro com conexao banco ao listar eventos")

    def getHora(self,ficio):
        hora = self.cur.execute("select hora_%s "
                                "from eventos "
                                "where nome = '%s'" % (ficio,self.variavel.get())).fetchone()
        return hora[0]
    def make_button_img(self, w, h, url, func, pos, col, row, alinhamento):
        self.arq = Image.open(url).resize((w, h), Image.ANTIALIAS)
        self.img.append(ImageTk.PhotoImage(self.arq))
        return Button(self, image=self.img[pos], height=h, width=w, command=func).grid(column=col, row=row, pady=5,
                                                                                       sticky=alinhamento)

    def onClose(self):
        self.destroy()
        self.original_frame.show()
