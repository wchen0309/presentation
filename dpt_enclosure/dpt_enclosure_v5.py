import cadquery as cq
from pathlib import Path

OUT=Path('/mnt/data')

# Premium desktop DPT enclosure V5
# Mechanical architecture only. PCB geometry intentionally omitted.
# - fixed lower inductor-switching bay, drawer-like front but non-sliding
# - partition plate above lower bay for DC-link/main electronics stack
# - entire upper safety hood hinges open for assembly/service
# - two independent top access hatches for normal DUT/socket/probe work
# - right side swing probe support rail

W,D = 430.0,390.0
LOWER_H=78.0
HOOD_Z0=78.0
HOOD_H=205.0
TOP_Z=HOOD_Z0+HOOD_H
WALL=4.0
R=24.0

# ---------- helpers ----------
def rp(w,d,h,r,z=0,x=0,y=0):
    s=cq.Workplane('XY').box(w,d,h,centered=(True,True,False)).translate((x,y,z))
    try:
        s=s.edges('|Z').fillet(min(r,w/2-0.5,d/2-0.5))
        s=s.edges('#Z').fillet(2.2)
    except Exception:
        pass
    return s

def box_xyz(w,d,h,x,y,z):
    return cq.Workplane('XY').box(w,d,h,centered=(True,True,False)).translate((x,y,z))

def cylz(d,h,x,y,z):
    return cq.Workplane('XY',origin=(x,y,z)).circle(d/2).extrude(h)

def cylx(d,length,x,y,z):
    return cq.Workplane('YZ',origin=(x,y,z)).circle(d/2).extrude(length)

def valid(o):
    vals=o.vals() if hasattr(o,'vals') else [o]
    return vals and all(v.isValid() for v in vals)

# ---------- lower plinth / inductor bay ----------
base_outer=rp(W,D,LOWER_H,R)
base_inner=rp(W-2*WALL,D-2*WALL,LOWER_H+6,R-WALL,6)
base_shell=base_outer.cut(base_inner)

# Fixed front service panel, visually drawer-like but screw/quarter-turn retained.
front_panel=rp(W-34,10,54,10,12,0,-D/2+1)
front_recess=rp(W-72,13,32,6,23,0,-D/2-4)
front_panel=front_panel.cut(front_recess)
front_insert=rp(W-82,5,26,5,26,0,-D/2-5.2)
vent_band=rp(190,4,8,4,16,0,-D/2-7)
fastL=cylz(12,5,-W/2+42,-D/2-7,36)
fastR=cylz(12,5, W/2-42,-D/2-7,36)

# Bottom board reservation rails, not board geometry.
inductor_tray=rp(W-66,D-74,4,8,14)
tray_rail_L=rp(12,D-86,12,3,16,-W/2+44,0)
tray_rail_R=rp(12,D-86,12,3,16, W/2-44,0)

# Structural separator plate between lower bay and upper electronics.
partition=rp(W-22,D-22,5,11,LOWER_H-2)
upper_mount=rp(W-58,D-58,5,9,HOOD_Z0+14)
mount_rail_L=rp(14,D-94,16,3,HOOD_Z0+16,-W/2+45,0)
mount_rail_R=rp(14,D-94,16,3,HOOD_Z0+16, W/2-45,0)
rear_panel=rp(W-76,7,46,7,18,0,D/2-1)

# ---------- one-piece upper hood ----------
hoodW,hoodD=W-14,D-14
hood_outer=rp(hoodW,hoodD,HOOD_H,22,HOOD_Z0)
hood_inner=rp(hoodW-18,hoodD-18,HOOD_H+10,16,HOOD_Z0+5)
hood=hood_outer.cut(hood_inner)

# Large smoked front window. Cut volume straddles front wall.
front_cut=box_xyz(W-64,34,128,0,-D/2+8,HOOD_Z0+34)
hood=hood.cut(front_cut)
front_glass=box_xyz(W-78,4,114,0,-D/2-1.2,HOOD_Z0+41)
front_bezel_outer=box_xyz(W-56,7,138,0,-D/2-3,HOOD_Z0+29)
front_bezel_inner=box_xyz(W-80,12,116,0,-D/2-6,HOOD_Z0+40)
front_bezel=front_bezel_outer.cut(front_bezel_inner)

# Right-side window leaves room for probe-rack mounting spine.
side_cut=box_xyz(34,D-128,106,W/2-8,6,HOOD_Z0+46)
hood=hood.cut(side_cut)
side_glass=box_xyz(4,D-142,92,W/2+0.7,6,HOOD_Z0+53)
side_bezel_outer=box_xyz(7,D-118,116,W/2+1.5,6,HOOD_Z0+41)
side_bezel_inner=box_xyz(12,D-144,94,W/2-3,6,HOOD_Z0+52)
side_bezel=side_bezel_outer.cut(side_bezel_inner)

# top deck integrated with hood, two openings
TOP_MX=19.0; TOP_MY=21.0; GAP=8.0
open_w=(W-2*TOP_MX-GAP)/2
open_d=D-2*TOP_MY
lx=-(GAP/2+open_w/2); rx=-lx
top_deck=rp(W-18,D-18,13,18,TOP_Z-13)
openL=rp(open_w-10,open_d-10,24,12,TOP_Z-18,lx,0)
openR=rp(open_w-10,open_d-10,24,12,TOP_Z-18,rx,0)
top_deck=top_deck.cut(openL).cut(openR)

# independent daily hatches
LID_T=10; FRAME=16

def lid(xc):
    outer=rp(open_w,open_d,LID_T,14,TOP_Z-1,xc,0)
    inner=rp(open_w-2*FRAME,open_d-2*FRAME,LID_T+8,9,TOP_Z+1,xc,0)
    frame=outer.cut(inner)
    pane=rp(open_w-2*FRAME-7,open_d-2*FRAME-7,4,8,TOP_Z+1.6,xc,0)
    handle=rp(72,18,8,5,TOP_Z+5.5,xc,-open_d/2+31)
    return frame,pane,handle

lf,lp,lh=lid(lx); rf,rpne,rh=lid(rx)

# Hinges: rear axis along X
hood_hinge_y=D/2-19; hood_hinge_z=HOOD_Z0+6
hood_hinge=cylx(16,W-80,-(W-80)/2,hood_hinge_y,hood_hinge_z)
lid_hinge_y=D/2-TOP_MY-3; lid_hinge_z=TOP_Z+2
lhbar=cylx(10,open_w-48,lx-(open_w-48)/2,lid_hinge_y,lid_hinge_z)
rhbar=cylx(10,open_w-48,rx-(open_w-48)/2,lid_hinge_y,lid_hinge_z)

# front hood latches to base, subtle and functional
latchL=rp(20,11,28,4,HOOD_Z0-1,-W/2+54,-D/2+7)
latchR=rp(20,11,28,4,HOOD_Z0-1, W/2-54,-D/2+7)

# rotation helpers
H1=(-W,hood_hinge_y,hood_hinge_z); H2=(W,hood_hinge_y,hood_hinge_z)
LL1=(lx-open_w, lid_hinge_y,lid_hinge_z); LL2=(lx+open_w,lid_hinge_y,lid_hinge_z)
RR1=(rx-open_w, lid_hinge_y,lid_hinge_z); RR2=(rx+open_w,lid_hinge_y,lid_hinge_z)

def rhood(o,deg=66): return o.rotate(H1,H2,-deg)
def rlid(o,side,deg=72): return o.rotate(*( (LL1,LL2,-deg) if side=='L' else (RR1,RR2,-deg) ))

# daily access state, both hatches open
lf_o,lp_o,lh_o,lhbar_o=[rlid(o,'L') for o in (lf,lp,lh,lhbar)]
rf_o,rp_o,rh_o,rhbar_o=[rlid(o,'R') for o in (rf,rpne,rh,rhbar)]

# full service state, complete hood opens as one unit, hatches remain closed with hood
service_group=[hood,front_glass,front_bezel,side_glass,side_bezel,top_deck,lf,lp,lh,rf,rpne,rh,hood_hinge,lhbar,rhbar,latchL,latchR]
service_group=[rhood(o) for o in service_group]

# ---------- probe support rail on right side ----------
# Base-mounted, can swing/stow; keeps heavy probes off DUT/socket.
probe_mount=rp(28,72,28,7,HOOD_Z0+28,W/2+9,-34)
probe_mast=cylz(14,174,W/2+24,-34,HOOD_Z0+35)
probe_pivot=cylz(24,18,W/2+24,-34,HOOD_Z0+202)
probe_arm=cylx(12,174,W/2+24-174,-34,HOOD_Z0+211)
probe_clamps=[rp(22,28,18,4,HOOD_Z0+202,W/2+24-x,-34) for x in (48,96,144)]
probe_stow=rp(22,36,66,5,HOOD_Z0+76,W/2+10,D/2-74)

# visual waist line, makes lower bay read as a separate service module
waist=rp(W-16,7,14,4,LOWER_H-5,0,-D/2+1)
status=rp(84,3,4,2,33,72,-D/2-7)
footL=rp(122,42,10,12,-5,-W/2+82,0)
footR=rp(122,42,10,12,-5, W/2-82,0)

# ---------- colors / assembly ----------
C={
 'body':cq.Color(.91,.92,.93), 'panel':cq.Color(.66,.68,.70), 'dark':cq.Color(.035,.04,.045),
 'glass':cq.Color(.06,.12,.17,.54), 'metal':cq.Color(.24,.26,.28), 'blue':cq.Color(.04,.48,.98),
 'shelf':cq.Color(.34,.36,.38)
}

for n,o in {'base':base_shell,'panel':front_panel,'partition':partition,'hood':hood,'frontglass':front_glass,
            'frontbezel':front_bezel,'sideglass':side_glass,'sidebezel':side_bezel,'deck':top_deck,
            'lf':lf,'rf':rf,'probe_arm':probe_arm}.items():
    if not valid(o): raise RuntimeError('invalid solid '+n)

BASE_PARTS=[
 (base_shell,'Lower_Bay_Shell','body'),(front_panel,'Lower_Bay_Fixed_Front','panel'),(front_insert,'Lower_Bay_Recess','dark'),
 (vent_band,'Lower_Bay_Vent','dark'),(fastL,'QuarterTurn_Left','metal'),(fastR,'QuarterTurn_Right','metal'),
 (inductor_tray,'Inductor_Board_Reserve_Tray','shelf'),(tray_rail_L,'Inductor_Rail_L','metal'),(tray_rail_R,'Inductor_Rail_R','metal'),
 (partition,'Structural_Partition','shelf'),(upper_mount,'Upper_Electronics_Mount','shelf'),(mount_rail_L,'Upper_Mount_Rail_L','metal'),(mount_rail_R,'Upper_Mount_Rail_R','metal'),
 (rear_panel,'Rear_Service_Panel','panel'),(waist,'Waist_Reveal','dark'),(status,'Status_Bar','blue'),(footL,'Foot_Runner_L','dark'),(footR,'Foot_Runner_R','dark'),
 (probe_mount,'Probe_Rack_Mount','metal'),(probe_mast,'Probe_Rack_Mast','metal'),(probe_pivot,'Probe_Rack_Pivot','dark'),
 (probe_arm,'Probe_Rack_Arm','metal'),(probe_stow,'Probe_Rack_Stow','dark')]

HOOD_CLOSED=[
 (hood,'Main_Service_Hood','body'),(front_glass,'Front_Smoked_Window','glass'),(front_bezel,'Front_Window_Bezel','dark'),
 (side_glass,'Right_Side_Window','glass'),(side_bezel,'Right_Side_Bezel','dark'),(top_deck,'Top_Access_Deck','body'),
 (lf,'Daily_Lid_Left_Frame','body'),(lp,'Daily_Lid_Left_Glass','glass'),(lh,'Daily_Lid_Left_Handle','dark'),
 (rf,'Daily_Lid_Right_Frame','body'),(rpne,'Daily_Lid_Right_Glass','glass'),(rh,'Daily_Lid_Right_Handle','dark'),
 (hood_hinge,'Main_Hood_Hinge','metal'),(lhbar,'Left_Lid_Hinge','metal'),(rhbar,'Right_Lid_Hinge','metal'),
 (latchL,'Hood_Latch_Left','dark'),(latchR,'Hood_Latch_Right','dark')]

HOOD_DAILY=[
 (hood,'Main_Service_Hood','body'),(front_glass,'Front_Smoked_Window','glass'),(front_bezel,'Front_Window_Bezel','dark'),
 (side_glass,'Right_Side_Window','glass'),(side_bezel,'Right_Side_Bezel','dark'),(top_deck,'Top_Access_Deck','body'),
 (lf_o,'Daily_Lid_Left_Frame','body'),(lp_o,'Daily_Lid_Left_Glass','glass'),(lh_o,'Daily_Lid_Left_Handle','dark'),
 (rf_o,'Daily_Lid_Right_Frame','body'),(rp_o,'Daily_Lid_Right_Glass','glass'),(rh_o,'Daily_Lid_Right_Handle','dark'),
 (hood_hinge,'Main_Hood_Hinge','metal'),(lhbar_o,'Left_Lid_Hinge','metal'),(rhbar_o,'Right_Lid_Hinge','metal'),
 (latchL,'Hood_Latch_Left','dark'),(latchR,'Hood_Latch_Right','dark')]

SERVICE_NAMES=[
 ('Main_Service_Hood','body'),('Front_Smoked_Window','glass'),('Front_Window_Bezel','dark'),('Right_Side_Window','glass'),
 ('Right_Side_Bezel','dark'),('Top_Access_Deck','body'),('Daily_Lid_Left_Frame','body'),('Daily_Lid_Left_Glass','glass'),
 ('Daily_Lid_Left_Handle','dark'),('Daily_Lid_Right_Frame','body'),('Daily_Lid_Right_Glass','glass'),('Daily_Lid_Right_Handle','dark'),
 ('Main_Hood_Hinge','metal'),('Left_Lid_Hinge','metal'),('Right_Lid_Hinge','metal'),('Hood_Latch_Left','dark'),('Hood_Latch_Right','dark')]

def build(name,hood_parts):
    a=cq.Assembly(name=name)
    for o,n,c in BASE_PARTS: a.add(o,name=n,color=C[c])
    for i,p in enumerate(probe_clamps): a.add(p,name=f'Probe_Clamp_{i+1}',color=C['dark'])
    for o,n,c in hood_parts: a.add(o,name=n,color=C[c])
    return a

closed=build('DPT_Enclosure_V5_Closed',HOOD_CLOSED)
daily=build('DPT_Enclosure_V5_Daily_Access',HOOD_DAILY)
service=build('DPT_Enclosure_V5_Full_Service',[(o,n,c) for o,(n,c) in zip(service_group,SERVICE_NAMES)])

for a,n in [(closed,'Closed'),(daily,'Daily_Access'),(service,'Full_Service')]:
    a.save(str(OUT/f'DPT_Enclosure_V5_{n}.step'))
    a.save(str(OUT/f'DPT_Enclosure_V5_{n}.glb'))

STATE_PARTS={
 'Closed':BASE_PARTS+[(p,f'Probe_Clamp_{i+1}','dark') for i,p in enumerate(probe_clamps)]+HOOD_CLOSED,
 'Daily_Access':BASE_PARTS+[(p,f'Probe_Clamp_{i+1}','dark') for i,p in enumerate(probe_clamps)]+HOOD_DAILY,
 'Full_Service':BASE_PARTS+[(p,f'Probe_Clamp_{i+1}','dark') for i,p in enumerate(probe_clamps)]+[(o,n,c) for o,(n,c) in zip(service_group,SERVICE_NAMES)]
}
print('V5 exported')
