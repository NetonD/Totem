from tkinter import *
import pyodbc
from auxiliares import tratarResultado, isNumber
from PIL import Image, ImageTk
from tkinter import messagebox
from datetime import datetime

class Presenca(Toplevel):
    def __init__(self, original,curs):
        self.original_frame = original
        Toplevel.__init__(self)
        self.title("Inscricao")
        self.geometry("940x780+30+30")
        self.img = []
        self.arq = None
        self.cur = curs
        self.matricula = None

        bg = Image.open("imagens\\fundo_inscricao.png").resize((940, 780), Image.ANTIALIAS)
        self.bgtk = ImageTk.PhotoImage(bg)
        Label(self, image=self.bgtk).place(x=0, y=0)

        self.overrideredirect(1)


        ####### Label
        lbl_matricula = Label(self, text="Matrícula:", font="Arial, 18").grid(column=1, row=1, sticky=W)
        lbl_nome = Label(self, text="Nome:", font="Arial, 18", pady=5).grid(column=1, row=4, columnspan=3, sticky=W)
        lbl_facul = Label(self, text="instituicao:", font="Arial, 18").grid(column=1, row=6, columnspan=1, sticky=W)
        lbl_curso = Label(self, text="Curso:", font="Arial, 18").grid(column=2, row=6, columnspan=2, sticky=W,padx=85)
        lbl_evento = Label(self, text="Evento:", font="Arial, 18", pady=5).grid(column=1, row=8, columnspan=3, sticky=W)

        Label(self, bg='#F0EEDE', height=1).grid(column=0, row=0, columnspan=3, pady=125)
        Label(self, bg='#C4E2E3').grid(column=0, row=0, rowspan=13, padx=125)

        ####### Entry
        self.varMatricula = StringVar()
        ent_matricula = Entry(self, width=14, textvariable=self.varMatricula, font="Arial, 20").grid(column=2, row=1,
                                                                                                      sticky=W)

        self.varNome = StringVar()
        ent_nome = Entry(self, state='disabled', textvariable=self.varNome, width=31, font="Arial, 20").grid(column=1,
                                                                                                             row=5,
                                                                                                             columnspan=3,
                                                                                                             sticky=W)

        self.varCurso = StringVar()
        ent_curso = Entry(self, state='disabled', textvariable=self.varCurso, width=17, font="Arial, 20").grid(column=2,
                                                                                                               row=7,
                                                                                                               columnspan=3,
                                                                                                               padx=85,
                                                                                                               sticky=W)
        self.varFacul = StringVar()
        ent_facul = Entry(self, state='disabled', textvariable=self.varFacul, width=12, font="Arial, 20").grid(column=1,
                                                                                                               row=7,
                                                                                                               columnspan=2,
                                                                                                               sticky=W)


        ####### Menu Option
        self.variavel = StringVar()
        self.variavel.set("Nenhum Selecionado")
        opcoes = {str(i) for i in tratarResultado(self.getEventos())}
        menuOption = OptionMenu(self, self.variavel, *opcoes)
        menuOption.config(width=39, font="Arial, 15")
        menuOption.grid(row=9, column=1, columnspan=3, sticky=W)
        menu = self.nametowidget(menuOption.menuname)
        menu.config(font="Arial, 15")

        ####### Button
        btn_checkin = self.make_button_img(120, 40, "imagens\\botao_checkin.png", self.checkin, 0, 1, 10, W)
        btn_checkout = self.make_button_img(120, 40, "imagens\\checkout_button.png", self.checkout, 1, 3, 10, W)
        btn_cancel = self.make_button_img(120, 40, "imagens\\botao_cancelar.png", self.onClose, 2, 2, 10, W)
        btn_buscar = self.make_button_img(120, 40, "imagens\\botao_buscar.png", self.completarCampos, 3, 3, 1, W)

    def buscar(self):
        aluno = self.cur.execute("select Alunos.nome,instituicao.nome_faculdade,cursos.nome "
                                 "from Alunos, instituicao,cursos "
                                 "where Alunos.faculdade = instituicao.id "
                                 "and Alunos.curso = cursos.id "
                                 "and Alunos.matricula = %s; "% self.varMatricula.get()).fetchall()
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
        except Exception as e:
            messagebox.showinfo("Alerta", "Campo obrigatorio para busca.\nVerifique e tente novamente!")
            raise e
    def checkin(self):
        try:
            if self.variavel.get() == "Nenhum Selecionado": raise Exception
            veri = self.cur.execute('select "%s".aluno '
                                    'from alunos,"%s" '
                                    'where "%s".aluno = %i' % (self.variavel.get(), self.variavel.get(), self.variavel.get(), self.matricula))
            dado = veri.fetchone()
            if not dado:
                messagebox.showinfo("Alerta", "Voce não está inscrito nesse evento")
            elif (datetime.now().time() >= self.getHora('inicio')) and (self.getHora('final') <= datetime.now().time()):
                self.cur.execute('update %s set checkin=1 where "%s".id_aluno = %i' % (
                    self.variavel.get(), self.variavel.get(), self.matricula))
                self.cur.execute("commit")
                messagebox.showinfo("Sucesso", "Checkin realizado com sucesso")
                self.onClose()
            else:
                messagebox.showinfo("Alerta", "Aguarde o horario correto")
        except pyodbc.ProgrammingError:
            messagebox.showinfo("Alerta","Contate suporte")
        except Exception as e:
            messagebox.showinfo("Alerta","Selecione um evento")
            raise e

    def checkout(self):
        try:
            if self.variavel.get() == 'Nenhum Selecionado': raise Exception
            veri = self.cur.execute('select "%s".aluno '
                                    'from alunos,"%s" '
                                    'where "%s".aluno = %i' % (self.variavel.get(), self.variavel.get(), self.variavel.get(), self.matricula))
            dado = veri.fetchone()
            checkin = self.cur.execute('select checkin from "%s"'%self.variavel.get()).fetchone()
            if not dado:
                messagebox.showinfo("Alerta", "Voce não está inscrito nesse evento")
            elif datetime.now().time() < self.getHora('final') and checkin[0]:
                self.cur.execute('update "%s" set checkout=1 where "%s".aluno = %i' % (
                    self.variavel.get(), self.variavel.get(), self.matricula))
                self.cur.execute("commit")
                messagebox.showinfo("Sucesso","Checkout realizado com sucesso")
                self.onClose()
            else:
                messagebox.showinfo("Alerta", "Aguarde o horario correto")
        except pyodbc.ProgrammingError as e:
            messagebox.showinfo("Erro","Contate suporte")
            print(e)
        except Exception as e:
            messagebox.showinfo("Alerta","Selecione um evento")
            raise e

    
    def getEventos(self):
        try:
            eventos = self.cur.execute("select nome from Eventos").fetchall()
            return eventos
        except:
            log = open("logerro.txt", 'w')
            log.write("Erro com conexao banco ao listar eventos")

    def getHora(self,fim_or_inicio):
        resultado = self.cur.execute("select %s "
                                "from eventos "
                                "where nome = '%s'" % (fim_or_inicio,self.variavel.get())).fetchone()

        return datetime.strptime(resultado[0],'%H:%M').time()

    def make_button_img(self, w, h, url, func, pos, col, row, alinhamento):
        self.arq = Image.open(url).resize((w, h), Image.ANTIALIAS)
        self.img.append(ImageTk.PhotoImage(self.arq))
        return Button(self, image=self.img[pos], height=h, width=w, command=func,borderwidth=0).grid(column=col, row=row, pady=15,
                                                                                       sticky=alinhamento)

    def onClose(self):
        self.destroy()
        self.original_frame.show()
