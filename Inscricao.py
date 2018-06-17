from tkinter import *
import pyodbc
from PIL import Image,ImageTk
from tkinter import messagebox
from auxiliares import tratarResultado,string2int

#PRETENDO DEIXAR ISSO MAIS FACIL PARA INSTALAÇÃO
LOGIN = "Neto"
SENHA = "Almir@lves123"
SERVIDOR = "totem-bd.database.windows.net"
BANCO = "BD_TOTEM"

class Inscricao(Toplevel):
    def __init__(self,original,curs):
        self.original_frame = original
        Toplevel.__init__(self)
        self.title("Inscricao")
        self.geometry("940x780+30+30")
        self.img = []
        self.arq = None
        self.cur = curs

        bg = Image.open("imagens\\fundo_inscricao.png").resize((940,780),Image.ANTIALIAS)
        self.bgtk = ImageTk.PhotoImage(bg)
        Label(self,image=self.bgtk).place(x=0,y=0)

        self.overrideredirect(1)
        #self.wm_attributes("-topmost", True)
        #self.wm_attributes("-transparentcolor", "somecolor")

        

        ######## Label

        Label(self,text="Nome Completo:",font="Arial, 18").grid(column=1,row=0,sticky=SW,columnspan=2)
        Label(self,text="Email:",font="Arial, 18").grid(column=1,row=2,sticky=W,columnspan=2)
        Label(self,text="Matricula:",font="Arial, 18").grid(column=1,row=4,sticky=W)
        Label(self,text="Telefone:",font="Arial, 18").grid(column=2,row=4,sticky=W,padx=14)
        Label(self,text="Instituição:",font="Arial, 18").grid(column=1,row=6,sticky=W)
        Label(self,text="Curso:",font="Arial, 18").grid(column=1,row=8,sticky=W)
        Label(self,text="Eventos:",font="Arial, 18").grid(column=1,row=10,sticky=W)

        Label(self,bg='#F0EEDE',height=1).grid(column=0, row=0, columnspan=3, pady=125)
        Label(self,bg='#C4E2E3').grid(column=0,row=0,rowspan=13,padx=125)

        ######## Entry
        self.varNome = StringVar()
        ent_nome = Entry(self,width=30,font="Arial, 20",textvariable=self.varNome).grid(row=1,column=1,columnspan=2,sticky=W)
        self.varEmail = StringVar()
        ent_email = Entry(self, width=30, font="Arial, 20",textvariable=self.varEmail).grid(row=3, column=1,columnspan=2,sticky=W)
        self.varMatricula = StringVar()
        ent_matricula = Entry(self, width=12, font="Arial, 20",textvariable=self.varMatricula).grid(row=5, column=1,sticky=W)
        self.varCelular = StringVar()
        ent_celular = Entry(self,width=17, font="Arial, 20",textvariable=self.varCelular).grid(row=5,column=2,stick=W,padx=14)

        ######## Buttons
        btn_cancel = self.make_button_img(160,95,"imagens\\botao_cancelar.png",self.onClose,0,1,12,W)
        btn_concluir = self.make_button_img(160,96,"imagens\\botao_confirmar.png",self.cadastrar,1,2,12,E)

        ######## Lista insttituições

        self.variavel = StringVar(self)
        self.variavel.set("Ruy Barbosa")
        resposta = {str(i) for i in tratarResultado(self.getFaculdade())}
        menuOption = OptionMenu(self,self.variavel,*resposta)
        menuOption.config(font=("Arial",15),width=37) #LETRA DO MENU
        menuOption.grid(row=7,column=1,sticky=W,columnspan=2)
        menu = self.nametowidget(menuOption.menuname)
        menu.config(font=("Arial",15)) #LETRA DOS ITENS

        ######## Lista de cursos

        self.var = StringVar(self)
        self.var.set("Ciência da computação")
        resultado = {str(i) for i in tratarResultado(self.getCursos())}
        listaCurso = OptionMenu(self,self.var,*resultado)
        listaCurso.config(font="Arial, 15",width=37)
        listaCurso.grid(column=1,row=9,sticky=W,columnspan=2)
        subitem = self.nametowidget(listaCurso.menuname)
        subitem.config(font="Arial, 15")

        ######### Lista Eventos

        self.variable = StringVar(self)
        self.variable.set("Nenhum selecionado")
        consulta = {str(j) for j in tratarResultado(self.getEventos())}
        listaEvento = OptionMenu(self,self.variable,*consulta) #NÃO FUNCIONA SE TABELA TIVER VAZIA
        listaEvento.config(width=37,font="Arial, 15")
        item = self.nametowidget(listaEvento.menuname)
        item.config(font="Arial, 15")
        listaEvento.grid(column=1,row=11,columnspan=2,sticky=W)

    def onClose(self):
        self.destroy()
        self.original_frame.show()

    def make_button_img(self, w, h, url, func, pos, col,row,alinhamento):
        self.arq = Image.open(url).resize((w, h), Image.ANTIALIAS)
        self.img.append(ImageTk.PhotoImage(self.arq))
        btn = Button(self, image=self.img[pos],relief='flat',  height=h, width=w, command=func)


        btn.grid(column=col, row=row,pady=15,sticky=alinhamento)
        return btn

    def getCursos(self):
        try:
            cursos = self.cur.execute("select nome from Cursos").fetchall()
            return cursos
        except:
            log = open("logerro.txt",'rb')
            log.write("Erro com conexao banco ao listar cursos")


    def getEventos(self):
        try:
            eventos = self.cur.execute("select nome from Eventos").fetchall()
            return eventos
        except:
            log = open("logerro.txt",'rb')
            log.write("Erro com conexao banco ao listar eventos")



    def getFaculdade(self):
        try:
            fauldades = self.cur.execute("select nome from Instituição").fetchall()
            return fauldades
        except:
            log = open("logerro.txt",'rb')
            log.write("Erro com conexao banco ao listar eventos")


    def cadastrar(self):
        try:
            nome = str(self.varNome.get())
            email = self.varEmail.get()
            matricula = int(self.varMatricula.get())
            telefone = int(self.varCelular.get())
            facul = self.variavel.get()
            curso = self.var.get()
            evento = self.variable.get()

            if not nome or not email or evento == "Nenhum selecionado": raise Exception

            #con = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};server="+str(SERVIDOR)+";database="+str(BANCO)+";uid="+str(LOGIN)+";pwd="+str(SENHA))
            #cur = con.cursor()
            id_curso = tratarResultado(self.cur.execute("select id_curso from cursos where nome = (?)",curso).fetchone())
            id_facul = tratarResultado(self.cur.execute("select id_faculdade from instituição where nome = (?)",facul).fetchone())

            cadastro_aluno =  tratarResultado(self.cur.execute('select matricula from Alunos'))
            aluno_evento = tratarResultado(self.cur.execute('select id_aluno from "%s"'%evento))
            aluno_evento = string2int(aluno_evento)
            cadastro_aluno = string2int(cadastro_aluno)


            if not matricula in cadastro_aluno:
                self.cur.execute("insert into Alunos(nome,email,matricula,telefone,id_instituição,id_cursos) values (?, ?, ?, ?, ?, ?)",(nome,email,matricula,telefone,id_facul[0],id_curso[0]))

            if not matricula in aluno_evento:
                self.cur.execute('insert into "%s" values (?,?,0,0)'%evento,matricula,nome)
                self.cur.execute('commit')
                messagebox.showinfo("Sucesso","Cadastro efetuado com sucesso!")
                self.onClose()
            else: messagebox.showinfo("Alerta","Você já está cadastrado(a) no evento.")
        except pyodbc.IntegrityError:
            messagebox.showinfo("Alerta","Você já está cadastrado(a)")
        except UnboundLocalError:
            print("Linha 170")#####
        except pyodbc.ProgrammingError as e:
            print("Linha 170")######
        except ValueError as e:
            messagebox.showinfo("ERRO", "Verifique os campos: Matricula e Telefone")
        except Exception as e:
            messagebox.showinfo("ERRO","Não pode haver campos vazios")
            print(e)
