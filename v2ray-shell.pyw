#!/usr/bin/env python3

from tkinter import Tk, BOTH, Text, END
from tkinter.ttk import Frame, Button, Label
from pathlib import Path
import sys, subprocess

class runV2Rayshell(Frame):
    def __init__(self, root):
        super(runV2Rayshell, self).__init__()
        self.root = root
        self.pyqt5 = False
        self.check_PyQt5_installed()
        self.pip_source = u"""[global] 
index-url = https://pypi.douban.com/simple/
trusted-host = pypi.douban.com
"""
        if (self.pyqt5 == False):
            self.ui()
        else:
            self.ui()
            self.root.withdraw()
            self.run_current_v2rayshell()
    
    def run_current_v2rayshell(self):
        dir = "/src/bridgehouse/"
        path = Path().cwd()
        src_path ="{}{}".format(path, dir)
        if Path(src_path).is_dir():
            bridgehouse_path = src_path.split("/")
            sys.path.append("/".join(bridgehouse_path[:-2]))
            try:
                from bridgehouse import bridge
            except Exception as e:
                self.root.deiconify()
                self.text.delete(1.0, END)
                self.text.insert(2.0, e)
            else:
                #os.system('"{}{}"'.format(src_path, "bridge.py"))
                subprocess.call('"{}{}"'.format(src_path, "bridge.py"), shell = True)
                self.root.destroy()

    def check_PyQt5_installed(self):        
        try: import PyQt5
        except Exception: self.pyqt5 = False
        else: self.pyqt5 = True

    def set_pip_source(self):
        name = "pip.ini"
        home_path = "{}/pip".format(str(Path.home()))
        file_path = "{}/{}".format(home_path, name)
        if Path(home_path).is_dir() == False:
            Path(home_path).mkdir()

        if Path(home_path).is_dir():
            try:
                with open(file_path, "w", encoding="utf8") as f:
                    f.write(self.pip_source)
            except Exception:
                self.text.delete(1.0, END)
                self.text.insert(
                    2.0,"install {} failed. you can do by manual...\n{}".format(
                        filePath, self.pip_source)) 
            else:
                self.text.delete(1.0, END)
                self.text.insert(
                    2.0,"{} installed successfully...\n{}".format(
                        file_path, self.pip_source))
         
    def install_PyQt5(self):
        test = subprocess.Popen(
                ["pip","install","PyQt5"], 
                stdout=subprocess.PIPE)
        output = test.communicate()[0]
        self.text.delete(1.0, END)
        self.text.insert(END, output.decode("utf-8"))
        
    def ui(self):
        label_no_pyqt5 = Label(self, text = "There is no PyQt5 install.")
        label_pip_source = Label(
            self, 
            text = "You can click on the button below\nto speed up the installation of pypi source")
        label_install_pyqt5 = Label(
            self, text = "Then as a ROOT (OR ADMINISTRATOR) install PyQt5, \nlast restart this script.")
        butonn_install_source = Button(
            self, text = "install pypi source",
            command = self.set_pip_source)
        
        buton_install_PyQt5 = Button(
            self, 
            text = "install PyQt5",
            command = self.install_PyQt5)
        
        self.text = Text(self)
        
        label_empty  = Label(self)
        label_empty2 = Label(self)
        label_empty3 = Label(self)

        label_no_pyqt5.pack()
        label_pip_source.pack()
        label_install_pyqt5.pack()
        label_empty.pack()
        butonn_install_source.pack()
        label_empty2.pack()
        buton_install_PyQt5.pack()
        self.text.pack()
        label_empty3.pack()
        self.master.title("start run v2ray-shell")
        self.pack(fill = BOTH, expand = 1)
        self.center_window()
    
    def center_window(self):
        w = 620; h = 460
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        
        x = (sw -w)/2
        y = (sh -h)/2
        self.master.geometry("{}x{}+{}+{}".format(w, h, int(x), int(y)))
    
if __name__ == "__main__":
    root = Tk()
    runV2Rayshell(root)
    root.mainloop()