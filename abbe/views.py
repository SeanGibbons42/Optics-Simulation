import tkinter as tk

class View():
    def __init__(self, parent):
        self.mainframe = tk.Frame(parent)
        self.mainframe.place(relx = 0, rely = 0, relheight = 1, relheight = 1)

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
        #size widget
        self.bind("<Configure>", self.on_resize)

        tk.Canvas.__init__(self, parent, height = height, width = width)


    def draw_diagram(self, height, width):
        obj_x = self.x_convert(0.1)
        obj_start = self.y_convert(0.25)
        obj_end = self.y_convert(0.75)
        self.create_line(obj_x, obj_start, obj_x, obj_y)

        lens_xstart = self.x_convert(0.50-0.05)
        lens_xend = self.x_convert(0.50+0.05)
        lens_ystart = self.y_convert(0.25)
        lens_yend = self.y_convert(0.75)
        self.create_oval(lens_xstart, lens_ystart, lens_xend, lens_yend)

        fcl_x = self.x_convert(0.7)
        fcl_start = self.y_convert(0.25)
        fcl_end = self.y_convert(0.75)
        self.create_line(fcl_x, fcl_start, fcl_x, fcl_end, dash=20)

        img_x = self.x_convert(0.9)
        img_start =  self.y_convert(0.25)
        img_end = self.y_convert(0.75)
        self.create_line(img_x, img_start, img_x, img_end)


    def x_convert(self, relx):
        return relx*self.width

    def y_convert(self, rely):
        return rely*self.height

    def on_resize(self, event):
        print("resize")
        tk.update()
        if width == 0:
            width = self.winfo_width()
        if height == 0:
            height = self.winfo_height()
        self.draw_diagram(self.height, self.width)


class PlanePlot():
    pass
