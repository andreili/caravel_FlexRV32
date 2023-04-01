#!/bin/python
import json, sys;

class PIN:
    def __init__(self, name, x0, y0, position, step, is_horisontal, is_input):
        self.name = name
        offset = -1
        if (isinstance(position, str)):
            part = position.split()
            offset = int(part[1])
        if (is_horisontal):
            if (offset == -1):
                self.x = position
            else:
                self.x = x0 + (offset * step)
            self.y = y0
        else:
            self.x = x0
            if (offset == -1):
                self.y = position
            else:
                self.y = y0 + (offset * step)
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
        self.steps = self.pins_src["steps"]
        self.pin_width = self.pins_src["pin_width"]
        self.pin_height = self.pins_src["pin_height"]
        #self.pin_half_width = int(self.pin_width / 2)
        #self.pin_half_height = int(self.pin_height / 2)
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
                step = self.steps[2]
            elif (cat_name == "bottom"):
                is_horisontal = True
                #self.f_order.write("\n#S\n")
                x0 = -1
                y0 = 0
                step = self.steps[3]
            elif (cat_name == "left"):
                is_horisontal = False
                #self.f_order.write("\n#W\n")
                x0 = 0
                y0 = -1
                step = self.steps[0]
            elif (cat_name == "right"):
                is_horisontal = False
                #self.f_order.write("\n#E\n")
                x0 = self.width - self.pin_width
                y0 = -1
                step = self.steps[1]
            for info in cat:
                name = info["name"]
                position = info["position"]
                is_input = info["is_input"]
                if (info["type"] == "single"):
                    #self.f_order.write("{}\n".format(name))
                    pin = PIN(name, x0, y0, position, step, is_horisontal, is_input)
                    self.pins.append(pin)
                    x0 = pin.x
                    y0 = pin.y
                else:
                    range_start = int(info["start"])
                    range_end = int(info["end"]) + 1
                    for i in range(range_start,range_end):
                        p_name = name.format(i)
                        #self.f_order.write(name.format(i) + "\n")
                        pin = PIN(p_name, x0, y0, position, step, is_horisontal, is_input)
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
