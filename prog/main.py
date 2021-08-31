#                         #
#    by AGOSSOU Hermann   #
#                         #

'''A simple template for an tkinter i/o program with tkinter'''
'''model with python class'''

# import the module and all specifications
# pip install tkinter
import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
from tkinter.filedialog import askopenfile


'''a clas to handle backend of the tk app''' 
class TkProg(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Adding a title to the window
        self.wm_title("Test Application")
        
        root=self
        root.geometry("500x500")
        root.title("Welcome !!!")

        # create a label
        label=Label(root,text="You can either add information or send an excel sheet")

        # placing the label at the right position
        label.place(x=100,y=80)

        # create a button
        button=Button(root,text="Add your info",bg="green",command=self.add_info)
        button.place(x=130,y=130)

        # create a button
        button2=Button(root,text="Download and analyse",bg="green",command = self.download_data)
        button2.place(x=250,y=130)

        # create a textarea 
            # geometry
        textarea=scrolledtext.ScrolledText(root,wrap = tk.WORD,width = 40,height = 15)
        textarea.grid(column = 0, pady = 10, padx = 10,)
        textarea.place(x=90,y=240)
        self.button  = button
        self.button2 = button2
        self.label = label
        self.textarea = textarea
    
    def set_text(self,str):
        # get value
        self.textarea.insert('1.0', str)
    def get_text(self):
        # add text
        return self.textarea.get('1.0', 'end')
        
    def add_info(self):
        '''fonction1: get then override texte value'''
        textcontent = self.get_text()
        newText = self.get_new_text(textcontent)
        self.set_text(newText)

    def download_data(self):
        '''fonction2: upload a file and override texte value'''
        #download file 
        filepath = self.open_file()
        self.set_text(filepath)

    def get_new_text(self,textcontent,**args):
        '''customisable method to handle content overriding'''
        return 'bof\nbof'

    def open_file(self):
        '''handle upload and get filepath '''
        filepath = askopenfile(mode='r', filetypes=[("All files", "*.*")])
        return filepath


if __name__ == '__main__':
    # app mainloop
    app = TkProg()
    app.mainloop()