import tkinter as tk

class View():
    def __init__(self, parent):
        self.mainframe = tk.Frame(parent)
        self.mainframe.place(relx = 0, rely = 0, relheight = 1, relwidth = 1)

        self.diagram = AbbeDiagram(self.mainframe)
        self.diagram.place(relx = 0, rely = 0, relheight = 0.4, relwidth = 1)


    def init_buttons(self):
        pass

    def init_labels(self):
        pass

    def init_fields(self):
        pass

class AbbeDiagram(tk.Canvas):
    def __init__(self, parent, width = 0, height = 0):
        tk.Canvas.__init__(self, parent, height = height, width = width)
        self.bind("<Configure>", self.on_resize)

    def draw_diagram(self):
        self.delete("all")

        #object, focal, and image plane locations
        obj_x = self.x_convert(0.1)
        fcl_x = self.x_convert(0.7)
        img_x = self.x_convert(0.9)

        #top and bottom bounds to the diagram
        top_y = self.y_convert(0.25)
        bottom_y = self.y_convert(0.75)

        self.create_line(obj_x, top_y, obj_x, bottom_y, width=10)

        lens_xstart = self.x_convert(0.50-0.025)
        lens_xend = self.x_convert(0.50+0.025)
        self.create_oval(lens_xstart, top_y, lens_xend, bottom_y, fill = "#0abee9")

        self.create_line(fcl_x, top_y, fcl_x, bottom_y, dash=20, width=5)
        self.create_line(img_x, top_y, img_x, bottom_y, width=10)

        offset = self.x_convert(0.01)
        y = self.y_convert(0.85)
        dim_height = self.y_convert(0.1)
        lens_x = (lens_xstart+lens_xend)//2
        self.draw_dimensionline(obj_x, lens_x, y, dim_height)
        self.draw_dimensionline(lens_x, fcl_x, y, dim_height)
        self.draw_dimensionline(fcl_x, img_x, y, dim_height)

    def draw_dimensionline(self, start, end, y, height):
        mid_y = self.y_convert(0.5)
        offset = self.x_convert(0.01)
        self.create_line(start, y, end, y, arrow="both", width=5)
        self.create_line(start, y-height//2, start, y+height//2, width=3)
        self.create_line(end, y-height//2, end, y+height//2, width=3)
        # self.create_line()

    def x_convert(self, relx):
        return relx*self.winfo_width()

    def y_convert(self, rely):
        return rely*self.winfo_height()

    def on_resize(self, event):
        self.draw_diagram()


class PlanePlot():
    pass
