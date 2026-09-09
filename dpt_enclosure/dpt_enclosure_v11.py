import cadquery as cq
from pathlib import Path

OUT = Path("/mnt/data")

# ============================================================
# DPT Premium Enclosure V11 - installation-detail design
# Pure mechanical enclosure / no PCB models.
#
# Design frozen at this stage:
# 1) Upper shroud: rear hook + 2 front quarter-turn compression latches
#    + perimeter gasket + tapered locating pins.
# 2) Lower inductor module: short male/female guide rails + 4 hard load pads
#    + 2 front captive locking pins.
# 3) Service drawer: side-mounted heavy-duty slide envelopes sized around
#    76.2 mm height / 19.1 mm side space class.
# 4) Drawer power connection: 3 blind-mate single-pole busbar channels
#    (BUS+ / BUSN / BUS-) at the rear backplane, feeding a fixed 3-way
#    vertical riser cassette through the separator. No loose power cable
#    moves with the drawer.
# 5) Daily test lid: 6 mm smoked PC, hidden touch latch cavity,
#    spring-pop plungers, rear torque-hinge envelope, lid-closed interlock pocket.
# 6) External fasteners hidden: front/side skins are fastened from inside;
#    bottom service screws only on underside / rear.
# ============================================================

W, D = 430.0, 390.0
IND_H = 102.0
UP_BASE_H = 46.0
UP_BASE_Z = IND_H
SHROUD_Z0 = IND_H + UP_BASE_H
SHROUD_H = 188.0
TOP_Z = SHROUD_Z0 + SHROUD_H

INDIGO = (28/255, 31/255, 136/255)  # #1C1F88

def rp(w,d,h,r,z=0,x=0,y=0):
    s = cq.Workplane("XY").box(w,d,h,centered=(True,True,False)).translate((x,y,z))
    try:
        s = s.edges("|Z").fillet(min(r,w/2-0.6,d/2-0.6))
        s = s.edges("#Z").fillet(min(2.0,max(0.5,h/2-0.2)))
    except Exception:
        pass
    return s

def bx(w,d,h,x=0,y=0,z=0):
    return cq.Workplane("XY").box(w,d,h,centered=(True,True,False)).translate((x,y,z))

def cylz(d,h,x=0,y=0,z=0):
    return cq.Workplane("XY",origin=(x,y,z)).circle(d/2).extrude(h)

def cyly(d,length,x=0,y=0,z=0):
    return cq.Workplane("XZ",origin=(x,y,z)).circle(d/2).extrude(length)

def cylx(d,length,x=0,y=0,z=0):
    return cq.Workplane("YZ",origin=(x,y,z)).circle(d/2).extrude(length)

def ring_rect(w,d,wall,h,z,x=0,y=0,r=8):
    o = rp(w,d,h,r,z,x,y)
    i = rp(w-2*wall,d-2*wall,h+2,max(2,r-wall),z-1,x,y)
    return o.cut(i)

def valid(o):
    vals=o.vals() if hasattr(o,"vals") else [o]
    return bool(vals) and all(v.isValid() for v in vals)

COL = {
    "light": cq.Color(0.92,0.93,0.94),
    "warm": cq.Color(0.87,0.88,0.89),
    "graphite": cq.Color(0.07,0.08,0.095),
    "darkmetal": cq.Color(0.22,0.24,0.27),
    "metal": cq.Color(0.57,0.59,0.62),
    "glass": cq.Color(0.10,0.15,0.20,0.42),
    "indigo": cq.Color(*INDIGO),
    "black": cq.Color(0.02,0.025,0.03),
    "insulator": cq.Color(0.14,0.15,0.16),
    "copper": cq.Color(0.72,0.35,0.12),
    "gasket": cq.Color(0.05,0.05,0.055),
}

# ============================================================
# LOWER INDUCTOR MODULE
# ============================================================
LOW_W, LOW_D = W-18, D-18
lower_outer = rp(LOW_W,LOW_D,IND_H,20,0)
lower_inner = rp(LOW_W-14,LOW_D-14,IND_H-10,14,7)
lower_box = lower_outer.cut(lower_inner)

front_open = rp(W-68,16,70,10,16,0,-D/2+2)
lower_box = lower_box.cut(front_open)
lower_front = rp(W-48,12,68,10,13,0,-D/2+4)
lower_front = lower_front.cut(rp(124,10,24,8,34,0,-D/2-2))
drawer_pull = rp(110,4,13,6,39,0,-D/2-5)

lower_top = rp(W-28,D-28,8,12,IND_H-8)

PAD_X = W/2-54
PAD_Y = D/2-54
load_pads = []
for i,(x,y) in enumerate([(-PAD_X,-PAD_Y),(PAD_X,-PAD_Y),(-PAD_X,PAD_Y),(PAD_X,PAD_Y)]):
    load_pads.append((rp(30,30,5,4,IND_H-1,x,y),f"Lower_Module_Load_Pad_{i+1}","metal"))

RAIL_X = W/2-66
rail_body_L = rp(15,D-106,8,2,IND_H-2,-RAIL_X,8)
rail_body_R = rp(15,D-106,8,2,IND_H-2, RAIL_X,8)
rail_head_L = rp(26,D-120,4,2,IND_H+5,-RAIL_X,8)
rail_head_R = rp(26,D-120,4,2,IND_H+5, RAIL_X,8)

lower_lock_keep_L = cylz(14,12,-W/2+56,-D/2+28,IND_H-5)
lower_lock_keep_R = cylz(14,12, W/2-56,-D/2+28,IND_H-5)

# ============================================================
# SERVICE DRAWER AND REAL SLIDE ENVELOPE
# ============================================================
SLIDE_H = 76.2
SLIDE_T = 19.1
SLIDE_LEN = 304.8

DRAW_W = W - 2*(38 + SLIDE_T)
DRAW_D = 300.0
DRAW_H = 72.0
drawer_body = rp(DRAW_W,DRAW_D,DRAW_H,9,15,0,-4)
drawer_front = rp(W-52,12,68,10,13,0,-D/2+4)
drawer_front = drawer_front.cut(rp(124,10,24,8,34,0,-D/2-2))
drawer_pull2 = rp(110,4,13,6,39,0,-D/2-5)

slide_y = -3.0
slide_x = W/2 - 38 - SLIDE_T/2
slide_L = rp(SLIDE_T,SLIDE_LEN,SLIDE_H,2,13,-slide_x,slide_y)
slide_R = rp(SLIDE_T,SLIDE_LEN,SLIDE_H,2,13, slide_x,slide_y)
inner_slide_L = rp(8,SLIDE_LEN-12,SLIDE_H-8,2,17,-slide_x+5,slide_y)
inner_slide_R = rp(8,SLIDE_LEN-12,SLIDE_H-8,2,17, slide_x-5,slide_y)

lock_lever_L = bx(8,28,16,-slide_x+4,-D/2+34,24)
lock_lever_R = bx(8,28,16, slide_x-4,-D/2+34,24)

# ============================================================
# REAR DRAWER BACKPLANE: BUS+, BUSN, BUS-
# ============================================================
BUS_X = (-65.0,0.0,65.0)
BUS_NAMES = ("BUS_PLUS","BUS_N","BUS_MINUS")
BACKPLANE_Y = D/2 - 40.0
BACKPLANE_Z = 17.0

backplane = bx(238,10,78,0,BACKPLANE_Y,BACKPLANE_Z)

bus_wells=[]
bus_sockets=[]
bus_blades=[]
bus_barriers=[]
for i,(x,name) in enumerate(zip(BUS_X,BUS_NAMES)):
    well = rp(48,42,48,6,31,x,BACKPLANE_Y-24)
    bus_wells.append((well,f"{name}_Insulated_Well","insulator"))
    socket = rp(38,30,34,5,38,x,BACKPLANE_Y-36)
    bus_sockets.append((socket,f"{name}_BlindMate_Socket_Envelope","black"))
    blade = bx(24,3,32,x,BACKPLANE_Y-57,39)
    bus_blades.append((blade,f"{name}_Drawer_Blade_3mm","copper"))
for j,x in enumerate((-32.5,32.5), start=1):
    bus_barriers.append((bx(4,56,58,x,BACKPLANE_Y-27,27),f"BUS_Insulation_Barrier_{j}","insulator"))

cassette_outer = rp(230,68,22,8,IND_H-11,0,BACKPLANE_Y-18)
cassette_inner = rp(218,56,24,5,IND_H-9,0,BACKPLANE_Y-18)
bus_cassette = cassette_outer.cut(cassette_inner)

feedthrough_rings=[]
power_risers=[]
for x,name in zip(BUS_X,BUS_NAMES):
    ring = cylz(36,18,x,BACKPLANE_Y-18,IND_H-9).cut(cylz(27,20,x,BACKPLANE_Y-18,IND_H-10))
    feedthrough_rings.append((ring,f"{name}_Feedthrough_Grommet","insulator"))
    riser = bx(24,9,48,x,BACKPLANE_Y-18,IND_H-5)
    power_risers.append((riser,f"{name}_Fixed_Power_Riser","insulator"))

# ============================================================
# UPPER TEST BASE
# ============================================================
upper_outer = rp(W,D,UP_BASE_H,22,UP_BASE_Z)
upper_inner = rp(W-16,D-16,UP_BASE_H+8,16,UP_BASE_Z+7)
upper_base_shell = upper_outer.cut(upper_inner)

install_deck = rp(W-30,D-34,7,13,SHROUD_Z0-9)
bus_cut = rp(242,76,18,8,SHROUD_Z0-15,0,BACKPLANE_Y-18)
install_deck = install_deck.cut(bus_cut)
bus_upper_insert = ring_rect(240,74,7,8,SHROUD_Z0-10,0,BACKPLANE_Y-18,8)

upper_feed_rings=[]
for x,name in zip(BUS_X,BUS_NAMES):
    r = cylz(36,16,x,BACKPLANE_Y-18,SHROUD_Z0-12).cut(cylz(27,18,x,BACKPLANE_Y-18,SHROUD_Z0-13))
    upper_feed_rings.append((r,f"{name}_Upper_Gland_Insert","insulator"))

gallery_outer = rp(238,36,102,8,SHROUD_Z0-3,0,D/2-30)
gallery_inner = rp(224,24,90,5,SHROUD_Z0+4,0,D/2-31)
power_gallery = gallery_outer.cut(gallery_inner)
gallery_cover = rp(226,5,88,5,SHROUD_Z0+5,0,D/2-48)
gallery_div1 = bx(4,24,88,-32.5,D/2-30,SHROUD_Z0+5)
gallery_div2 = bx(4,24,88, 32.5,D/2-30,SHROUD_Z0+5)

waist_front = rp(W-26,15,30,9,UP_BASE_Z+8,0,-D/2+1)
waist_L = rp(14,D-54,30,6,UP_BASE_Z+8,-W/2+3,0)
waist_R = rp(14,D-54,30,6,UP_BASE_Z+8, W/2-3,0)
waist_shadow = rp(W-38,4,6,2,UP_BASE_Z+5,0,-D/2-5)

receiver_L = rp(34,D-92,18,4,UP_BASE_Z-4,-RAIL_X,8).cut(rp(28,D-78,13,3,UP_BASE_Z-2,-RAIL_X,8))
receiver_R = rp(34,D-92,18,4,UP_BASE_Z-4, RAIL_X,8).cut(rp(28,D-78,13,3,UP_BASE_Z-2, RAIL_X,8))
rear_stop_L = rp(40,18,20,4,UP_BASE_Z-4,-RAIL_X,D/2-42)
rear_stop_R = rp(40,18,20,4,UP_BASE_Z-4, RAIL_X,D/2-42)

upper_pads=[]
for i,(x,y) in enumerate([(-PAD_X,-PAD_Y),(PAD_X,-PAD_Y),(-PAD_X,PAD_Y),(PAD_X,PAD_Y)]):
    upper_pads.append((rp(32,32,4,4,UP_BASE_Z-3,x,y),f"Upper_Load_Pad_{i+1}","darkmetal"))

front_module_lock_L = cyly(16,24,-W/2+56,-D/2+30,UP_BASE_Z+17)
front_module_lock_R = cyly(16,24, W/2-56,-D/2+30,UP_BASE_Z+17)
module_interlock_pocket = rp(32,22,18,4,UP_BASE_Z+5,RAIL_X,D/2-60)

# ============================================================
# UPPER SHROUD
# ============================================================
hood_outer = rp(W-14,D-14,SHROUD_H,22,SHROUD_Z0)
hood_inner = rp(W-32,D-32,SHROUD_H-8,16,SHROUD_Z0-8)
shroud = hood_outer.cut(hood_inner)

front_skirt = rp(W-20,12,20,7,SHROUD_Z0-18,0,-D/2+3)
side_skirt_L = rp(12,D-42,20,5,SHROUD_Z0-18,-W/2+6,0)
side_skirt_R = rp(12,D-42,20,5,SHROUD_Z0-18, W/2-6,0)

gasket_outer = rp(W-34,D-34,4,14,SHROUD_Z0-4)
gasket_inner = rp(W-46,D-46,6,10,SHROUD_Z0-5)
gasket_ring = gasket_outer.cut(gasket_inner)

shroud_rear_hook_L = bx(28,12,28,-W/2+48,D/2-32,SHROUD_Z0-14)
shroud_rear_hook_R = bx(28,12,28, W/2-48,D/2-32,SHROUD_Z0-14)
base_rear_keeper_L = rp(34,16,14,4,SHROUD_Z0-11,-W/2+48,D/2-33)
base_rear_keeper_R = rp(34,16,14,4,SHROUD_Z0-11, W/2-48,D/2-33)

loc_pin_L = cylz(14,18,-W/2+42,-D/2+42,SHROUD_Z0-6).union(cylz(8,7,-W/2+42,-D/2+42,SHROUD_Z0+12))
loc_pin_R = cylz(14,18, W/2-42,-D/2+42,SHROUD_Z0-6).union(cylz(8,7, W/2-42,-D/2+42,SHROUD_Z0+12))

LATCH_Z = SHROUD_Z0-7
e9_head_L = cyly(28,4,-W/2+138,-D/2+11,LATCH_Z)
e9_head_R = cyly(28,4, W/2-138,-D/2+11,LATCH_Z)
e9_body_L = cyly(20,38,-W/2+138,-D/2+49,LATCH_Z)
e9_body_R = cyly(20,38, W/2-138,-D/2+49,LATCH_Z)
e9_cam_L = bx(36,4,8,-W/2+138,-D/2+54,LATCH_Z-4)
e9_cam_R = bx(36,4,8, W/2-138,-D/2+54,LATCH_Z-4)

front_cut = bx(W-56,34,122,0,-D/2+8,SHROUD_Z0+32)
shroud = shroud.cut(front_cut)
front_bezel = bx(W-44,8,136,0,-D/2-2,SHROUD_Z0+25).cut(bx(W-72,14,110,0,-D/2-6,SHROUD_Z0+38))
front_glass = bx(W-74,4,108,0,-D/2-1.2,SHROUD_Z0+39)
window_clamp_top = bx(W-86,6,8,0,-D/2+8,SHROUD_Z0+143)
window_clamp_bot = bx(W-86,6,8,0,-D/2+8,SHROUD_Z0+30)

probe_cut = bx(42,150,72,W/2-8,-12,SHROUD_Z0+94)
shroud = shroud.cut(probe_cut)
probe_bezel = bx(7,168,88,W/2+1.5,-12,SHROUD_Z0+86).cut(bx(12,146,68,W/2-3,-12,SHROUD_Z0+96))

top_deck = rp(W-18,D-18,13,18,TOP_Z-13)
access_w=252.0
access_d=D-44.0
access_x=63.0
access_open = rp(access_w-10,access_d-10,24,12,TOP_Z-18,access_x,0)
top_deck = top_deck.cut(access_open)

left_edge=-W/2+22
access_left=access_x-access_w/2
fixed_x=(left_edge+access_left)/2
fixed_w=access_left-left_edge
fixed_roof = rp(max(fixed_w+20,118),D-50,22,18,TOP_Z-3,fixed_x-3,0).union(rp(max(fixed_w+42,142),164,13,16,TOP_Z-3,fixed_x+8,-88))
roof_reveal=rp(max(fixed_w-8,88),D-82,4,11,TOP_Z+2,fixed_x-3,8)

left_grip = bx(4,98,16,-W/2+1.5,54,SHROUD_Z0+36)
right_grip = bx(4,64,16,W/2-1.5,80,SHROUD_Z0+36)

# ============================================================
# DAILY TEST LID
# ============================================================
lid_frame_outer = rp(access_w,access_d,10,14,TOP_Z-1,access_x,0)
lid_frame_inner = rp(access_w-30,access_d-30,18,9,TOP_Z+1,access_x,0)
lid_frame = lid_frame_outer.cut(lid_frame_inner)
lid_pc = rp(access_w-38,access_d-38,6,8,TOP_Z+1.2,access_x,0)

E4_W,E4_D,E4_H = 34.0,24.0,18.0
touch_latch_pocket = rp(E4_W,E4_D,E4_H,4,TOP_Z-17,access_x,-access_d/2+27)
touch_keeper = bx(18,5,10,access_x,-access_d/2+22,TOP_Z-2)

pop_L = cylz(10,12,access_x-access_w/2+34,-access_d/2+30,TOP_Z-11)
pop_R = cylz(10,12,access_x+access_w/2-34,-access_d/2+30,TOP_Z-11)

hinge_y=D/2-25
hinge_z=TOP_Z+2
hinge_L=cyly(16,36,access_x-access_w/2+30,hinge_y-18,hinge_z)
hinge_R=cyly(16,36,access_x+access_w/2-30,hinge_y-18,hinge_z)
lid_interlock = rp(30,18,16,4,TOP_Z-14,access_x+84,hinge_y-22)

# ============================================================
# RIGHT FOLD-AWAY PROBE SHELF
# ============================================================
SHELF_W,SHELF_D,SHELF_T=112.0,156.0,6.0
HX=W/2+5.0
HZ=SHROUD_Z0+84.0
SY=-12.0
shelf = rp(SHELF_W,SHELF_D,SHELF_T,7,HZ-3,HX+SHELF_W/2,SY)
shelf_lip = rp(8,SHELF_D-16,18,3,HZ+1,HX+SHELF_W-7,SY)
shelf_skin = rp(SHELF_W-6,SHELF_D-6,3,6,HZ-5,HX+SHELF_W/2,SY)
shelf_hinge_F=cyly(12,26,HX,SY-SHELF_D/2+6,HZ)
shelf_hinge_R=cyly(12,26,HX,SY+SHELF_D/2-32,HZ)

SHELF_AXIS1=(HX,-D,HZ)
SHELF_AXIS2=(HX,D,HZ)
LID_AXIS1=(access_x-access_w,D/2-25,TOP_Z+2)
LID_AXIS2=(access_x+access_w,D/2-25,TOP_Z+2)

def rotate_parts(parts,axis1,axis2,deg):
    out=[]
    for o,n,c in parts:
        out.append((o.rotate(axis1,axis2,deg),n,c))
    return out

lower_module_parts = [
    (lower_box,"Lower_Inductor_Module_Box","warm"),
    (lower_front,"Lower_Inductor_Module_Front","warm"),
    (drawer_pull,"Lower_Front_Recess","graphite"),
    (lower_top,"Lower_Module_Top_Interface","metal"),
    (rail_body_L,"Lower_Module_Male_Rail_L","darkmetal"),
    (rail_body_R,"Lower_Module_Male_Rail_R","darkmetal"),
    (rail_head_L,"Lower_Module_Rail_Head_L","graphite"),
    (rail_head_R,"Lower_Module_Rail_Head_R","graphite"),
    (lower_lock_keep_L,"Lower_Module_Lock_Keeper_L","graphite"),
    (lower_lock_keep_R,"Lower_Module_Lock_Keeper_R","graphite"),
    (slide_L,"Drawer_Fixed_Slide_Envelope_L","darkmetal"),
    (slide_R,"Drawer_Fixed_Slide_Envelope_R","darkmetal"),
    (backplane,"Drawer_Power_Backplane","metal"),
    (bus_cassette,"BUS_Feedthrough_Cassette","graphite"),
] + load_pads + bus_wells + bus_sockets + bus_barriers + feedthrough_rings + power_risers

drawer_parts = [
    (drawer_body,"Inductor_Service_Drawer","darkmetal"),
    (drawer_front,"Inductor_Drawer_Front","warm"),
    (drawer_pull2,"Drawer_Concealed_Pull","graphite"),
    (inner_slide_L,"Drawer_Moving_Slide_L","graphite"),
    (inner_slide_R,"Drawer_Moving_Slide_R","graphite"),
    (lock_lever_L,"Drawer_Slide_Lock_Lever_L","black"),
    (lock_lever_R,"Drawer_Slide_Lock_Lever_R","black"),
] + bus_blades

upper_base_parts = [
    (upper_base_shell,"Upper_Test_Base","warm"),
    (install_deck,"Installation_Deck","metal"),
    (bus_upper_insert,"Upper_BUS_Cassette_Insert","graphite"),
    (power_gallery,"Rear_Power_Gallery","graphite"),
    (gallery_cover,"Rear_Power_Gallery_Cover","darkmetal"),
    (gallery_div1,"Rear_Gallery_Divider_1","black"),
    (gallery_div2,"Rear_Gallery_Divider_2","black"),
    (waist_front,"Indigo_Waist_Front","indigo"),
    (waist_L,"Indigo_Waist_Left","indigo"),
    (waist_R,"Indigo_Waist_Right","indigo"),
    (waist_shadow,"Waist_Shadow","graphite"),
    (receiver_L,"Lower_Module_Receiver_Rail_L","darkmetal"),
    (receiver_R,"Lower_Module_Receiver_Rail_R","darkmetal"),
    (rear_stop_L,"Lower_Module_Rear_Stop_L","graphite"),
    (rear_stop_R,"Lower_Module_Rear_Stop_R","graphite"),
    (front_module_lock_L,"Lower_Module_Captive_Lock_L","graphite"),
    (front_module_lock_R,"Lower_Module_Captive_Lock_R","graphite"),
    (module_interlock_pocket,"Lower_Module_Seated_Interlock_Pocket","black"),
    (base_rear_keeper_L,"Shroud_Rear_Keeper_L","graphite"),
    (base_rear_keeper_R,"Shroud_Rear_Keeper_R","graphite"),
    (loc_pin_L,"Shroud_Locating_Pin_L","metal"),
    (loc_pin_R,"Shroud_Locating_Pin_R","metal"),
] + upper_pads + upper_feed_rings

shroud_parts = [
    (shroud,"One_Piece_Upper_Shroud","light"),
    (front_skirt,"Shroud_Front_Overlap_Skirt","light"),
    (side_skirt_L,"Shroud_Side_Skirt_L","light"),
    (side_skirt_R,"Shroud_Side_Skirt_R","light"),
    (gasket_ring,"Shroud_Perimeter_Gasket","gasket"),
    (shroud_rear_hook_L,"Shroud_Rear_Hook_L","graphite"),
    (shroud_rear_hook_R,"Shroud_Rear_Hook_R","graphite"),
    (e9_head_L,"Shroud_E9_Latch_Head_L","graphite"),
    (e9_head_R,"Shroud_E9_Latch_Head_R","graphite"),
    (e9_body_L,"Shroud_E9_Latch_Body_L","darkmetal"),
    (e9_body_R,"Shroud_E9_Latch_Body_R","darkmetal"),
    (e9_cam_L,"Shroud_E9_Cam_L","darkmetal"),
    (e9_cam_R,"Shroud_E9_Cam_R","darkmetal"),
    (front_bezel,"Front_Window_Bezel","graphite"),
    (front_glass,"Front_Transparent_Window","glass"),
    (window_clamp_top,"Window_Internal_Clamp_Top","darkmetal"),
    (window_clamp_bot,"Window_Internal_Clamp_Bottom","darkmetal"),
    (probe_bezel,"Right_Probe_Portal_Bezel","graphite"),
    (top_deck,"Top_Deck","light"),
    (fixed_roof,"Left_Fixed_Streamlined_Roof","light"),
    (roof_reveal,"Left_Roof_Reveal","graphite"),
    (left_grip,"Left_Concealed_Grip","graphite"),
    (right_grip,"Right_Concealed_Grip","graphite"),
]

lid_parts = [
    (lid_frame,"Daily_Lid_Aluminum_Frame","light"),
    (lid_pc,"Daily_Lid_6mm_Smoked_PC","glass"),
    (touch_keeper,"Daily_Lid_E4_Keeper","graphite"),
]
lid_fixed_parts = [
    (touch_latch_pocket,"Daily_Lid_E4_Latch_Cavity","graphite"),
    (pop_L,"Daily_Lid_Pop_Plunger_L","metal"),
    (pop_R,"Daily_Lid_Pop_Plunger_R","metal"),
    (hinge_L,"Daily_Lid_Torque_Hinge_L","darkmetal"),
    (hinge_R,"Daily_Lid_Torque_Hinge_R","darkmetal"),
    (lid_interlock,"Daily_Lid_Closed_Interlock_Pocket","black"),
]

shelf_parts = [
    (shelf,"Probe_Shelf","graphite"),
    (shelf_skin,"Probe_Shelf_Outer_Skin","warm"),
    (shelf_lip,"Probe_Shelf_Lip","graphite"),
    (shelf_hinge_F,"Probe_Shelf_Hinge_F","metal"),
    (shelf_hinge_R,"Probe_Shelf_Hinge_R","metal"),
]

def add_parts(a,parts,trans=(0,0,0)):
    for o,n,c in parts:
        obj=o.translate(trans) if trans!=(0,0,0) else o
        a.add(obj,name=n,color=COL[c])

def build(state="closed"):
    a=cq.Assembly(name=f"DPT_Enclosure_V11_{state}")
    add_parts(a,lower_module_parts)
    add_parts(a,upper_base_parts)
    add_parts(a,lid_fixed_parts)

    drawer_shift=(0,0,0)
    shroud_shift=(0,0,0)
    lid_state=lid_parts
    shelf_state=rotate_parts(shelf_parts,SHELF_AXIS1,SHELF_AXIS2,-90)

    if state=="drawer_open":
        drawer_shift=(0,-185,0)
    elif state=="shroud_removed":
        shroud_shift=(0,-50,110)
    elif state=="exploded":
        drawer_shift=(0,-185,0)
        shroud_shift=(0,-45,135)
    elif state=="daily":
        lid_state=rotate_parts(lid_parts,LID_AXIS1,LID_AXIS2,-72)
        shelf_state=shelf_parts

    add_parts(a,drawer_parts,drawer_shift)
    add_parts(a,shroud_parts,shroud_shift)
    add_parts(a,lid_state,shroud_shift)
    add_parts(a,shelf_state,shroud_shift)
    return a

def build_bus_detail():
    a=cq.Assembly(name="BUS_Drawer_Backplane_Detail")
    add_parts(a,[ (backplane,"Power_Backplane","metal"), (bus_cassette,"Feedthrough_Cassette","graphite") ] + bus_wells + bus_sockets + bus_barriers + feedthrough_rings + power_risers + bus_blades)
    return a

def build_lid_detail():
    a=cq.Assembly(name="Daily_Lid_Touch_Open_Detail")
    add_parts(a,lid_parts+lid_fixed_parts)
    return a

for nm,o in [
    ("lower_box",lower_box),("drawer_body",drawer_body),("upper_base_shell",upper_base_shell),
    ("install_deck",install_deck),("shroud",shroud),("gasket_ring",gasket_ring),
    ("front_glass",front_glass),("lid_frame",lid_frame),("lid_pc",lid_pc)
]:
    assert valid(o), f"invalid solid: {nm}"

for st in ["closed","daily","drawer_open","shroud_removed","exploded"]:
    build(st).save(str(OUT/f"DPT_Enclosure_V11_{st}.step"),mode="default")

build_bus_detail().save(str(OUT/"DPT_Enclosure_V11_BUS_Backplane_Detail.step"),mode="default")
build_lid_detail().save(str(OUT/"DPT_Enclosure_V11_Touch_Lid_Detail.step"),mode="default")

print("V11 exported")
