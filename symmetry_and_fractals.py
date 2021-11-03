from tkinter import *
from tkinter import ttk
import tkmacosx as tkmac
import math
import cmath


class Application(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.set_style()

        # Initiate the application window and display for the objects
        self.grid(row=0, column=0, rowspan=5, columnspan=6)
        self.config(highlightthickness=10)
        self.width = 900
        self.height = 600
        self.level = 0
        self.disp = Canvas(self, width=self.width, height=self.height,
                           bg=pale_yellow, cursor="exchange",
                           highlightthickness=10,
                           highlightbackground=light_blue)
        self.disp.grid(column=0, row=0, columnspan=11, rowspan=5)

        # Initiate styles and label configurations
        self.set_labels()

        # Initiate the two fractal classes
        self.tri_class = SierpinskiTriangle(self.width, self.height)
        self.isl_class = GosperIsland(self.width, self.height)

        # Add buttons onto the display window
        self.triangle_mode_btn()
        self.island_mode_btn()
        self.clear_canvas_btn()

        # Set up initial condidtions for objects.
        self.triangle = False
        self.island = False
        self.anchor = False
        self.coords_updr = False

        self.mirrors = False
        self.m_count = 0

        self.zoom_count = 0

        self.tile_button = 0
        self.tile_count = 0
        self.tiles_ls = []

        self.centrey_updr = 0
        self.centrex_updr = 0
        self.pos_vecs = []

        self.first_time = 1

    def set_labels(self):
        # Initiate and place global text in the NW corner
        self.instructions = StringVar()
        self.instructions.set('LEFT MOUSE BUTTON to pan\n'
                              + 'RIGHT MOUSE BUTTON to rotate\n'
                              + 'SCROLL OR "+" AND "-" to zoom\n'
                              + 'ARROW KEYS to change level\n'
                              + '"m" to show mirror lines')
        self.instruct_lbl = ttk.Label(self.disp, textvariable=self.instructions,
                                      style='InstructLabel.TLabel')
        self.instruct_lbl.place(relx=0.03, rely=0.1, anchor="w")

        # Create Text for the SE corner
        self.rot_txt = StringVar()
        self.rot_txt.set("0°")
        self.rot_label = ttk.Label(self.disp, textvariable=self.rot_txt,
                                   style='RotLabel.TLabel')

        self.lvl_txt = StringVar()
        self.lvl_txt.set("Level %d" % self.level)
        self.lvl_lbl = ttk.Label(self.disp, textvariable=self.lvl_txt,
                                 style='SubTtlLabel.TLabel')

        # Initiate Text for the NE Corner (title and object information)
        self.ttl_txt1 = StringVar()
        self.ttl_lbl1 = ttk.Label(self.disp, textvariable=self.ttl_txt1,
                                  style='TtlLabel.TLabel')

        self.ttl_txt2 = StringVar()
        self.ttl_lbl2 = ttk.Label(self.disp, textvariable=self.ttl_txt2,
                                  style='TtlLabel.TLabel')

        self.subttl_txt = StringVar()
        self.subttl = ttk.Label(self.disp, textvariable=self.subttl_txt,
                                style='SubTtlLabel.TLabel')

        # Initiate labels for misc. messages.
        self.mr_error = StringVar()
        self.mr_error.set('Mirrors look weird? Hit "Clear".')
        self.mr_error_lbl = ttk.Label(self, textvariable=self.mr_error,
                                      style='ErrorLabel.TLabel')

        self.no_shape_error = StringVar()
        self.no_shape_error.set('Please Initialise a shape first!')
        self.no_shape_error_lbl = ttk.Label(self, textvariable=self.no_shape_error,
                                      style='ErrorLabel.TLabel')

        self.no_shape_error = StringVar()
        self.no_shape_error.set('Please Initialise a shape first!')
        self.no_shape_error_lbl = ttk.Label(self, textvariable=self.no_shape_error,
                                      style='ErrorLabel.TLabel')

        self.isl_mr_error = StringVar()
        self.isl_mr_error.set('There are no mirror lines!')
        self.isl_mr_error_lbl = ttk.Label(self, textvariable=self.isl_mr_error,
                                      style='ErrorLabel.TLabel')

        self.error_ls = [self.mr_error_lbl, self.no_shape_error_lbl,
                         self.isl_mr_error_lbl]

        self.isl_tile_level = StringVar()
        self.isl_tile_level.set('Go to the next levels + zoom.')
        self.isl_tile_level_lbl = ttk.Label(self, textvariable=self.isl_tile_level,
                                      style='ErrorLabel.TLabel')

        # Create list of labels to remove on clear.
        self.forget_on_clear = [self.subttl,
                                self.ttl_lbl1,
                                self.ttl_lbl2,
                                self.lvl_lbl,
                                self.rot_label,
                                self.isl_tile_level_lbl
                                ] + self.error_ls

    def set_style(self):
        # Customise colour palettes.
        global pale_yellow, dark_blue, light_blue, yellow
        pale_yellow = '#f2f1e8'
        dark_blue = '#40556b'
        light_blue = '#97babb'
        yellow = '#d9c267'

        # Create styles for buttons
        self.style = {'dark_btn': {'bg': dark_blue, 'fg': light_blue, 
                                   'font': ('DIN Alternate', 16),
                                   'borderless': True, 'padx': 0,
                                   'highlightthickness': 0},
                      'light_btn': {'bg': pale_yellow, 'fg': dark_blue, 
                                   'font': ('DIN Alternate', 16),
                                   'borderless': True, 'padx': 0,
                                   'highlightthickness': 0}
                     }

        # Create styles for various labels
        style = ttk.Style()
        style.theme_use('classic')
        style.configure('TtlLabel.TLabel', font=('DIN Alternate', 36),
                        background=pale_yellow, foreground=light_blue,
                        anchor=RIGHT, )
        style.configure('SubTtlLabel.TLabel', font=('DIN Condensed', 25),
                        background=pale_yellow, foreground=dark_blue,
                        anchor=RIGHT, )
        style.configure('RotLabel.TLabel', font=('DIN Alternate', 25),
                        background=dark_blue, foreground=pale_yellow,
                        anchor=RIGHT, width=7)
        style.configure('InstructLabel.TLabel', font=('DIN Alternate', 15),
                        background=pale_yellow, foreground=dark_blue,
                        anchor=LEFT)
        style.configure('ErrorLabel.TLabel', font=('DIN Alternate', 15),
                        background=yellow, foreground=dark_blue,
                        anchor=CENTER, padx=2)

    def apply_style(self, style_type, obj_name):
        # For any buttons, add styles.
        for key in self.style[style_type].keys():
            obj_name[key] = self.style[style_type][key]


    def clear_canvas(self, all_obj=True):
        for item in self.forget_on_clear:
            item.grid_forget()
            item.place_forget()
        self.disp.delete('shape', 'shape-aux')
        if all_obj:
            self.disp.delete('tiling')
            self.tile_count = 0
        self.m_count = 0
        self.rot_txt.set("0°")
        self.zoom_count = 0
        self.pos_vecs = []
        self.tile_button.grid_forget()

        if self.curr_obj == self.tri_class:
            self.centrex, self.centrey = self.og_centrex, self.og_centrey
        self.origin = complex(self.centrex, self.centrey)

    def triangle_mode_btn(self):
        self.tri_button = tkmac.Button(self, text="Triangle Mode (t)",
                                 command=lambda: self.draw_obj(self.tri_class))
        self.apply_style('dark_btn', self.tri_button)
        self.tri_button.grid(row=5, column=0)

    def island_mode_btn(self):
        self.isl_button = tkmac.Button(self, text="Island Mode (i)", 
                                 command=lambda: self.draw_obj(self.isl_class))
        self.apply_style('dark_btn', self.isl_button)
        self.isl_button.grid(row=5, column=1)

    def tile_mode_button(self):
        self.tile_button = tkmac.Button(self, text="TILE!!", command=self.tile_event)
        self.apply_style('light_btn', self.tile_button)
        self.tile_button.grid(row=5, column=2)

    def clear_canvas_btn(self):
        self.clear_button = tkmac.Button(self, text="Clear (c)", command=self.clear_canvas)
        self.apply_style('dark_btn', self.clear_button)
        self.clear_button.grid(row=5, column=10, pady=15)

    def place_ttls(self):
        self.ttl_lbl1.place(relx=0.95, rely=0.1, anchor="e")
        self.ttl_lbl2.place(relx=0.95, rely=0.16, anchor="e")
        self.subttl.place(relx=0.95, rely=0.21, anchor="e")
        self.lvl_lbl.place(relx=0.95, rely=0.815, anchor="e")
        self.rot_label.place(relx=0.95, rely=0.87, anchor="e")

    def set_isl_centre(self):
        self.centrex, self.centrey = (self.width / 2,
                                      self.isl_class.y_offset
                                      + self.isl_class.length
                                      * math.sqrt(3) / 2)
        self.origin = complex(self.centrex, self.centrey)

    def set_tri_centre(self):
        # Retrieve the coordinates of the Sierpinski base.
        y_offset = self.tri_class.y_offset
        height = self.tri_class.height
        x1, y1, y2 = 450, y_offset, height + y_offset
        y3 = y2
        x2 = x1 - (y2 - y_offset) / math.sqrt(3)
        x3 = x1 + (y2 - y_offset) / math.sqrt(3)

        self.centrex, self.centrey = (x1, y_offset + 2 * height / 3)
        self.og_centrex, self.og_centrey = (x1, y_offset + 2 * height / 3)
        self.origin = complex(self.centrex, self.centrey)

        self.outer_coords = [(x1, y1), (x2, y2), (x3, y3)]
        self.og_outer_coords = [(x1, y1), (x2, y2), (x3, y3)]

    def draw_obj(self, mode):
        self.no_shape_error_lbl.grid_forget()

        # If there are already things on the canvas, reset the canvas 
        # except for any tilings.
        if self.first_time:
            self.first_time = 0
        else:
            self.clear_canvas(all_obj=False)

        # Set the x-position of the fractals
        if mode == self.tri_class:
            x = self.width / 2
        else:
            x = self.width / 2 - (mode.length / 2)

        # Get the coordinates for the fractal,
        # plus a list of original coordinates for resetting
        self.coords_ls = mode.get_coords(self.level, mode.length,
                                         mode.height, x, mode.y_offset)
        self.og_coords_ls = mode.get_coords(self.level, mode.length,
                                            mode.height, x, mode.y_offset)

        if mode == self.tri_class:
            # Create the triangle, with separate handling for level 0
            # and others due to coordinate storage differences
            self.set_tri_centre()
            if self.level == 0:
                self.triangle = self.disp.create_polygon(self.coords_ls,
                                                         fill=yellow,
                                                         tags=('shape'))
            else:
                self.triangle = []
                for item in self.coords_ls:
                    temp_tri = self.disp.create_polygon(item,
                                                        fill=yellow,
                                                        tags=('shape'))
                    self.disp.itemconfig(temp_tri, fill=yellow)
                    self.triangle.append(temp_tri)
            self.draw_tri_outline()

            self.ttl_txt1.set("SIERPINSKI'S")
            self.ttl_txt2.set("TRIANGLE")
            self.subttl_txt.set("(basic & cool)")

        elif mode == self.isl_class:
            self.set_isl_centre()
            self.island = self.disp.create_polygon(self.coords_ls,
                                                   fill="", width=10,
                                                   outline = yellow,
                                                   tags=('shape'))
            self.isl_outline = self.disp.create_polygon(self.coords_ls,
                                                        fill="", width=5,
                                                        activewidth=10,
                                                        dash=(2, 1, 2, 1),
                                                        outline=dark_blue,
                                                        tags=('shape-aux'))
            self.outer_coords = self.og_coords_ls.copy()
            self.og_outer_coords = self.outer_coords.copy()

            self.ttl_txt1.set("THE GOSPER")
            self.ttl_txt2.set("ISLAND")
            self.subttl_txt.set("(unique & cool)")

        self.curr_obj = mode
        self.draw_anchor()
        self.place_ttls()
        self.tile_mode_button()

    def draw_tri_outline(self):
        self.tri_outline = self.disp.create_polygon(self.outer_coords, activewidth=10,
                                                    width=5, dash=(2, 1, 2, 1),
                                                    outline=dark_blue, fill="",
                                                    tags=('shape-aux'))

    def draw_anchor(self):
        temp_coord = self.coords_ls[0]
        if self.curr_obj == self.isl_class or self.level == 0:

            self.anchor_coords = [(temp_coord[0], temp_coord[1] + 10),
                                  (temp_coord[0] + 10, temp_coord[1]),
                                  (temp_coord[0], temp_coord[1] - 10),
                                  (temp_coord[0] - 10, temp_coord[1])]
        else:
            self.anchor_coords = [(temp_coord[0][0], temp_coord[0][1] + 10),
                                  (temp_coord[0][0] + 10, temp_coord[0][1]),
                                  (temp_coord[0][0], temp_coord[0][1] - 10),
                                  (temp_coord[0][0] - 10, temp_coord[0][1])]

        if self.anchor:
            self.disp.delete(self.anchor)

        self.anchor = self.disp.create_polygon(self.anchor_coords, fill=light_blue,
                                               tags=('shape-aux'))

    def get_angle(self, event):
        if not self.triangle and not self.island:
            self.no_shape_error_lbl.grid(row=5, column=6, columnspan=3)
            return

        # Get the distance from the centre to the x and y position of cursor
        dx = event.x - self.centrex
        dy = event.y - self.centrey
        direction_vector = complex(dx, dy)

        if direction_vector == complex(0):
            return 0.0
        else:
            return direction_vector / abs(direction_vector)

    def apply_rotation(self, to_rotate, rotation, origin):
        rotd_vertices = []
        coords_updr = []
        # print(to_rotate)
        for x, y in to_rotate:
            # get the postion of the vertices relative to the center
            # of the triangle.
            pos_vector = complex(x, y) - origin
            rotd_vector = pos_vector * rotation
            absolute_vertex = rotd_vector + origin

            rotd_vertices.append(absolute_vertex.real)
            rotd_vertices.append(absolute_vertex.imag)

            coords_updr.append((absolute_vertex.real, absolute_vertex.imag))
        return rotd_vertices, coords_updr

    def get_pre_rot_angle(self):
        x2, y2 = self.outer_coords[0]
        x1, y1 = self.og_outer_coords[0]

        vec1 = (complex(x2, y2) - self.origin)
        vec1 = vec1 / abs(vec1)
        vec2 = complex(x1, y1) - self.origin
        vec2 = vec2 / abs(vec2)

        base_angle = vec1 / vec2
        return base_angle

    def initiate_rot(self, event):
        self.init_angle = self.get_angle(event)

    def rotate(self, event):
        if not self.triangle and not self.island:
            self.no_shape_error_lbl.grid(row=5, column=6, columnspan=3)
            return

        # Get the angle of rotation from init. click
        # and set the rotation label.
        rotation = self.get_angle(event) / self.init_angle
        self.rot_txt.set(f"{round(cmath.phase(rotation) * 180 / cmath.pi, 1)}")

        # Get the amount the object has already been rotated by
        base = self.get_pre_rot_angle()
        new_angle = cmath.phase(rotation) * 180 / cmath.pi + cmath.phase(base) * 180 / cmath.pi
        if new_angle < 0:
            new_angle += 360
        self.rot_txt.set(f"{round(new_angle % 360, 1)}°")

        if self.curr_obj == self.tri_class:
            if self.level == 0:
                rotd_vertices, self.coords_updr = self.apply_rotation(self.coords_ls, rotation, self.origin)
                self.disp.coords(self.triangle, *rotd_vertices)
            elif self.level > 0:
                self.coords_updr = []
                for i in range(len(self.coords_ls)):
                    # for i in range(len(item)):
                    rotd_vertices, temp_coords_updr = self.apply_rotation(self.coords_ls[i], rotation, self.origin)
                    self.coords_updr.append(temp_coords_updr)
                    self.disp.coords(self.triangle[i], *rotd_vertices)
        elif self.curr_obj == self.isl_class:
            rotd_vertices, self.coords_updr = self.apply_rotation(self.coords_ls, rotation, self.origin)
            self.disp.coords(self.island, *rotd_vertices)

        rotd_anchor_vertices, discard = self.apply_rotation(self.anchor_coords, rotation, self.origin)
        self.disp.coords(self.anchor, *rotd_anchor_vertices)

        if self.mirrors:
            self.mr_coords_updr = []
            for i in range(len(self.mirrors_coords)):
                pair = self.mirrors_coords[i]
                mr_rot_vertices, mr_coords_temp = self.apply_rotation(pair, rotation, self.origin)
                self.disp.coords(self.mirrors[i], *mr_rot_vertices)
                self.mr_coords_updr.append(mr_coords_temp)

    def zoom_action(self, event, coords, coord_num):
        temp_zoom_updr = []
        zoomed_coords = []
        # For each of the original vertices, add their positions to a list.
        for x, y in coords:
            pos_vector = complex(x,y) - self.origin
            if self.curr_obj == self.tri_class:
                if (self.zoom_count < (3 ** (self.level + 1)) 
                        and len(self.pos_vecs) <= (3 ** (self.level + 1))):
                    self.pos_vecs.append((pos_vector.real, pos_vector.imag))
                if self.level == 0:
                    rad_vector = complex(self.coords_ls[0][0],
                                         self.coords_ls[0][1])
                else:
                    rad_vector = complex(self.coords_ls[0][0][0],
                                         self.coords_ls[0][0][1])
            else:
                if (self.zoom_count < 6 * (3 ** (self.level)) 
                        and len(self.pos_vecs) <= 6 * (3 ** (self.level))):
                    self.pos_vecs.append((pos_vector.real, pos_vector.imag))
                rad_vector = complex(self.coords_ls[0][0], self.coords_ls[0][1])
            direction = complex(self.pos_vecs[coord_num][0], 
                                self.pos_vecs[coord_num][1]) / abs(rad_vector)
            coord_num += 1

            if event.delta > 0 or event.char == '=':
                zoom_coord = pos_vector + 50 * direction + self.origin
                self.zoom_count += 1
            elif event.delta < 0 or event.char == '-':
                zoom_coord = pos_vector - 50 * direction + self.origin
                self.zoom_count -= 1

            zoomedx, zoomedy = zoom_coord.real, zoom_coord.imag
            zoomed_coords.append(zoomedx)
            zoomed_coords.append(zoomedy)
            temp_zoom_updr.append((zoomedx, zoomedy))

        return zoomed_coords, temp_zoom_updr, coord_num

    def zoom_event(self, event):
        if not self.triangle and not self.island:
            self.no_shape_error_lbl.grid(row=5, column=6, columnspan=3)
            return

        if self.curr_obj == self.tri_class:
            coord_num = 0
            if self.level == 0:
                zoomed_coords, zoom_updr, coord_num = self.zoom_action(event, self.coords_ls, coord_num)
                self.disp.coords(self.triangle, *zoomed_coords)
                self.coords_ls = zoom_updr
            else:
                temp_coords_updr= []
                for i in range(len(self.coords_ls)):
                    item = self.coords_ls[i]
                    zoomed_coords, zoom_updr, coord_num = self.zoom_action(event, item, coord_num)
                    self.disp.coords(self.triangle[i], *zoomed_coords)
                    temp_coords_updr.append(zoom_updr)
                self.coords_ls = temp_coords_updr
        else:
            coord_num = 0
            zoomed_coords, zoom_updr, coord_num = self.zoom_action(event, self.coords_ls, coord_num)
            self.disp.coords(self.island, *zoomed_coords)
            self.coords_ls = zoom_updr

        if self.mirrors:
            for item in self.mirrors:
                self.disp.delete(item)
            self.show_mirrors()
            self.mr_error_lbl.grid(row=5, column=5, columnspan=4)

        self.draw_anchor()

    def initiate_pan(self, event):
        self.init_pan_pos = (event.x, event.y)

    def pan_action(self, coords, pan_vec):
        temp_pan_updr = []
        panned_coords = []
        for x, y in coords:
            pannedx = x + pan_vec[0]
            pannedy = y + pan_vec[1]         
            panned_coords.append(pannedx)
            panned_coords.append(pannedy)
            temp_pan_updr.append((pannedx, pannedy))
        return panned_coords, temp_pan_updr

    def pan_event(self, event):
        if not self.triangle and not self.island:
            self.no_shape_error_lbl.grid(row=5, column=6, columnspan=3)
            return

        delta_pan_pos = (event.x - self.init_pan_pos[0],
                         event.y - self.init_pan_pos[1])

        # Update the centre coordinates
        self.centrex += delta_pan_pos[0]
        self.centrey += delta_pan_pos[1]

        if self.curr_obj == self.tri_class:
            if self.level == 0:
                panned_coords, pan_updr = self.pan_action(self.coords_ls, 
                                                          delta_pan_pos)
                self.disp.coords(self.triangle, *panned_coords)
                self.coords_ls = pan_updr
            else:
                temp_coords_updr= []
                for i in range(len(self.coords_ls)):
                    item = self.coords_ls[i]
                    panned_coords, pan_updr = self.pan_action(item,
                                                              delta_pan_pos)
                    self.disp.coords(self.triangle[i], *panned_coords)
                    temp_coords_updr.append(pan_updr)
                self.coords_ls = temp_coords_updr
        else:
            panned_coords, pan_updr = self.pan_action(self.coords_ls,
                                                      delta_pan_pos)
            self.disp.coords(self.island, *panned_coords)
            self.coords_ls = pan_updr

        self.init_pan_pos = (event.x, event.y)

        # Update the position of the anchor
        panned_anchor_coords, pan_anchor_updr = self.pan_action(self.anchor_coords,
                                                                delta_pan_pos)
        self.disp.coords(self.anchor, *panned_anchor_coords)
        self.anchor_coords = pan_anchor_updr

        if self.mirrors:
            self.mr_coords_updr = []
            for i in range(len(self.mirrors_coords)):
                pair = self.mirrors_coords[i]
                panned_mr_coords, mr_coords_temp = self.pan_action(pair, delta_pan_pos)
                self.disp.coords(self.mirrors[i], *panned_mr_coords)
                self.mr_coords_updr.append(mr_coords_temp)
            self.mirrors_coords = self.mr_coords_updr

    def create_mirrors(self, coord):
        x, y = coord[0], coord[1]
        origin = complex(self.centrex, self.centrey)
        vertex_vec = complex(x, y) - origin
        direction_vector = vertex_vec / abs(vertex_vec)

        p1 = vertex_vec + 2000 * direction_vector + origin
        p2 = self.origin - (vertex_vec + 2000 * direction_vector)

        self.mirrors_coords.append([(p1.real, p1.imag), (p2.real, p2.imag)])
        self.mirrors.append(self.disp.create_line(p1.real, p1.imag,
                                                 p2.real, p2.imag,
                                                 dash=(5, 2),
                                                 fill=light_blue,
                                                 width=2, tags=('shape_aux')))

    def show_mirrors(self):
        self.mirrors_coords = []
        self.mirrors = []
        if self.curr_obj == self.tri_class:
            for coordinate in self.outer_coords:
                self.create_mirrors(coordinate)
        elif self.level == 0:
            for i in range(0,3):
                coord1 = self.og_outer_coords[i]
                self.create_mirrors(coord1)

                v = complex(coord1[0], coord1[1])
                x2, y2 = self.og_outer_coords[i+1]
                w = complex(x2, y2)
                vertex_vec2 = v + 1 / 2 * (w - v)

                self.create_mirrors((vertex_vec2.real, vertex_vec2.imag))
        elif self.level == 1:
            for i in range(2, 9, 3):
                coord1 = self.og_outer_coords[i]
                self.create_mirrors(coord1)

                v = complex(coord1[0], coord1[1])
                x2, y2 = self.og_outer_coords[i + 3]
                w = complex(x2, y2)
                vertex_vec2 = v + 1 / 2 * (w - v)

                self.create_mirrors((vertex_vec2.real, vertex_vec2.imag))
        else:
            self.isl_mr_error_lbl.grid(row=5, column=5, columnspan=4)

    def toggle_mirrors(self, event):
        if not self.triangle and not self.island:
            self.no_shape_error_lbl.grid(row=5, column=6, columnspan=3)
            return
    
        self.m_count += 1
        if self.m_count // 2 == 0:
            self.show_mirrors()
        elif self.curr_obj == self.isl_class and self.level > 1:
            for item in self.mirrors:
                self.disp.itemconfig(item, state="hidden")
            self.isl_mr_error_lbl.grid(row=5, column=5, columnspan=4)
        elif self.m_count % 2 == 0:
            for item in self.mirrors:
                self.disp.itemconfig(item, state="hidden")
        elif self.m_count % 2 == 1:
            for item in self.mirrors:
                self.disp.itemconfig(item, state="normal")

    def tile_action(self, shift_vec):
        shift_vec = (shift_vec.real, shift_vec.imag)
        if self.curr_obj == self.isl_class or self.level == 0:
            shifted_coords, temp_shift_updr = self.pan_action(self.og_coords_ls,
                                                              shift_vec)
            temp_shape = self.disp.create_polygon(shifted_coords, fill="", 
                                                  outline = dark_blue,
                                                  tags=('tiling'))
            self.tiles_ls.append(temp_shape)
        else:
            for item in self.og_coords_ls:
                shifted_coords, temp_shift_updr = self.pan_action(item,
                                                                  shift_vec)
                temp_shape = self.disp.create_polygon(shifted_coords, fill="",
                                                      outline = light_blue,
                                                      tags=('tiling'))
                self.tiles_ls.append(temp_shape)

    def tile(self):
        if self.curr_obj == self.isl_class:
            mag = math.sqrt(3) * self.isl_class.length
            for i in range(0, 6):
                for j in range(1, 4):
                    # Create the tiles immediately around the original
                    # and entending in those directions
                    shift_angle = math.pi / 6 + ((math.pi / 3) * i)
                    shift_vec = cmath.rect(mag * j, shift_angle)
                    self.tile_action(shift_vec)

                # Fill in the remaining layers of islands.
                shift_angle = ((math.pi / 3) * i)
                shift_vec = cmath.rect(mag * 3 / math.sqrt(3), shift_angle)
                self.tile_action(shift_vec)

                shift_angle = math.atan(math.sqrt(3) / 9) + ((math.pi / 3) * i)
                shift_vec = cmath.rect(mag * math.sqrt(21) / math.sqrt(3), shift_angle)
                self.tile_action(shift_vec)
        else:
            for i in range(0, 4 ):
                for j in range(0, 6):
                    # Create most triangles immediately adjacent
                    # to the orginal
                    mag = self.tri_class.length * math.sqrt((3 / 4) 
                                                            + (0.5 + i) ** 2)
                    shift_angle = math.atan(math.sqrt(3) / 2 / (0.5 + i))
                    shift_angle = shift_angle + (math.pi / 3) * j
                    shift_vec = cmath.rect(mag, shift_angle)
                    self.tile_action(shift_vec)

                    mag = self.tri_class.length * i
                    shift_angle = (math.pi / 3) * j
                    shift_vec = cmath.rect(mag, shift_angle)
                    self.tile_action(shift_vec)
            # fill in remaining triangles.
            mag = self.tri_class.length * math.sqrt((3 / 4) + (2.5) ** 2)
            shift_angle = -1 * math.atan(math.sqrt(3) / 5)
            shift_vec = cmath.rect(mag, shift_angle)
            self.tile_action(shift_vec)

            mag = self.tri_class.length * math.sqrt((3 / 4) + (2.5) ** 2)
            shift_angle = -1 * math.atan(math.sqrt(3) / 5) + math.pi
            shift_vec = cmath.rect(mag, shift_angle)
            self.tile_action(shift_vec)

            mag = self.tri_class.length * math.sqrt((3) + (3) ** 2)
            shift_angle = -1 * math.atan(math.sqrt(3) / 3)
            shift_vec = cmath.rect(mag, shift_angle)
            self.tile_action(shift_vec)

    def tile_event(self):
        if self.tile_count % 2 == 0:
            self.tile()
            self.isl_tile_level_lbl.grid(row=5, column=5, columnspan=4)
        else:
            self.disp.delete('tiling')

        # Handle toggling on and off
        self.tile_count += 1

    def key_press(self, event):
        # Handle keyboard input.
        if event.keysym == "t":
            self.draw_obj(self.tri_class)
        elif event.keysym == "i":
            self.draw_obj(self.isl_class)
        elif event.keysym in ["Up", "Right"]:
            self.level += 1
            self.draw_obj(self.curr_obj)
        elif event.keysym in ["Down", "Left"] and self.level > 0:
            self.level -= 1
            self.draw_obj(self.curr_obj)
            root.bind("=", w.zoom_event)
        elif event.char in ["-", "="]:
            self.zoom_event(event)
        elif event.keysym == "m":
            self.toggle_mirrors(event)
        elif event.keysym == "c":
            self.clear_canvas()

        # Reset the angle and level text
        self.rot_txt.set("0°")
        self.lvl_txt.set("Level %d" % self.level)

        # Remove mirrors from islands of level 2 or greater
        if self.curr_obj == self.isl_class and self.level > 1:
            for item in self.mirrors:
                self.disp.itemconfig(item, state="hidden")
            self.isl_mr_error_lbl.grid(row=5, column=5, columnspan=4)

class SierpinskiTriangle():
    def __init__(self, width, height):
        self.height = height - 450
        self.length = self.height * 2 / math.sqrt(3)
        self.dispw = width
        self.y_offset = 250
        self.centre()

    def centre(self):
        x1 = self.dispw / 2
        y1 = self.y_offset
        y2 = self.y_offset + self.height
        y3 = self.y_offset + self.height
        x2 = x1 - self.length / 2
        x3 = x1 + self.length / 2
        self.centrex, self.centrey = (x1, self.y_offset + 2 * self.height / 3)
        self.origin = complex(self.centrex, self.centrey)
        self.basexy = [(x1, y1), (x2, y2), (x3, y3)]

    def get_coords(self, level, length, height, x, y):
        if level == 0:
            return [(x, y),
                    (x - length / 2, y + height),
                    (x + length / 2, y + height)]
        coord_ls = []
        if level == 1:
            coord_ls.append(self.get_coords(level - 1, length / 2, height / 2,
                                            x, y))
            coord_ls.append(self.get_coords(level - 1, length / 2, height / 2,
                                            x - length / 4, y + height / 2))
            coord_ls.append(self.get_coords(level - 1, length / 2, height / 2,
                                            x + length / 4, y + height / 2))
        else:
            coord_ls += self.get_coords(level - 1, length / 2, height / 2,
                                        x, y)
            coord_ls += self.get_coords(level - 1, length / 2, height / 2,
                                        x - length / 4, y + height / 2)
            coord_ls += self.get_coords(level - 1, length / 2, height / 2,
                                        x + length / 4, y + height / 2)
        return coord_ls


class GosperIsland():
    def __init__(self, width, height):
        self.length = 100
        self.height = self.length * math.sqrt(3) / 2
        self.dispw = width
        self.y_offset = 250
        self.centre()

    def centre(self):
        self.centrex, self.centrey = (self.dispw / 2, self.y_offset + self.length * math.sqrt(3) / 2)
        self.origin = complex(self.centrex, self.centrey)

    def get_coords(self, level, length, width, x, y):
        coord_ls = []
        mini_a = (cmath.pi / 3) - math.asin(2 / math.sqrt(7) * math.sin(cmath.pi * 2 / 3))
        hex_a = 2 * cmath.pi / 3
        big_a = cmath.pi / 3
        start_coord = complex(x,y)
        curr_coord = start_coord
        curr_angle = 0
        new_side_length = length * ((1 / math.sqrt(7)) ** level)
        fs_pattern = self.get_fs_pattern(level)

        for i in range(6 * (3 ** level)):
            if i == 0:
                coord_ls.append((x,y))
            elif i == 1:
                curr_angle = hex_a + level * mini_a
                side_vec = cmath.rect(new_side_length, curr_angle)
                curr_coord = curr_coord + side_vec
                coord_ls.append((curr_coord.real, curr_coord.imag))
            elif level == 0:
                curr_angle -= big_a
                side_vec = cmath.rect(new_side_length, curr_angle)
                curr_coord = curr_coord + side_vec
                coord_ls.append((curr_coord.real, curr_coord.imag))
            else:
                if fs_pattern[i] == 0:
                    curr_angle -= big_a
                    side_vec = cmath.rect(new_side_length, curr_angle)
                    curr_coord = curr_coord + side_vec
                    coord_ls.append((curr_coord.real, curr_coord.imag))
                elif fs_pattern[i] == 1:
                    curr_angle += big_a
                    side_vec = cmath.rect(new_side_length, curr_angle)
                    curr_coord = curr_coord + side_vec
                    coord_ls.append((curr_coord.real, curr_coord.imag))
        return coord_ls

    def get_fs_pattern(self, level):
        num_ls = []  # Whether the next step should add (1) or substract (0)
        i = 0
        while i < 6 * (3 ** level):
            if i % 3 == 0:
                num_ls.append(1)
            else:
                num_ls.append(0)
            j = 2
            while j < level + 1:
                test = i % (3 ** j)
                compare_to = 3 ** (j) - (3 ** (j - 1) - 1)

                if test == compare_to:
                    if num_ls[i] == 0:
                        num_ls[i] = 1
                    else:
                        num_ls[i] = 0
                j += 1
            i += 1
        return num_ls

if __name__ == '__main__':
    root = Tk()
    root.geometry("950x700")
    w = Application(root)
    w.config(bg=light_blue, width=1000, height=700)

    w.disp.bind("<Button-2>", w.initiate_rot)
    w.disp.bind("<B2-Motion>", w.rotate, add="+")
    w.disp.bind("<Button-1>", w.initiate_pan)
    w.disp.bind("<B1-Motion>", w.pan_event)
    w.disp.bind("<MouseWheel>", w.zoom_event, add="+")
    root.bind("<Key>", w.key_press)

    w.master.mainloop()
