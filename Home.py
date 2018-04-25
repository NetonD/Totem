from tkinter import  *
from PIL import Image,ImageTk
from Presenca import *
from Inscricao import *

class Home(object):
    
    def __init__(self,parent):
        self.root = parent
        self.root.title("Home")
        self.frame = Frame(parent)
        self.frame.grid()
        self.arq = None
        self.img = []
        btn_inscricao = self.make_button_img(self.frame,200,200,"imagens\\icon_inscricao.png",self.open_inscricao,0,0)
        btn_presenca = self.make_button_img(self.frame,200,200,"imagens\\icon_presenca.png",self.open_presenca,1,1) #N ESQUECER DE TROCAR
        lbl_inscricao = Label(self.frame,text="Inscrição",font="Arial, 23").grid(row=1,column=0)
        lbl_inscricao = Label(self.frame, text="Presença", font="Arial, 23").grid(row=1, column=1)

    def make_button_img(self,parent,w,h,url,func,pos,col):
         self.arq = Image.open(url).resize((w,h),Image.ANTIALIAS)
         self.img.append(ImageTk.PhotoImage(self.arq))
         return Button(parent,image = self.img[pos],height = h, width = w,command=func).grid(column=col,row=0,pady=(200),padx=130)

    def make_button(self,parent,w,h,texto,func):
         return Button(parent,width =w,height= h,text = texto,command=func).pack()

    def hiden(self):
        self.root.withdraw()

    def show(self):
        self.root.update()
        self.root.deiconify()

    def open_inscricao(self):
        self.hiden()
        subframe = Inscricao(self)
    def open_presenca(self):
        self.hiden()
        Presenca(self)


root= Tk()
root.geometry("940x780+30+30")
app = Home(root)
root.mainloop()