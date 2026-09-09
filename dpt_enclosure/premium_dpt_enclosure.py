# Derived in spirit from CadQuery/cadquery-contrib Parametric_Enclosure.py (MIT)
# Original copyright (c) 2018 Dave Cowden.
# This redesign is a new premium benchtop DPT enclosure concept.

import cadquery as cq
from pathlib import Path

OUT = Path('.')
W, D, BASE_H = 430.0, 390.0, 188.0
WALL, BOTTOM, R = 3.5, 6.0, 24.0
POST_D, POST_H = 24.0, 300.0
POST_X, POST_Y = W/2-11.0, D/2-11.0
LEFT_COVER_X0, LEFT_COVER_X1 = -W/2+25, -44.0
CH_X0, CH_X1 = -24.0, W/2-30.0
CH_Y0, CH_Y1 = -D/2+24.0, D/2-24.0
CH_H, TOP_Z = 76.0, BASE_H
LID_Z = BASE_H + CH_H

def rounded_prism(w,d,h,r=10.0,z0=0.0,x0=0.0,y0=0.0):
    s=cq.Workplane('XY').box(w,d,h,centered=(True,True,False)).translate((x0,y0,z0))
    if r>0:
        try: s=s.edges('|Z').fillet(min(r,w/2-0.1,d/2-0.1))
        except Exception: pass
    return s

def front_plate_poly(points_xz,thickness,y_front):
    return cq.Workplane('XZ',origin=(0,y_front,0)).polyline(points_xz).close().extrude(thickness)

def solid_ok(obj):
    vals=obj.vals() if hasattr(obj,'vals') else [obj]
    return len(vals)>0 and all(v.isValid() for v in vals)

outer=rounded_prism(W,D,BASE_H,R,0)
inner=rounded_prism(W-2*WALL,D-2*WALL,BASE_H+12,R-WALL,BOTTOM)
base_shell=outer.cut(inner)
waist=rounded_prism(W-18,6,52,2,105,0,-D/2-1.8)
front_fascia=rounded_prism(W-54,5,88,8,14,0,-D/2-3)
vent=rounded_prism(W-105,7,12,5,5,0,-D/2-6)
win_pts=[(-178,112),(-178,173),(-58,173),(-35,145),(-52,112)]
window=front_plate_poly(win_pts,5,-D/2-6.2)
border_pts=[(-186,106),(-186,181),(-52,181),(-25,146),(-47,106)]
window_border=front_plate_poly(border_pts,6,-D/2-7).cut(window)
right_bezel_pts=[(-18,106),(25,181),(178,181),(186,106)]
right_bezel=front_plate_poly(right_bezel_pts,5,-D/2-6.5)
right_open_pts=[(-3,116),(35,169),(164,169),(172,116)]
right_open=front_plate_poly(right_open_pts,7,-D/2-7.5)
right_bezel=right_bezel.cut(right_open)

left_span=LEFT_COVER_X1-LEFT_COVER_X0
hood_profile=[(CH_Y0,TOP_Z),(CH_Y0,TOP_Z+32),(-72,TOP_Z+62),(CH_Y1-24,TOP_Z+72),(CH_Y1,TOP_Z+58),(CH_Y1,TOP_Z)]
left_hood=cq.Workplane('YZ',origin=(LEFT_COVER_X0,0,0)).polyline(hood_profile).close().extrude(left_span)
try: left_hood=left_hood.edges('|X').fillet(9)
except Exception: pass
hood_reveal=(cq.Workplane('YZ',origin=(LEFT_COVER_X0+2,0,0)).polyline([(CH_Y0+5,TOP_Z+1),(CH_Y0+5,TOP_Z+8),(CH_Y1-5,TOP_Z+8),(CH_Y1-5,TOP_Z+1)]).close().extrude(left_span-4))

ch_w,ch_d=CH_X1-CH_X0,CH_Y1-CH_Y0
ch_x,ch_y=(CH_X0+CH_X1)/2,(CH_Y0+CH_Y1)/2
ch_outer=rounded_prism(ch_w,ch_d,CH_H,18,TOP_Z,ch_x,ch_y)
ch_inner=rounded_prism(ch_w-22,ch_d-22,CH_H+8,11,TOP_Z+7,ch_x,ch_y)
ch_ring=ch_outer.cut(ch_inner)
front_cut=rounded_prism(ch_w-42,95,CH_H+18,8,TOP_Z+4,ch_x,CH_Y0+32)
ch_ring=ch_ring.cut(front_cut)
liner_outer=rounded_prism(ch_w-12,ch_d-12,CH_H-10,14,TOP_Z+6,ch_x,ch_y)
liner_inner=rounded_prism(ch_w-28,ch_d-28,CH_H+4,9,TOP_Z+11,ch_x,ch_y)
ch_inner_liner=liner_outer.cut(liner_inner).cut(front_cut)

lid_w,lid_d=ch_w+8,ch_d+6
lid_x,lid_y=ch_x,ch_y+2
lid_outer=rounded_prism(lid_w,lid_d,16,18,LID_Z,lid_x,lid_y)
lid_cut=rounded_prism(lid_w-30,lid_d-34,22,12,LID_Z+4,lid_x,lid_y-2)
lid_frame_closed=lid_outer.cut(lid_cut)
lid_glass_closed=rounded_prism(lid_w-38,lid_d-42,5,10,LID_Z+5,lid_x,lid_y-2)
handle_closed=rounded_prism(82,20,10,5,LID_Z+12,lid_x,CH_Y0+44)
hinge_y,hinge_z=CH_Y1-2,LID_Z+4
axis_p1,axis_p2=(-W,hinge_y,hinge_z),(W,hinge_y,hinge_z)
def rot(obj,deg): return obj.rotate(axis_p1,axis_p2,deg)
lid_frame_open=rot(lid_frame_closed,-68)
lid_glass_open=rot(lid_glass_closed,-68)
handle_open=rot(handle_closed,-68)

posts=[]; feet=[]; caps=[]
for x in (-POST_X,POST_X):
    for y in (-POST_Y,POST_Y):
        p=cq.Workplane('XY').center(x,y).circle(POST_D/2).extrude(POST_H)
        p=p.cut(cq.Workplane('XY').center(x,y).circle((POST_D-5)/2).extrude(POST_H+2))
        posts.append(p)
        feet.append(cq.Workplane('XY').center(x,y).circle(POST_D/2+3).extrude(8))
        caps.append(cq.Workplane('XY').center(x,y).circle(POST_D/2+1).extrude(6).translate((0,0,POST_H)))

service_panel=rounded_prism(5,170,92,3,42,W/2+1.5,38)
status_bar=rounded_prism(96,3,4,1.5,54,64,-D/2-7.3)
COL={'white':cq.Color(.91,.92,.93),'metal':cq.Color(.72,.74,.76),'black':cq.Color(.035,.04,.045),'glass':cq.Color(.08,.12,.16,.62),'blue':cq.Color(.05,.48,.93),'darkmetal':cq.Color(.17,.18,.20)}

def build(open_lid=False):
    a=cq.Assembly(name='DPT_Premium_Enclosure')
    for obj,name,color in [(base_shell,'Main_Chassis_Shell','white'),(waist,'Black_Waist_Band','black'),(front_fascia,'Front_Fascia','metal'),(vent,'Front_Vent','black'),(window_border,'Front_Window_Bezel','black'),(window,'Front_Window','glass'),(right_bezel,'Test_Chamber_Front_Bezel','black'),(left_hood,'Fixed_Left_Hood','white'),(hood_reveal,'Hood_Reveal','black'),(ch_ring,'Test_Chamber_Rim','white'),(ch_inner_liner,'Test_Chamber_Inner_Liner','black'),(service_panel,'Side_Service_Panel','metal'),(status_bar,'Status_Light','blue')]:
        a.add(obj,name=name,color=COL[color])
    for i,p in enumerate(posts): a.add(p,name=f'Corner_Post_{i+1}',color=COL['metal'])
    for i,p in enumerate(feet): a.add(p,name=f'Foot_{i+1}',color=COL['black'])
    for i,p in enumerate(caps): a.add(p,name=f'Post_Cap_{i+1}',color=COL['black'])
    if open_lid:
        a.add(lid_frame_open,name='Top_Lid_Frame',color=COL['white']); a.add(lid_glass_open,name='Top_Lid_Glass',color=COL['glass']); a.add(handle_open,name='Top_Lid_Handle',color=COL['darkmetal'])
    else:
        a.add(lid_frame_closed,name='Top_Lid_Frame',color=COL['white']); a.add(lid_glass_closed,name='Top_Lid_Glass',color=COL['glass']); a.add(handle_closed,name='Top_Lid_Handle',color=COL['darkmetal'])
    return a

for n,o in {'base':base_shell,'hood':left_hood,'chamber_rim':ch_ring,'liner':ch_inner_liner,'lid':lid_frame_closed}.items():
    assert solid_ok(o), f'invalid solid: {n}'

closed,opened=build(False),build(True)
closed.save(str(OUT/'DPT_Premium_Enclosure_Closed.step'),mode='default')
opened.save(str(OUT/'DPT_Premium_Enclosure_Open.step'),mode='default')
closed.save(str(OUT/'DPT_Premium_Enclosure_Closed.glb'))
opened.save(str(OUT/'DPT_Premium_Enclosure_Open.glb'))
print('exported')
