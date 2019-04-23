import tkinter as tk
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np

class View():
    def __init__(self, parent):
        """ Class View: Top-level class for drawing UI elements """
        self.mainframe = tk.Frame(parent)
        self.mainframe.place(relx = 0, rely = 0, relheight = 1, relwidth = 1)

        self.diagram = AbbeDiagram(self.mainframe)
        self.diagram.place(relx = 0, rely = 0, relheight = 0.4, relwidth = 0.75)

        self.init_labels()
        self.init_fields()
        self.init_buttons()
        self.create_plots()

    def init_buttons(self):
        self.compute_button = tk.Button(self.mainframe, text = "Compute")
        self.compute_button.place(relx = 0.8, rely = 0.3, relwidth = 0.1, relheight = 0.1)

    def init_labels(self):
        #draw text labels
        self.fcl_lbl = tk.Label(self.mainframe, text="Focal Length")
        self.diam_lbl = tk.Label(self.mainframe, text="Lens Diameter")
        self.fcl_lbl.place(relx = 0.75, rely = 0.1, relheight=0.1, relwidth = 0.1)
        self.diam_lbl.place(relx = 0.75, rely = 0.2, relheight=0.1, relwidth = 0.1)

    def init_fields(self):
        #draw text input fields
        self.fcl_fld = tk.Entry(self.mainframe)
        self.diam_fld = tk.Entry(self.mainframe)
        self.fcl_fld.place(relx = 0.85, rely = 0.125, relheight=0.05, relwidth = 0.1)
        self.diam_fld.place(relx = 0.85, rely = 0.225, relheight=0.05, relwidth = 0.1)

    def create_plots(self):
        self.obj_plot = PlotButton(self.mainframe)
        self.fcl_plot = PlotLabel(self.mainframe)
        self.img_plot = PlotLabel(self.mainframe)
        self.obj_plot.place(relx = 0.05, rely=0.5, relheight=0.3, relwidth=0.3)
        self.fcl_plot.place(relx = 0.35, rely=0.5, relheight=0.3, relwidth=0.3)
        self.img_plot.place(relx = 0.65, rely=0.5, relheight=0.3, relwidth=0.3)



class AbbeDiagram(tk.Canvas):
    """Class AbbeDiagram: Draws a basic diagram explaining the lens setup"""

    def __init__(self, parent):
        #call to parent constructor
        tk.Canvas.__init__(self, parent, bd=3)
        #event binding: we want to re-draw the diagram when the
        self.bind("<Configure>", self.on_resize)

    def draw_diagram(self):
        """ Draws a representation of the lens/image/focal plane system """
        self.delete("all")

        #object, focal, and image plane locations
        obj_x = self.x_convert(0.1)
        fcl_x = self.x_convert(0.7)
        img_x = self.x_convert(0.9)

        #top and bottom bounds to the diagram
        top_y = self.y_convert(0.25)
        bottom_y = self.y_convert(0.75)

        #draw the image plane
        self.create_line(obj_x, top_y, obj_x, bottom_y, width=10)

        #draw the lens
        lens_xstart = self.x_convert(0.50-0.025)
        lens_xend = self.x_convert(0.50+0.025)
        self.create_oval(lens_xstart, top_y, lens_xend, bottom_y, fill = "#0abee9")

        #Draw focal plane
        self.create_line(fcl_x, top_y, fcl_x, bottom_y, dash=20, width=5)
        self.create_line(img_x, top_y, img_x, bottom_y, width=10)

        #Draw dimension markers
        offset = self.x_convert(0.01)
        y = self.y_convert(0.85)
        dim_height = self.y_convert(0.1)
        lens_x = (lens_xstart+lens_xend)//2
        self.draw_dimensionline(obj_x, lens_x, y, dim_height, text = "2f")
        self.draw_dimensionline(lens_x, fcl_x, y, dim_height, text = "f")
        self.draw_dimensionline(fcl_x, img_x, y, dim_height, text = "f")

    def draw_dimensionline(self, start, end, y, height, text = ""):
        """ Draws horizontal dimension arrows """
        mid_y = self.y_convert(0.5)
        offset = self.x_convert(0.01)
        self.create_line(start, y, end, y, arrow="both", width=5)
        self.create_line(start, y-height//2, start, y+height//2, width=3)
        self.create_line(end, y-height//2, end, y+height//2, width=3)
        self.create_text((start+end)//2, y+30, text=text, font="helvetica 30")

    def x_convert(self, relx):
        """
        x convert takes a relative coordinate (0-1) in the x axis and
        converts it to a distance in pixels.
        """
        return relx*self.winfo_width()

    def y_convert(self, rely):
        """ y-axis analog of x_convert """
        return rely*self.winfo_height()

    def on_resize(self, event):
        """ event handler for window resizing. """
        self.draw_diagram()

class PlotLabel(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.fig = Figure(figsize=(4,4), dpi=100)
        self.ax0 = self.fig.add_axes((0, 0, 1, 1))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(relx=0,rely=0, relheight=1, relwidth=1)

    def display(self, img):
        self.ax0.imshow(img, cmap=plt.get_cmap('gray'), vmin=0, vmax=1)
        self.canvas.draw()

    def clear(self):
        self.ax0.clear()

    def rgb2gray(self, rgb):
        return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

class PlotButton(PlotLabel):
    def __init__(self,master):
        PlotLabel.__init__(self, master)
        self.canvas.get_tk_widget().bind("<Button-1>", self.open_file)

    def open_file(self, event):
        path = filedialog.askopenfilename(filetypes=[('PNG','*.png')])
        img = mpimg.imread(path)
        img = self.rgb2gray(img)
        self.ax0.imshow(img, cmap=plt.get_cmap("gray"), vmin=0, vmax=1)
        self.canvas.draw()



    def display(self):
        pass

class PlanePlot():
    pass
