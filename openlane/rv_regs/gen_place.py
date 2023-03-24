#!/bin/python


y_grid_offset = 4

x_one = 4.150
y_one = 2.720
edff_step_x = 11.040 + 2.300
dff1_step_x = 7.360 + 1.910
dff2_step_x = 7.820 + 1.910
dff4_step_x = 8.740 + 1.910
# lower two rows - for input logic
btm_offset = 2

reg_offsets = [ 19.320, (y_one * y_grid_offset) ]
ori = "N"

def reg_get_ori(idx):
   return "N"
#   if ((idx % 2) == 0):
#        return "FS"
#   else:
#        return "N"

# main register file
y = reg_offsets[1] + (y_one * btm_offset)
for i in range(0,32):
    x = reg_offsets[0]
    for j in range(1,32):
        print("g_bit\[{0}\].g_word\[{1}\].r_bit.r_bit {2} {3} N".format(i, j, round(x,3), round(y,3)))
        x += edff_step_x
    y += (y_one * 2)

# read registers
y = reg_offsets[1] + (y_one * btm_offset)
x = reg_offsets[0] + (edff_step_x * 31)
for i in range(0,32):
    y1 = y + 0
    y2 = y + y_one
    print("g_bit\[{0}\].r_rs1.r_bit {1} {2} N ".format(i, round(x,3), round(y1,3)))
    print("g_bit\[{0}\].r_rs2.r_bit {1} {2} FS".format(i, round(x,3), round(y2,3)))
    y += (y_one * 2)
