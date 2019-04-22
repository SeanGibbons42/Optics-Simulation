import tkinter as kk

class Controller():
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
    

if __name__ == "__main__":
    app = tk.Tk()
    frame = AbbeApp(app)
    frame.place(relx = 0, rely=0, relheight=1, relwidth=1)
    app.mainloop()
