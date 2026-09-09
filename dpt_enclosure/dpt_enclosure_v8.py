import cadquery as cq
from pathlib import Path

OUT = Path("/mnt/data")

# ============================================================
# DPT Premium Enclosure V8
# Industrial-design refinement:
# - fixed lower service drawer for inductor switching board
# - one-piece removable upper shroud, open-bottom
# - rear hooks + short locating rails + flush compression latches
# - single RIGHT daily-access transparent lid
# - touch-to-release lid with spring-pop concept + torque hinges
# - transparent front upper window
# - concealed side grip recesses
# - fold-away RIGHT probe shelf
# - hidden rear BUS+/BUSN/BUS- gallery
# - PANXIN logo palette used only as accent
# ============================================================

W, D = 430.0, 390.0
LOWER_H = 88.0
SHROUD_Z0 = LOWER_H
SHROUD_H = 198.0
TOP_Z = SHROUD_Z0 + SHROUD_H
WALL = 4.0
R = 24.0

PANXIN_CYAN = (3/255, 110/255, 184/255)
PANXIN_INDIGO = (28/255, 31/255, 136/255)

def rp(w, d, h, r, z=0, x=0, y=0):
    s = cq.Workplane("XY").box(w, d, h, centered=(True, True, False)).translate((x,y,z))
    try:
        s = s.edges("|Z").fillet(min(r, w/2-0.5, d/2-0.5))
        s = s.edges("#Z").fillet(min(2.2, max(0.6,h/2-0.2)))
    except Exception:
        pass
    return s

def bx(w,d,h,x=0,y=0,z=0):
    return cq.Workplane("XY").box(w,d,h,centered=(True,True,False)).translate((x,y,z))

def cylz(d,h,x=0,y=0,z=0):
    return cq.Workplane("XY", origin=(x,y,z)).circle(d/2).extrude(h)

def cyly(d,length,x=0,y=0,z=0):
    return cq.Workplane("XZ", origin=(x,y,z)).circle(d/2).extrude(length)

def valid(o):
    vals=o.vals() if hasattr(o,"vals") else [o]
    return bool(vals) and all(v.isValid() for v in vals)

COL = {
    "warmgray": cq.Color(0.88,0.89,0.90),
    "lightgray": cq.Color(0.93,0.94,0.945),
    "graphite": cq.Color(0.075,0.085,0.10),
    "darkmetal": cq.Color(0.22,0.24,0.27),
    "metal": cq.Color(0.55,0.58,0.61),
    "glass": cq.Color(0.12,0.17,0.22,0.47),
    "clear": cq.Color(0.18,0.22,0.27,0.28),
    "cyan": cq.Color(*PANXIN_CYAN),
    "indigo": cq.Color(*PANXIN_INDIGO),
    "black": cq.Color(0.025,0.03,0.035),
}

base_outer = rp(W, D, LOWER_H, R, 0)
base_inner = rp(W-2*WALL, D-2*WALL, LOWER_H+4, R-WALL, 6)
base_shell = base_outer.cut(base_inner)
waist_front = rp(W-22, 12, 28, 8, LOWER_H-27, 0, -D/2+1)
waist_side_L = bx(10, D-48, 28, -W/2+2, 0, LOWER_H-27)
waist_side_R = bx(10, D-48, 28,  W/2-2, 0, LOWER_H-27)
accent_cyan = rp(72, 3, 4, 2, LOWER_H-15, -48, -D/2-6)
accent_indigo = rp(72, 3, 4, 2, LOWER_H-15,  24, -D/2-6)

DRAW_W, DRAW_D, DRAW_H = W-54, D-74, 52.0
DRAW_Y_CLOSED = 4.0
drawer_body = rp(DRAW_W, DRAW_D, DRAW_H, 9, 13, 0, DRAW_Y_CLOSED)
drawer_front = rp(W-48, 12, 58, 10, 10, 0, -D/2+4)
pull_recess = rp(122, 9, 22, 8, 26, 0, -D/2-3)
drawer_front = drawer_front.cut(pull_recess)
pull_insert = rp(110, 4, 12, 6, 31, 0, -D/2-5)
slide_L = rp(14, D-100, 13, 3, 20, -W/2+42, 8)
slide_R = rp(14, D-100, 13, 3, 20,  W/2-42, 8)
drawer_rail_L = rp(8, D-112, 8, 2, 23, -W/2+52, 8)
drawer_rail_R = rp(8, D-112, 8, 2, 23,  W/2-52, 8)
drawer_latch_L = cylz(16, 7, -W/2+34, -D/2-4, 31)
drawer_latch_R = cylz(16, 7,  W/2-34, -D/2-4, 31)

partition = rp(W-22, D-22, 6, 11, LOWER_H-3)
BUS_X = (-62.0,0.0,62.0)
BUS_Y = D/2 - 42.0
for x in BUS_X:
    partition = partition.cut(cylz(28, 18, x, BUS_Y, LOWER_H-8))
bus_grommets=[]
for x in BUS_X:
    bus_grommets.append(cylz(38,8,x,BUS_Y,LOWER_H-4).cut(cylz(28,10,x,BUS_Y,LOWER_H-5)))

install_deck = rp(W-30,D-34,7,13,SHROUD_Z0+6)
mount_field = rp(W-74,D-92,4,10,SHROUD_Z0+14,0,-10)
rail_x=W/2-27
guide_L=rp(18,D-78,13,4,SHROUD_Z0+3,-rail_x,-4)
guide_R=rp(18,D-78,13,4,SHROUD_Z0+3, rail_x,-4)
key_L=rp(7,D-94,8,2,SHROUD_Z0+13,-rail_x,-4)
key_R=rp(7,D-94,8,2,SHROUD_Z0+13, rail_x,-4)
rear_hook_L = rp(34,18,24,4,SHROUD_Z0+4,-rail_x,D/2-40)
rear_hook_R = rp(34,18,24,4,SHROUD_Z0+4, rail_x,D/2-40)
rear_hook_cap_L = rp(42,10,10,3,SHROUD_Z0+24,-rail_x,D/2-42)
rear_hook_cap_R = rp(42,10,10,3,SHROUD_Z0+24, rail_x,D/2-42)
shroud_latch_L = cylz(18,7,-W/2+38,-D/2-5,LOWER_H-19)
shroud_latch_R = cylz(18,7, W/2-38,-D/2-5,LOWER_H-19)
latch_index_L = cylz(4,8,-W/2+38,-D/2-7,LOWER_H-16)
latch_index_R = cylz(4,8, W/2-38,-D/2-7,LOWER_H-16)

gallery_outer=rp(218,34,136,8,SHROUD_Z0+10,0,D/2-32)
gallery_inner=rp(204,22,124,5,SHROUD_Z0+16,0,D/2-33)
power_gallery=gallery_outer.cut(gallery_inner)
gallery_cover=rp(208,5,120,5,SHROUD_Z0+18,0,D/2-50)
lane_div1=bx(4,22,116,-36,D/2-32,SHROUD_Z0+20)
lane_div2=bx(4,22,116, 36,D/2-32,SHROUD_Z0+20)

hood_outer=rp(W-14,D-14,SHROUD_H,22,SHROUD_Z0)
hood_inner=rp(W-32,D-32,SHROUD_H-8,16,SHROUD_Z0-8)
shroud=hood_outer.cut(hood_inner)
front_cut=bx(W-56,34,128,0,-D/2+8,SHROUD_Z0+36)
shroud=shroud.cut(front_cut)
front_bezel=bx(W-44,8,142,0,-D/2-2,SHROUD_Z0+29).cut(bx(W-72,14,116,0,-D/2-6,SHROUD_Z0+42))
front_glass=bx(W-74,4,114,0,-D/2-1.2,SHROUD_Z0+43)

grip_y=52.0
grip_z=SHROUD_Z0+34
left_grip_cut=bx(24,118,26,-W/2+7,grip_y,grip_z)
right_grip_cut=bx(24,88,26,W/2-7,grip_y+26,grip_z)
shroud=shroud.cut(left_grip_cut).cut(right_grip_cut)
left_grip_inner=bx(4,104,16,-W/2+1.5,grip_y,grip_z+5)
right_grip_inner=bx(4,74,16,W/2-1.5,grip_y+26,grip_z+5)

probe_cut=bx(40,150,72,W/2-8,-12,SHROUD_Z0+104)
shroud=shroud.cut(probe_cut)
probe_bezel=bx(7,168,88,W/2+1.5,-12,SHROUD_Z0+96).cut(bx(12,146,68,W/2-3,-12,SHROUD_Z0+106))

top_deck=rp(W-18,D-18,13,18,TOP_Z-13)
access_w=252.0
access_d=D-44.0
access_x=63.0
access_open=rp(access_w-10,access_d-10,24,12,TOP_Z-18,access_x,0)
top_deck=top_deck.cut(access_open)
left_edge=-W/2+22
access_left=access_x-access_w/2
fixed_x=(left_edge+access_left)/2
fixed_w=access_left-left_edge
fixed_fairing=rp(max(fixed_w+20,118),D-50,22,18,TOP_Z-3,fixed_x-3,0).union(rp(max(fixed_w+42,142),164,13,16,TOP_Z-3,fixed_x+8,-88))
fair_reveal=rp(max(fixed_w-8,88),D-82,4,11,TOP_Z+2,fixed_x-3,8)

lid_outer=rp(access_w,access_d,10,14,TOP_Z-1,access_x,0)
lid_inner=rp(access_w-34,access_d-34,18,9,TOP_Z+1,access_x,0)
lid_frame=lid_outer.cut(lid_inner)
lid_glass=rp(access_w-41,access_d-41,4,8,TOP_Z+1.7,access_x,0)
press_zone=rp(46,5,4,2,TOP_Z+4,access_x,-access_d/2+18)
touch_latch_body=rp(34,22,18,5,TOP_Z-15,access_x,-access_d/2+24)
pop_plunger_L=cylz(10,10,access_x-access_w/2+31,-access_d/2+28,TOP_Z-10)
pop_plunger_R=cylz(10,10,access_x+access_w/2-31,-access_d/2+28,TOP_Z-10)
hinge_y=D/2-25
hinge_z=TOP_Z+2
hinge_L=cyly(14,36,access_x-access_w/2+28,hinge_y-18,hinge_z)
hinge_R=cyly(14,36,access_x+access_w/2-28,hinge_y-18,hinge_z)
axis1=(access_x-access_w,hinge_y,hinge_z)
axis2=(access_x+access_w,hinge_y,hinge_z)
def rlid(o,deg=72): return o.rotate(axis1,axis2,-deg)
lid_frame_open=rlid(lid_frame)
lid_glass_open=rlid(lid_glass)
press_zone_open=rlid(press_zone)

SHELF_W,SHELF_D,SHELF_T=112.0,156.0,6.0
HX=W/2+5.0
HZ=SHROUD_Z0+90
SY=-12.0
shelf=rp(SHELF_W,SHELF_D,SHELF_T,7,HZ-3,HX+SHELF_W/2,SY)
shelf_lip=rp(8,SHELF_D-16,18,3,HZ+1,HX+SHELF_W-7,SY)
shelf_skin=rp(SHELF_W-6,SHELF_D-6,3,6,HZ-5,HX+SHELF_W/2,SY)
S1=(HX,-D,HZ); S2=(HX,D,HZ)
def rshelf(o,deg=-90): return o.rotate(S1,S2,deg)
shelf_stowed=rshelf(shelf)
shelf_lip_stowed=rshelf(shelf_lip)
shelf_skin_stowed=rshelf(shelf_skin)
shelf_hinge_F=cyly(12,26,HX,SY-SHELF_D/2+6,HZ)
shelf_hinge_R=cyly(12,26,HX,SY+SHELF_D/2-32,HZ)

fixed_parts=[
    (base_shell,"Lower_Chassis","warmgray"),(waist_front,"Graphite_Waist_Front","graphite"),
    (waist_side_L,"Graphite_Waist_Left","graphite"),(waist_side_R,"Graphite_Waist_Right","graphite"),
    (accent_cyan,"PANXIN_Accent_Cyan","cyan"),(accent_indigo,"PANXIN_Accent_Indigo","indigo"),
    (partition,"Structural_Separator","metal"),(install_deck,"Installation_Deck","metal"),
    (mount_field,"PCB_Mounting_Field","darkmetal"),(guide_L,"Shroud_Guide_L","darkmetal"),
    (guide_R,"Shroud_Guide_R","darkmetal"),(key_L,"Shroud_Key_L","graphite"),(key_R,"Shroud_Key_R","graphite"),
    (rear_hook_L,"Shroud_Rear_Hook_L","graphite"),(rear_hook_R,"Shroud_Rear_Hook_R","graphite"),
    (rear_hook_cap_L,"Shroud_Rear_Hook_Cap_L","darkmetal"),(rear_hook_cap_R,"Shroud_Rear_Hook_Cap_R","darkmetal"),
    (power_gallery,"Rear_Power_Gallery","graphite"),(gallery_cover,"Rear_Power_Gallery_Cover","darkmetal"),
    (lane_div1,"BUS_Lane_Divider_1","black"),(lane_div2,"BUS_Lane_Divider_2","black"),
    (slide_L,"Drawer_Slide_L","darkmetal"),(slide_R,"Drawer_Slide_R","darkmetal"),
    (shroud_latch_L,"Shroud_Compression_Latch_L","graphite"),(shroud_latch_R,"Shroud_Compression_Latch_R","graphite"),
    (latch_index_L,"Latch_Index_L","cyan"),(latch_index_R,"Latch_Index_R","cyan")]
for i,g in enumerate(bus_grommets): fixed_parts.append((g,f"BUS_Grommet_{i+1}","black"))

drawer_parts=[(drawer_body,"Inductor_Service_Tray","darkmetal"),(drawer_front,"Inductor_Drawer_Front","warmgray"),
              (pull_insert,"Concealed_Spring_Pull","graphite"),(drawer_rail_L,"Drawer_Rail_L","graphite"),
              (drawer_rail_R,"Drawer_Rail_R","graphite"),(drawer_latch_L,"Drawer_Latch_L","graphite"),
              (drawer_latch_R,"Drawer_Latch_R","graphite")]

shroud_parts=[(shroud,"One_Piece_Removable_Shroud","lightgray"),(front_bezel,"Front_Window_Bezel","graphite"),
              (front_glass,"Front_Transparent_Window","glass"),(left_grip_inner,"Left_Concealed_Grip","graphite"),
              (right_grip_inner,"Right_Concealed_Grip","graphite"),(probe_bezel,"Right_Probe_Portal_Bezel","graphite"),
              (top_deck,"Top_Deck","lightgray"),(fixed_fairing,"Left_Fixed_Streamlined_Roof","lightgray"),
              (fair_reveal,"Left_Roof_Reveal","graphite")]

def add(a,parts,trans=(0,0,0)):
    for o,n,c in parts:
        obj=o.translate(trans) if trans!=(0,0,0) else o
        a.add(obj,name=n,color=COL[c])

def build(state):
    a=cq.Assembly(name=f"DPT_Enclosure_V8_{state}")
    add(a,fixed_parts)
    if state=="drawer": add(a,drawer_parts,(0,-146,0))
    else: add(a,drawer_parts)
    if state=="service":
        shift=(0,-62,46)
        add(a,shroud_parts,shift)
        for o,n,c in [(lid_frame,"Daily_Lid_Frame","lightgray"),(lid_glass,"Daily_Lid_Glass","glass"),
                      (press_zone,"Touch_Release_Press_Zone","cyan"),(hinge_L,"Torque_Hinge_L","darkmetal"),
                      (hinge_R,"Torque_Hinge_R","darkmetal"),(touch_latch_body,"Touch_Latch_Body","graphite"),
                      (pop_plunger_L,"Pop_Plunger_L","metal"),(pop_plunger_R,"Pop_Plunger_R","metal"),
                      (shelf_stowed,"Probe_Shelf_Stowed","graphite"),(shelf_skin_stowed,"Probe_Shelf_Skin","warmgray"),
                      (shelf_lip_stowed,"Probe_Shelf_Lip","graphite"),(shelf_hinge_F,"Probe_Shelf_Hinge_F","metal"),
                      (shelf_hinge_R,"Probe_Shelf_Hinge_R","metal")]:
            a.add(o.translate(shift),name=n,color=COL[c])
    else:
        add(a,shroud_parts)
        for o,n,c in [(touch_latch_body,"Touch_Latch_Body","graphite"),(pop_plunger_L,"Pop_Plunger_L","metal"),
                      (pop_plunger_R,"Pop_Plunger_R","metal"),(hinge_L,"Torque_Hinge_L","darkmetal"),
                      (hinge_R,"Torque_Hinge_R","darkmetal")]: a.add(o,name=n,color=COL[c])
        if state=="daily":
            for o,n,c in [(lid_frame_open,"Daily_Lid_Frame","lightgray"),(lid_glass_open,"Daily_Lid_Glass","glass"),
                          (press_zone_open,"Touch_Release_Press_Zone","cyan"),(shelf,"Probe_Shelf_Deployed","graphite"),
                          (shelf_skin,"Probe_Shelf_Skin","warmgray"),(shelf_lip,"Probe_Shelf_Lip","graphite"),
                          (shelf_hinge_F,"Probe_Shelf_Hinge_F","metal"),(shelf_hinge_R,"Probe_Shelf_Hinge_R","metal")]:
                a.add(o,name=n,color=COL[c])
        else:
            for o,n,c in [(lid_frame,"Daily_Lid_Frame","lightgray"),(lid_glass,"Daily_Lid_Glass","glass"),
                          (press_zone,"Touch_Release_Press_Zone","cyan"),(shelf_stowed,"Probe_Shelf_Stowed","graphite"),
                          (shelf_skin_stowed,"Probe_Shelf_Skin","warmgray"),(shelf_lip_stowed,"Probe_Shelf_Lip","graphite"),
                          (shelf_hinge_F,"Probe_Shelf_Hinge_F","metal"),(shelf_hinge_R,"Probe_Shelf_Hinge_R","metal")]:
                a.add(o,name=n,color=COL[c])
    return a

for name,o in [("base_shell",base_shell),("partition",partition),("shroud",shroud),("top_deck",top_deck),("lid_frame",lid_frame),("drawer_body",drawer_body)]:
    assert valid(o), f"invalid: {name}"

for state in ["closed","daily","drawer","service"]:
    a=build(state)
    a.save(str(OUT/f"DPT_Enclosure_V8_{state.capitalize()}.step"),mode="default")
    a.save(str(OUT/f"DPT_Enclosure_V8_{state.capitalize()}.glb"))

print("V8 exported")
