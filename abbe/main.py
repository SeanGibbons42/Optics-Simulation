import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
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

        self.v.obj_plot.canvas.get_tk_widget().bind("<Button-1>", self.open_file)
        self.v.compute_button.config(command=self.compute_planes)

    def compute_planes(self):
        fcl = self.m.fft2(self.m.obj_pic)
        self.v.fcl_plot.ax0.imshow(fcl, cmap=plt.get_cmap("gray"), vmin=0, vmax=1)
        self.v.fcl_plot.canvas.draw()

    def open_file(self, event):
        path = filedialog.askopenfilename(filetypes=[('PNG','*.png')])
        img = self.m.load_img(path)
        self.v.obj_plot.ax0.imshow(img, cmap=plt.get_cmap("gray"), vmin=0, vmax=1)
        self.v.obj_plot.canvas.draw()

#This code runs when the program is run. It basically launches the app:
if __name__ == "__main__":
    app = tk.Tk()
    app.geometry("2000x1500")
    main = Controller(app)
    # frame.place(relx = 0, rely=0, relheight=1, relwidth=1)
    app.mainloop()
