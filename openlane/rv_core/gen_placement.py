#!/bin/python
import json

dist_regs_to_fetch_y = 10.0
dist_regs_to_alu1_x = 10.0
dist_decode_to_fetch_x = 10.0
dist_x_to_regs = 10.0
dist_y_to_regs = 10.0
offset_alu1_y = 20.0

def load_js(fn):
    f = open(fn, "r")
    js = json.load(f)
    f.close()
    return js

def get_corners(fn):
    js = load_js(fn)
    area = js["DIE_AREA"]
    strs = area.split()
    ints = [ int(strs[2]), int(strs[3]) ]
    return ints

corners_fetch = get_corners("../rv_fetch/config.json")
corners_decode = get_corners("../rv_decode/config.json")
corners_alu1 = get_corners("../rv_alu1/config.json")
corners_alu2 = get_corners("../rv_alu2/config.json")
corners_write = get_corners("../rv_write/config.json")
corners_regs = get_corners("../rv_regs/config.json")

#pos_regs = [ dist_x_to_regs, dist_y_to_regs, "u_regs" ]
#pos_alu1 = [
#    (pos_regs[0] + corners_regs[0] + dist_regs_to_alu1_x),
#    (pos_regs[1] + offset_alu1_y),
#    "u_st3_alu1"
#    ]
#pos_decode = [
#    (pos_regs[0] + corners_regs[0] - corners_decode[0]),
#    (pos_regs[1] + corners_regs[1] + dist_regs_to_fetch_y),
#    "u_st2_decode"
#    ]
#pos_fetch = [
#    (pos_decode[0] - corners_fetch[0] - dist_decode_to_fetch_x),
#    (pos_decode[1]),
#    "u_st1_fetch"
#    ]

pos_alu2 = [
    (10.0),
    (10.0),
    "u_st4_alu2",
    "N"
    ]
pos_write = [
    (pos_alu2[0]),
    (pos_alu2[1] + corners_alu2[1] + 10.0),
    "u_st5_write",
    "N"
    ]
pos_alu1 = [
    (pos_write[0] + corners_write[0] + 10.0),
    (pos_write[1]),
    "u_st3_alu1",
    "R90"
    ]
pos_regs = [
    (pos_write[0]),
    (pos_write[1] + corners_write[1] + 10.0),
    "u_regs",
    "N"
    ]
pos_decode = [
    (pos_regs[0] + corners_regs[0] + 10.0),
    (pos_regs[1]),
    "u_st2_decode",
    "N"
    ]
pos_fetch = [
    (pos_decode[0]),
    (pos_decode[1] + corners_decode[1] + 10.0),
    "u_st1_fetch",
    "N"
    ]

positions = [
    pos_regs,
    pos_alu1,
    pos_alu2,
    pos_write,
    pos_decode,
    pos_fetch
    ]
f = open("placement.cfg", "w")
for pos in positions:
    f.write("{} {} {} {}\n".format(
        pos[2],
        round(pos[0], 3),
        round(pos[1], 3),
        pos[3]
        ))
f.close()
