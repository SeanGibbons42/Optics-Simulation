import tkinter as tk
import views
import models

class Controller():
    def __init__(self, parent):
        self.v = views.View(parent)
        self.m = models.Model()



if __name__ == "__main__":
    app = tk.Tk()
    main = Controller(app)
    # frame.place(relx = 0, rely=0, relheight=1, relwidth=1)
    app.mainloop()
