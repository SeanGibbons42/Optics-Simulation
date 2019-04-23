import tkinter as tk
import views
import models

class Controller():
    """
    Class Controller integrates the UI (View) with the
    data/calculations (Model). 
    """
    def __init__(self, parent):
        self.v = views.View(parent)
        self.m = models.Model()


#This code runs when the program is run. It basically launches the app:
if __name__ == "__main__":
    app = tk.Tk()
    main = Controller(app)
    # frame.place(relx = 0, rely=0, relheight=1, relwidth=1)
    app.mainloop()
