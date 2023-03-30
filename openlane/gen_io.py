#!/bin/python
import json, sys;

pdn_offset_x = 1380
pdn_offset_y = 2480
pdn_step_y = 2720
pdn_step_y_half = int(pdn_step_y / 2)

pin_width = 1000
pin_height = 300

pin_half_width = int(pin_width / 2)
pin_half_height = int(pin_height / 2)

def gen_rows():
    row = 0
    y = 0 + pdn_step_y
    ori = "N "
    while ((y + (2 * pdn_step_y)) < die_size_y):
        if ((row % 2) == 0):
            ori = "N "
        else:
            ori = "FS"
        s = "ROW ROW_{} unithd {} {} {} DO 320 BY 1 STEP 460 0 ;\n".format(
            row,
            pdn_offset_x,
            y,
            ori
        )
        f.write(s)
        row += 1
        y += pdn_step_y

def gen_tracks():
    f.write("TRACKS X 230 DO 326 STEP 460 LAYER li1 ;\n")
    f.write("TRACKS Y 170 DO 353 STEP 340 LAYER li1 ;\n")
    f.write("TRACKS X 170 DO 441 STEP 340 LAYER met1 ;\n")
    f.write("TRACKS Y 170 DO 353 STEP 340 LAYER met1 ;\n")
    f.write("TRACKS X 230 DO 326 STEP 460 LAYER met2 ;\n")
    f.write("TRACKS Y 230 DO 261 STEP 460 LAYER met2 ;\n")
    f.write("TRACKS X 340 DO 220 STEP 680 LAYER met3 ;\n")
    f.write("TRACKS Y 340 DO 176 STEP 680 LAYER met3 ;\n")
    f.write("TRACKS X 460 DO 163 STEP 920 LAYER met4 ;\n")
    f.write("TRACKS Y 460 DO 130 STEP 920 LAYER met4 ;\n")
    f.write("TRACKS X 1700 DO 44 STEP 3400 LAYER met5 ;\n")
    f.write("TRACKS Y 1700 DO 35 STEP 3400 LAYER met5 ;\n")
    f.write("VIAS 3 ;\n")
    f.write("    - via2_3_3000_480_1_9_320_320 + VIARULE M1M2_PR + CUTSIZE 150 150  + LAYERS met1 via met2  + CUTSPACING 170 170  + ENCLOSURE 85 165 55 85  + ROWCOL 1 9  ;\n")
    f.write("    - via3_4_3000_480_1_7_400_400 + VIARULE M2M3_PR + CUTSIZE 200 200  + LAYERS met2 via2 met3  + CUTSPACING 200 200  + ENCLOSURE 40 85 65 65  + ROWCOL 1 7  ;\n")
    f.write("    - via4_5_3000_480_1_7_400_400 + VIARULE M3M4_PR + CUTSIZE 200 200  + LAYERS met3 via3 met4  + CUTSPACING 200 200  + ENCLOSURE 90 60 200 65  + ROWCOL 1 7  ;\n")
    f.write("END VIAS\n")

def write_pin(name, x, y, is_horisontal, is_input):
    direction = "INPUT"
    if (is_input == 0):
        direction = "OUTPUT"
    f.write("    - {} + NET {} + DIRECTION {} + USE SIGNAL\n".format(
        name,
        name,
        direction))
    f.write("      + PORT\n")
    if (is_horisontal):
        f.write("        + LAYER met3 ( {} {} ) ( {} {} )\n".format(
            (0 - pin_half_width),
            (0 - pin_half_height),
            pin_half_width,
            pin_half_height))
    else:
        f.write("        + LAYER met3 ( {} {} ) ( {} {} )\n".format(
            (0 - pin_half_height),
            (0 - pin_half_width),
            pin_half_height,
            pin_half_width))
    f.write("        + PLACED ( {} {} ) N ;\n".format(
        x, y))

def gen_pins():
    pins_count = 1 + 1 + 15 + 1 + 32 + 1 + 1 + 32 + 15 + 15 + 15 + 1 + 15 + 1 + 1 + 1 + 2
    f.write("PINS {} ;\n".format(pins_count))
    left_x = 0 + pin_half_width
    right_x = die_size_x - pin_half_width
    top_y = die_size_y - pin_half_width
    bottom_y = pin_half_width
    pin_x_offset = 2000							#
    pin_y_offset = pdn_step_y_half
    # top
    write_pin("i_clk", 144000, top_y, 0, 1)
    write_pin("i_reset_n", 140000, top_y, 0, 1)
    # left
    y = 10000								#
    write_pin("i_ack", left_x, y, 1, 1)
    y += pin_y_offset
    for idx in range(0,32):
        write_pin("i_instruction[{}]".format(idx), left_x, y + (idx * pdn_step_y_half), 1, 1)
    y = 95000								#
    for idx in range(1,16):
        write_pin("o_addr[{}]".format(idx), left_x, y + (idx * pin_y_offset), 1, 0)
    y += 16 * pin_y_offset
    write_pin("o_cyc", left_x, y, 1, 0)
    # bottom
    x = 10000								#
    write_pin("i_ebreak", x, bottom_y, 0, 1)
    x += pin_x_offset
    for idx in range(1,16):
        write_pin("i_pc_trap[{}]".format(idx), x + (idx * pin_x_offset), bottom_y, 0, 1)
    x = 105000								#
    write_pin("i_stall", x, bottom_y, 0, 1)
    x += pin_x_offset
    write_pin("i_pc_select", x, bottom_y, 0, 1)
    x += pin_x_offset
    for idx in range(1,16):
        write_pin("i_pc_target[{}]".format(idx), x + (idx * pin_x_offset), bottom_y, 0, 1)
    # right
    y = 10000
    for idx in range(0,32):
        write_pin("o_instruction[{}]".format(idx), right_x, y + (idx * pin_y_offset), 1, 0)
    y += 32 * pin_y_offset
    write_pin("o_ready", right_x, y, 1, 0)
    y = 65000								#
    for idx in range(1,16):
        write_pin("o_pc[{}]".format(idx), right_x, y + (idx * pin_y_offset), 1, 0)
    y += 16 * pin_y_offset
    for idx in range(1,16):
        write_pin("o_pc_next[{}]".format(idx), right_x, y + (idx * pin_y_offset), 1, 0)
    y += 16 * pin_y_offset
    write_pin("o_pc_change", right_x, y, 1, 0)
    f.write("END PINS\n")

#f = open("io_.def", "w")
#f.write("VERSION 5.8 ;\n")
#f.write("DIVIDERCHAR \"/\" ;\n")
#f.write("BUSBITCHARS \"[]\" ;\n")
#f.write("DESIGN rv_fetch ;\n")
#f.write("UNITS DISTANCE MICRONS 1000 ;\n")
#f.write("DIEAREA ( 0 0 ) ( {} {} ) ;\n".format(
#    die_size_x,
#    die_size_y))
#gen_rows()
#gen_tracks()
#gen_pins()
#f.write("END DESIGN\n")
#f.close()

class PIN:
    def __init__(self, name, x0, y0, position, is_horisontal, is_input):
        global io
        self.name = name
        offset = -1
        if (isinstance(position, str)):
            part = position.split()
            offset = int(part[1])
        if (is_horisontal):
            if (offset == -1):
                self.x = position
            else:
                self.x = x0 + (offset * io.step_x)
            self.y = y0
        else:
            self.x = x0
            if (offset == -1):
                self.y = position
            else:
                self.y = y0 + (offset * io.step_y)
        self.w = 0
        self.h = 0
        self.is_horisontal = is_horisontal
        self.is_input = is_input

    def save(self, f):
        if (self.is_input):
            direction = "INPUT"
        else:
            direction = "OUTPUT"
        f.write("    - {} + NET {} + DIRECTION {} + USE SIGNAL\n".format(
            self.name,
            self.name,
            direction))
        f.write("      + PORT\n")
        if (self.is_horisontal):
            f.write("        + LAYER met3 ( 0 0 ) ( {} {} )\n".format(io.pin_height, io.pin_width))
        else:
            f.write("        + LAYER met3 ( 0 0 ) ( {} {} )\n".format(io.pin_width, io.pin_height))
        f.write("        + PLACED ( {} {} ) N ;\n".format(self.x, self.y))

class IO:
    def init(self, path):
        f = open(path + "/config.json", "r")
        config = json.load(f)
        f.close()
        self.name = config["DESIGN_NAME"]
        area = config["DIE_AREA"]
        sizes = area.split()
        self.width = int(sizes[2]) * 1000
        self.height = int(sizes[3]) * 1000
        f = open(path + "/io.json", "r")
        self.pins_src = json.load(f)
        self.step_x = self.pins_src["step_x"]
        self.step_y = self.pins_src["step_y"]
        self.pin_width = self.pins_src["pin_width"]
        self.pin_height = self.pins_src["pin_height"]
        self.pin_half_width = int(self.pin_width / 2)
        self.pin_half_height = int(self.pin_height / 2)
        f.close()
        #self.f_order = open("pins.cfg", "w")
        #self.f_order.write("#BUS_SORT\n")
        self.pins = []
        self.parse_pins("top")
        self.parse_pins("left")
        self.parse_pins("right")
        self.parse_pins("bottom")
        #self.f_order.close()

    def parse_pins(self, cat_name):
        if (cat_name in self.pins_src):
            cat = self.pins_src[cat_name]
            if (cat_name == "top"):
                is_horisontal = True
                #self.f_order.write("\n#N\n")
                x0 = -1
                y0 = self.height - self.pin_width
            elif (cat_name == "bottom"):
                is_horisontal = True
                #self.f_order.write("\n#S\n")
                x0 = -1
                y0 = 0
            elif (cat_name == "left"):
                is_horisontal = False
                #self.f_order.write("\n#W\n")
                x0 = 0
                y0 = -1
            elif (cat_name == "right"):
                is_horisontal = False
                #self.f_order.write("\n#E\n")
                x0 = self.width - self.pin_width
                y0 = -1
            for info in cat:
                name = info["name"]
                position = info["position"]
                is_input = info["is_input"]
                if (info["type"] == "single"):
                    #self.f_order.write("{}\n".format(name))
                    pin = PIN(name, x0, y0, position, is_horisontal, is_input)
                    self.pins.append(pin)
                    x0 = pin.x
                    y0 = pin.y
                else:
                    range_start = int(info["start"])
                    range_end = int(info["end"]) + 1
                    for i in range(range_start,range_end):
                        p_name = name.format(i)
                        #self.f_order.write(name.format(i) + "\n")
                        pin = PIN(p_name, x0, y0, position, is_horisontal, is_input)
                        self.pins.append(pin)
                        x0 = pin.x
                        y0 = pin.y
                        position = "rel 1"

    def save(self, path):
        f = open(path + "/io.def", "w")
        f.write("VERSION 5.8 ;\n")
        f.write("DIVIDERCHAR \"/\" ;\n")
        f.write("BUSBITCHARS \"[]\" ;\n")
        f.write("DESIGN {} ;\n".format(self.name))
        f.write("UNITS DISTANCE MICRONS 1000 ;\n")
        f.write("DIEAREA ( 0 0 ) ( {} {} ) ;\n".format(self.width, self.height))
        f.write("PINS {} ;\n".format(len(self.pins)))
        for pin in self.pins:
            pin.save(f)
        f.write("END PINS\n")
        f.write("END DESIGN\n")
        f.close()

if (len(sys.argv) != 2):
    print("Invalid parameters!")
    exit(-1)
path = sys.argv[1]
io = IO()
io.init(path)
io.save(path)
