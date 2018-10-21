from tkinter import filedialog
from tkinter import *

class frame(Frame):

    def __init__(self, root, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.init_frame()
        self.folder_path1 = StringVar()
        self.folder_path2 = StringVar()
        root.configure(background='blue')
        root.geometry("300x150")

    def init_frame(self):
        self.master.title("SmartNotes")
        self.pack(fill=BOTH, expand=1)
        self.uploadvid_button = Button(self, text="Video",command=self.uploadvid)
        self.uploadvid_button.place(x=50, y=60)
        self.uploaddoc_button = Button(self, text="Document",command=self.uploaddoc)
        self.uploaddoc_button.place(x=162, y=60)

    def uploadvid(self):
        filenameVid = filedialog.askopenfilename()
        self.folder_path1.set(filenameVid)
        print(filenameVid)

    def uploaddoc(self):
        filenameDoc = filedialog.askopenfilename()
        self.folder_path2.set(filenameDoc)
        print(filenameDoc)

    def returnPath(self):
        return (self.folder_path1, self.folder_path2)

def getDocAndVidPath():
    root = Tk()
    app = frame(root,root)
    root.mainloop()
    return app.returnPath()

