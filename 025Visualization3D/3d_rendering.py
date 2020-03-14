# coding:utf-8
"""
create on Mar 14, 2020 By Wenyan YU
Email: ieeflsyu@outlook.com
Function:

用Python+tkinter探索三维可视化

"""

import tkinter as tk
import math as m
import time as t
from tkinter import colorchooser as c_chooser


class ThreeD():

    def __init__(self, canvas, coords, alpha = 0, beeta = 0, gaama = 0, frame_rate = 30, unit_pixels = 200):
        self.canvas = canvas
        self.coords = self.set_coords(coords)
        self.alpha = alpha
        self.beeta = beeta
        self.gaama = gaama
        self.frame_rate = frame_rate
        self.unit_pixels = unit_pixels
        self.printed_polygons = []
        self.set_view_dist()
        self.set_canvas_size()
        self.set_colour()
        self.set_view_point()
        self.set_virtual_axis()
        not_error = not(self.set_surface_equations())

        if not_error:
            raise Exception("Points that are supposed to be coplanar are non coplanar")

    @staticmethod
    def dist(point1, point2):
        x1,y1,z1 = point1
        x2,y2,z2 = point2

        return m.sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)

    @staticmethod
    def set_coords(coords):
        #[(points),[(orientation),(orientation),(colour)]]
        points = coords[0]
        final_coords = []
        for surface in coords[1:]:
            s = []
            for polygon in surface:
                p = []

                for point in polygon[:-1]:
                    p.append(points[point])

                p.append(polygon[-1])
                s.append(p)

            final_coords.append(s)

        return final_coords


    def set_view_dist(self):
        self.d = 0
        points = self.distinct_points()
        for point in points:
            distance = self.dist(point,(0,0,0))
            if distance>self.d:
                self.d = distance
        self.d*=50

    def set_view_point(self, view_point = None, reference_point = None):
        if view_point == None and reference_point == None:
            self.a = m.cos(self.beeta) * m.sin(self.alpha)
            self.b = m.sin(self.beeta)
            self.c = m.cos(self.beeta) * m.cos(self.alpha)

            reference_point = self.rotate_zaxis((0,1,0), theeta = self.gaama)
            self.set_virtual_axis(reference_point)
        else:
            self.a, self.b, self.c = view_point
            self.set_virtual_axis(reference_point)

    def distinct_points(self):
        points = []
        for surface in self.coords:
            for polygon in surface:
                for point in polygon[:-1]:
                    if point not in points:
                        points.append(point)
        return points

    def set_canvas_size(self):
        self.csize = 0
        points = self.distinct_points()
        for point in points:
            distance = self.dist(point,(0,0,0))
            if distance>self.csize:
                self.csize = distance
        self.csize = int(self.csize*2*self.unit_pixels)+50
        self.canvas.config(width = self.csize, height = self.csize)

    @staticmethod
    def plane_equation(point1, point2, point3):
        x1,y1,z1 = point1
        x2,y2,z2 = point2
        x3,y3,z3 = point3

        a = (y2-y1)*(z3-z1)-(y3-y1)*(z2-z1)
        b = (x3-x1)*(z2-z1)-(x2-x1)*(z3-z1)
        c = (x2-x1)*(y3-y1)-(x3-x1)*(y2-y1)
        d = a*x1 + b*y1 + c*z1

        return [a,b,c,d]

    def set_surface_equations(self):
        self.s_equations = []
        for surface in self.coords:
            point1 = surface[0][0]
            point2 = surface[0][1]
            point3 = surface[0][2]

            self.s_equations.append(self.plane_equation(point1,point2,point3))

            for polygon in surface:
                for point in polygon[:-1]:
                    x,y,z = point
                    a,b,c,d = self.s_equations[-1]
                    if a*x + b*y + c*z != d:
                        return 0

        return 1

    def display_list(self):
        l = []

        for equation in self.s_equations:
            A,B,C,D = equation
            x,y,z = self.d*self.a,self.d*self.b,self.d*self.c
            l.append(A*x + B*y + C*z >= D)

        # print(l)
        return l



    def display_surfaces(self,coords):
        d_list = self.display_list()
        d_surface = []

        for i in range(len(d_list)):
            if d_list[i]:
                d_surface.append(coords[i])

        return d_surface

    def threeD_to_twoD(self):
        return_coords = []
        for surface in self.coords:
            return_surface = []
            for polygon in surface:
                return_polygon = []
                for point in polygon[:-1]:
                    x,y,z = point
                    a,b,c = self.a, self.b, self.c
                    # X_temp = x*m.cos(self.alpha)-z*m.sin(self.alpha)
                    # Y_temp = y*m.cos(self.beeta)-z*m.sin(self.beeta)*m.cos(self.alpha)-x*m.sin(self.beeta)*m.sin(self.alpha)
                    #
                    # X = (X_temp*m.cos(self.gaama) + Y_temp*m.sin(self.gaama))*self.unit_pixels + self.csize/2
                    # Y = self.csize/2 - (-X_temp*m.sin(self.gaama) + Y_temp*m.cos(self.gaama))*self.unit_pixels

                    X = x*(b**2+c**2) - y*(a*b) - z*(a*c)
                    Y = y*(a**2+c**2) - z*(b*c) - x*(a*b)
                    Z = z*(a**2+b**2) - y*(b*c) - x*(a*c)

                    lamda = m.sqrt(b**2+c**2)
                    v = m.sqrt(a**2+b**2+c**2)
                    if lamda == 0:
                        lamdax = 1
                        c=1
                    else:
                        lamdax = lamda

                    X,Y,Z = self.rotate_xaxis((X,Y,Z), cos_val = c/lamdax, sin_val = b/lamdax)
                    X,Y,Z = self.rotate_yaxis((X,Y,Z), cos_val = lamda/v, sin_val = -a/v)

                    new_vxaxis = self.rotate_xaxis(self.vxaxis, cos_val = c/lamdax, sin_val = b/lamdax)
                    new_vxaxis = self.rotate_yaxis(new_vxaxis, cos_val = lamda/v, sin_val = -a/v)

                    new_referencepoint = self.rotate_xaxis(self.reference_point, cos_val = c/lamdax, sin_val = b/lamdax)
                    new_referencepoint = self.rotate_yaxis(new_referencepoint, cos_val = lamda/v, sin_val = -a/v)

                    if new_vxaxis[1]>=0 and new_referencepoint[1]>=0:
                        gaama = m.asin(new_vxaxis[1])
                    elif new_referencepoint[1]<=0:
                        gaama = m.pi - m.asin(new_vxaxis[1])
                    else:
                        gaama = 2*m.pi + m.asin(new_vxaxis[1])

                    X,Y,Z = self.rotate_zaxis((X,Y,Z),theeta = -gaama)
                    X = X*self.unit_pixels + self.csize/2
                    Y = self.csize/2 - Y*self.unit_pixels
                    return_polygon.append((X,Y))
                return_polygon.append('#%02x%02x%02x' % polygon[-1])

                return_surface.append(return_polygon)
            return_coords.append(return_surface)

        return return_coords

    def delete_polygon(self):
        for polygon in self.printed_polygons:
            self.canvas.delete(polygon)

        self.printed_polygons = []

    def print_object(self , during_animation = 0):
        self.delete_polygon()
        twoD_coords = self.display_surfaces(self.threeD_to_twoD())
        self.dynamic_colours()
        for surface in twoD_coords:
            for polygon in surface:
                self.printed_polygons.append(self.canvas.create_polygon(polygon[:-1], fill = polygon[-1]))
        self.canvas.update()

        if during_animation:
            t.sleep(1/self.frame_rate)

    def change_angles(self, change_alpha, change_beeta, change_gaama):
        self.alpha += change_alpha
        self.beeta += change_beeta
        self.gaama += change_gaama
        self.set_view_point()

    def set_angles(self, alpha = None, beeta = None, gaama = None):
        if alpha == None and beeta == None and gaama ==None:
            pass
        else:
            self.alpha = alpha
            self.beeta = beeta
            self.gaama = gaama
            self.set_view_point()

    @staticmethod
    def rotate_xaxis(point, theeta = None, cos_val = None, sin_val = None):
        if cos_val == None:
            cos_val = m.cos(theeta)
        if sin_val == None:
            sin_val = m.sin(theeta)

        x,y,z = point
        Y = y*cos_val - z*sin_val
        Z = y*sin_val + z*cos_val

        return (x,Y,Z)

    @staticmethod
    def rotate_yaxis(point, theeta = None, cos_val = None, sin_val = None):
        if cos_val == None:
            cos_val = m.cos(theeta)
        if sin_val == None:
            sin_val = m.sin(theeta)

        x,y,z = point
        X = x*cos_val + z*sin_val
        Z = -x*sin_val + z*cos_val

        return (X,y,Z)

    @staticmethod
    def rotate_zaxis(point, theeta = None, cos_val = None, sin_val = None):
        if cos_val == None:
            cos_val = m.cos(theeta)
        if sin_val == None:
            sin_val = m.sin(theeta)

        x,y,z = point
        X = x*cos_val - y*sin_val
        Y = x*sin_val + y*cos_val

        return (X,Y,z)

    def rotate_point_about_line(self, point, angle, line_vector):
        a,b,c = line_vector
        lamda = m.sqrt(b**2+c**2)
        v = m.sqrt(a**2+b**2+c**2)
        if lamda == 0:
            lamdax = 1
            c=1
        else:
            lamdax = lamda

        # print(line_vector)
        p = self.rotate_xaxis(point, cos_val = c/lamdax, sin_val = b/lamdax)
        p = self.rotate_yaxis(p, cos_val = lamda/v, sin_val = -a/v)
        p = self.rotate_zaxis(p, theeta = angle)
        p = self.rotate_yaxis(p, cos_val = lamda/v, sin_val = a/v)
        p = self.rotate_xaxis(p, cos_val = c/lamdax, sin_val = -b/lamdax)

        return p

    def set_virtual_axis(self, reference_point = (0,1,0)):
        self.reference_point = reference_point
        x1,y1,z1 = reference_point
        x2,y2,z2 = self.a,self.b,self.c
        self.vxaxis = (y1*z2-y2*z1, x2*z1-x1*z2, x1*y2-x2*y1)

    def set_first_click(self, event):
        self.mouse_loc = (event.x, event.y)

    def change_view_angle(self, event):
        self.canvas.unbind('<B1-Motion>', self.move)
        x_diff = event.x - self.mouse_loc[0]
        y_diff = event.y - self.mouse_loc[1]
        const = m.pi/(self.unit_pixels*4)
        alpha_change = -x_diff * const
        beeta_change = y_diff * const
        #print(self.reference_point)
        new_viewpoint = self.rotate_point_about_line((self.a,self.b,self.c),alpha_change,self.reference_point)
        new_viewpoint = self.rotate_point_about_line(new_viewpoint,-beeta_change,self.vxaxis)
        new_referencepoint = self.rotate_point_about_line(self.reference_point,-beeta_change,self.vxaxis)
        #print(self.vxaxis)
        # print('Angles: ',(self.alpha/m.pi,self.beeta/m.pi,self.gaama/m.pi))
        # print('viewpoint: ',self.reference_point)
        # print('vxaxis: ',self.vxaxis)
        self.set_view_point(new_viewpoint,new_referencepoint)
        #self.set_angles()

        self.print_object(1)
        # print((self.alpha/m.pi,self.beeta/m.pi,self.gaama/m.pi))
        self.mouse_loc = (event.x, event.y)
        self.move = self.canvas.bind('<B1-Motion>', self.change_view_angle)

    def dynamic_movement(self):
        self.start_move = self.canvas.bind('<Button-1>', self.set_first_click)
        self.move = self.canvas.bind('<B1-Motion>', self.change_view_angle)

    def stop_dynamic_movement(self):
        self.canvas.unbind('<Button-1>', self.start_move)
        self.canvas.unbind('<B1-Motion>',self.move)

    def change_colour(self, colours):
        for i in range(len(self.coords)):
            for j in range(len(self.coords[i])):
                self.colours[i][j][-1] = colours[i][j]

    def set_colour(self, colours = None):
        if colours == None:
            self.colours = []
            for surface in self.coords:
                s = []
                for polygon in surface:
                    s.append(polygon[-1])
                self.colours.append(s)
        else:
            self.colours = colours

    def dynamic_colours(self):
        a1,b1,c1 = self.a,self.b,self.c

        for i in range(len(self.coords)):
            a2,b2,c2 = self.s_equations[i][0],self.s_equations[i][1],self.s_equations[i][2]
            d = self.dist((a2,b2,c2),(0,0,0))
            a2,b2,c2 = a2/d,b2/d,c2/d

            cos_angle = a1*a2+b1*b2+c1*c2
            if cos_angle>=0:
                for j in range(len(self.coords[i])):
                    r,g,b = self.colours[i][j]
                    r,g,b = r*cos_angle + r/3*(1-cos_angle),g*cos_angle + g/3*(1-cos_angle),b*cos_angle + b/3*(1-cos_angle)
                    self.coords[i][j][-1] = (int(r),int(g),int(b))


# cube_coords = [[(1,-1,1),(-1,-1,1),(-1,-1,-1),(1,-1,-1),(1,1,-1),(1,1,1),(-1,1,1),(-1,1,-1)],[[5,6,1,0,(255,255,255)]],[[4,5,0,3,(0,255,0)]],[[2,7,4,3,(0,0,255)]],[[1,6,7,2,(255,255,255)]],[[6,5,4,7,(0,255,255)]],[[1,2,3,0,(255,255,0)]]]
# cone_coords = [[(1,-1,1),(-1,-1,1),(-1,-1,-1),(1,-1,-1),(0,1,0)],[[1,2,3,0,(255,0,0)]],[[1,0,4,(255,0,0)]],[[0,3,4,(255,0,0)]],[[2,4,3,(255,0,0)]],[[1,4,2,(255,0,0)]]]
# cube = ThreeD(canvas, cube_coords)
# cone = ThreeD(canvas, cone_coords)
# cube.print_object()
# cube.dynamic_movement()
# cone.print_object()
# cone.dynamic_movement()

class input_info():

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("3D Renderer")

        self.heading_frame = tk.Frame(self.root)
        heading = tk.Label(self.heading_frame, text = "3D Renderer", font = ("Arial Black", 30))

        self.body_frame = tk.Frame(self.root)
        q = tk.Label(self.body_frame, text = '''Please input the 3D coordinates of the corner points of your shape.
        (It should be of the form (x,y,z):(x,y,z):(x,y,z):.....)''', font = ("Arial", 18))
        q2 = tk.Label(self.body_frame, text = '''Please input the number of sides in your 3D shape.''', font = ("Arial", 18))


        self.points_input = tk.Entry(self.body_frame, font = ("Arial", 18), width = 50)
        self.surface_input = tk.Entry(self.body_frame, font = ("Arial", 18))

        empty_label = tk.Label(self.body_frame, text = '')

        self.button_frame = tk.Frame(self.root)
        done_button = tk.Button(self.button_frame, text = "Done", height = 2, width = 20, bg = "grey", command = self.connect_points)


        self.heading_frame.pack(side = 'top')
        self.body_frame.pack()
        heading.pack()
        q.grid(row = 0)
        self.points_input.grid(row = 1)
        empty_label.grid(row = 2)
        q2.grid(row = 3)
        self.surface_input.grid(row = 4)
        self.button_frame.pack(side = 'bottom')
        done_button.grid(row = 0, pady = 15)

        self.root.mainloop()

    def set_points(self):
        temp_points = self.points_input.get()
        temp_points2 = ''

        for stuff in temp_points:
            if stuff!=' ':
                temp_points2+=stuff

        try:
            point_list = temp_points2.split(':')
            self.points = []

            for point in point_list:
                x,y,z = point[1:-1].split(",")
                self.points.append((int(x),int(y),int(z)))

            self.surfaces = int(self.surface_input.get())

            self.body_frame.destroy()
            self.button_frame.destroy()
            return 1

        except:
            error_label = tk.Label(self.body_frame, text = "There's something wrong in your input!",  font = ("Arial", 14))
            error_label.grid(row = 5)
            return 0

    def connect_points(self):
        if self.set_points():
            self.curr_index = 0
            self.body_frame = tk.Frame(self.root)
            index_frame = tk.Frame(self.body_frame)
            input_frame = tk.Frame(self.body_frame)
            self.button_frame = tk.Frame(self.root)
            self.order_list = []
            self.side_label = tk.Label(self.body_frame, text = "Side "+str(self.curr_index+1), font = ("Arial", 28))
            point_index = tk.Label(index_frame, text = "Points\n"+ self.get_points_string(), font = ("Arial", 18))
            instruction = tk.Label(input_frame, text = "Input the idexes of the points that connect to make this side (For eg. 0,2,4,3), and choose its colour.\nMake sure you use the right hand rule for the order of the points.", font = ("Arial", 15))
            self.order_input = tk.Entry(input_frame, font = ("Arial", 18))
            next_button = tk.Button(self.button_frame, text = 'Next', bg = 'grey', height = 3, width = 30, command = self.go_next)
            back_button = tk.Button(self.button_frame, text = 'Back', bg = 'grey', height = 3, width = 30, command = self.go_back)
            self.colour_chosen = (255,255,255)
            self.error = 0
            self.colour_button = tk.Button(input_frame, text = 'Choose colour', bg = 'grey', command = self.colour_chooser)
            self.body_frame.pack(side = 'top')
            self.button_frame.pack(side = 'bottom')
            self.side_label.grid(row = 0, columnspan = 2)
            index_frame.grid(row = 1, column = 0)
            input_frame.grid(row = 1, column = 1)
            point_index.pack()
            instruction.grid(row = 0)
            self.order_input.grid(row = 1)
            self.colour_button.grid(row = 2)
            back_button.grid(row = 0, column = 0, padx = 25)
            next_button.grid(row = 0, column = 1, padx = 25)


    def get_points_string(self):
        index = 0
        final_string = ''

        for point in self.points:
            final_string+=str(index)+': '+str(point)+'\n'
            index+=1

        return final_string

    def go_next(self):
        if self.error:
            self.error_label.destroy()
        if self.curr_index<self.surfaces:
            order = self.order_input.get()
            if self.check_order(order):
                self.order_input.delete(0,len(order))
                order = order.split(',')
                for i in range(len(order)):
                    order[i] = int(order[i])
                order.append(self.colour_chosen)
                self.colour_chosen = (255,255,255)
                if self.curr_index==self.surfaces-1:
                    self.order_list.append([order])
                    self.draw_shape()
                else:
                    self.curr_index+=1
                    self.colour_button.config(bg = 'grey')
                    self.order_list.append([order])
                    self.side_label.config(text = "Side "+str(self.curr_index+1))


    def go_back(self):
        if self.curr_index>0:
            self.curr_index-=1
            self.order_list = self.order_list[:-1]
            self.side_label.config(text = "Side "+str(self.curr_index+1))
            self.order_input.delete(0,len(self.order_input.get()))

    def colour_chooser(self):
        r,g,b = c_chooser.askcolor()[0]
        self.colour_chosen = (int(r),int(g),int(b))
        self.colour_button.config(bg = '#%02x%02x%02x' % self.colour_chosen)

    def draw_shape(self):
        self.body_frame.destroy()
        self.button_frame.destroy()
        canvas = tk.Canvas(self.root)
        canvas.pack()
        shape = ThreeD(canvas, [self.points]+self.order_list)
        shape.print_object()
        shape.dynamic_movement()

    def check_order(self,order):
        try:
            indexes = order.split(',')
            self.error = 0
            for i in range(len(indexes)):
                indexes[i] = int(indexes[i])
                if indexes[i]>=len(self.points):
                    self.error = 1
        except:
            self.error = 1

        if self.error:
            self.error_label = tk.Label(self.body_frame, text = "There's something wrong with your input!", font = ("Arial",18))
            self.error_label.grid(row = 2, columnspan = 2)

        return not self.error


if __name__ == '__main__':
    Input = input_info()