#!/usr/bin/env python3
"""Original animated cartoon story. No external artwork, API or secrets.

python3 tools/render_story.py manifest.json --output .local/story/silent.mp4
Manifest: {"scenes":[{"title":"...", "duration":9}, ... nine scenes]}.
FFMPEG selects encoder executable; DRIVELINE_FONT_DIR may select Arial fonts.
Use --preview-only for a contact sheet/poster without rendering the full movie.
"""
from pathlib import Path
import argparse, json, math, os, random, subprocess
from PIL import Image, ImageDraw, ImageFont
W,H=1280,720
PAPER='#FFF7E9'; NAVY='#203D48'; TEAL='#167E83'; MINT='#BFE1D5'; CORAL='#E88170'; GOLD='#E9B94F'; BLUE='#80ADC5'; LAV='#B7ABD0'; SKINS=['#B97954','#E4B18C','#875840','#F0C6A1']
FONTDIR=Path(os.environ.get('DRIVELINE_FONT_DIR','/System/Library/Fonts/Supplemental'))
FONT_CACHE={}
def font(size,bold=False):
 key=(size,bold)
 if key not in FONT_CACHE:
  candidates=[FONTDIR/('Arial Bold.ttf' if bold else 'Arial.ttf'),Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')]
  found=next((p for p in candidates if p.exists()),None)
  if found is None:raise RuntimeError('Install Arial or DejaVu fonts, or set DRIVELINE_FONT_DIR')
  FONT_CACHE[key]=ImageFont.truetype(str(found),size)
 return FONT_CACHE[key]
def ease(x):
 x=max(0,min(1,x));return x*x*(3-2*x)
def mix(a,b,t):return tuple(round(x+(y-x)*t) for x,y in zip(a,b))
def rgb(h):return tuple(bytes.fromhex(h.lstrip('#')))
class Art:
 def __init__(self,im):self.im=im;self.d=ImageDraw.Draw(im)
 def line(self,pts,fill=NAVY,width=4):self.d.line(pts,fill=fill,width=width,joint='curve')
 def oval(self,box,fill,outline=NAVY,width=3):self.d.ellipse(box,fill=fill,outline=outline,width=width)
 def rect(self,box,fill,r=15,outline=NAVY,width=3):self.d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width)
 def poly(self,pts,fill,outline=NAVY,width=3):self.d.polygon(pts,fill=fill);self.line(pts+[pts[0]],outline,width) if outline else None
 def text(self,xy,s,size=24,fill=NAVY,bold=False,anchor=None):self.d.text(xy,s,font=font(size,bold),fill=fill,anchor=anchor)
 def arc(self,box,start,end,fill=NAVY,width=3):self.d.arc(box,start,end,fill=fill,width=width)
 def check(self,x,y,scale=1,color=TEAL):self.line([(x-8*scale,y),(x-2*scale,y+6*scale),(x+12*scale,y-9*scale)],color,max(2,round(4*scale)))

def person(a,x,y,s=1,shirt=TEAL,skin=0,mood='happy',pose='stand',phase=0,hijab=False,glasses=False):
 """y is foot baseline; proportional joint motion keeps feet/expressions readable."""
 skin=SKINS[skin%len(SKINS)];bounce=math.sin(phase)*2*s if pose=='walk' else math.sin(phase*.6)*1.4*s
 y+=bounce
 def P(dx,dy):return(x+dx*s,y+dy*s)
 def B(x1,y1,x2,y2):return(*P(x1,y1),*P(x2,y2))
 a.oval(B(-29,-8,35,8),'#E5DFD0',None)
 step=math.sin(phase)*15 if pose=='walk' else 3
 a.line([P(-11,-59),P(-14-step,-29),P(-20-step,-3)],NAVY,max(3,int(9*s)))
 a.line([P(13,-59),P(16+step,-30),P(20+step,-3)],NAVY,max(3,int(9*s)))
 a.line([P(-20-step,-3),P(-7-step,-3)],NAVY,max(3,int(8*s)));a.line([P(20+step,-3),P(32+step,-3)],NAVY,max(3,int(8*s)))
 a.poly([P(-23,-122),P(22,-122),P(29,-58),P(-28,-58)],shirt,width=max(2,int(3*s)))
 a.rect(B(-8,-136,8,-116),skin,r=max(2,int(5*s)),width=max(2,int(2*s)))
 left=[P(-20,-115),P(-40,-91),P(-38,-67)];right=[P(20,-115),P(38,-94),P(41,-69)]
 if pose=='wave':right=[P(20,-115),P(43,-134),P(48+math.sin(phase)*5,-163)]
 if pose=='phone':right=[P(21,-113),P(38,-98),P(33,-121)]
 if pose=='umbrella':right=[P(20,-112),P(47,-122),P(53,-141)]
 if pose=='point':right=[P(20,-115),P(49,-118),P(76,-132)]
 if pose=='walk':left=[P(-20,-115),P(-33,-91),P(-37-step*.65,-75)];right=[P(20,-115),P(34,-93),P(35+step*.65,-75)]
 for arm in [left,right]:a.line(arm,NAVY,max(3,int(8*s)));a.oval((arm[-1][0]-5*s,arm[-1][1]-5*s,arm[-1][0]+5*s,arm[-1][1]+5*s),skin,width=max(1,int(2*s)))
 if hijab:a.oval(B(-31,-193,32,-127),shirt,width=max(2,int(3*s)));a.poly([P(-25,-166),P(-32,-119),P(34,-120),P(27,-166)],shirt,width=max(2,int(3*s)))
 else:a.oval(B(-26,-192,28,-139),NAVY)
 a.oval(B(-23,-181,24,-134),skin,width=max(2,int(3*s)))
 if not hijab:a.poly([P(-24,-170),P(-24,-183),P(-7,-195),P(17,-190),P(27,-174),P(7,-181),P(-3,-174)],NAVY,width=1)
 for dx in [-8,9]:a.oval(B(dx-2,-165,dx+2,-161),NAVY,None)
 if glasses:
  a.rect(B(-17,-169,-1,-158),None,r=4,width=max(1,int(2*s)));a.rect(B(3,-169,19,-158),None,r=4,width=max(1,int(2*s)));a.line([P(-1,-164),P(3,-164)],width=max(1,int(2*s)))
 if mood=='worried':a.arc(B(-8,-151,10,-138),190,350,width=max(1,int(2*s)));a.line([P(-15,-172),P(-5,-175)],width=max(1,int(2*s)));a.line([P(6,-175),P(16,-172)],width=max(1,int(2*s)))
 else:a.arc(B(-9,-156,10,-141),0,170,width=max(1,int(2*s)))
 if pose=='phone':a.rect(B(25,-140,43,-111),NAVY,r=3,width=1);a.rect(B(28,-137,40,-117),MINT,r=1,width=1)

def car(a,x,y,s=1,color=CORAL,phase=0,driver=True):
 def P(dx,dy):return(x+dx*s,y+dy*s)
 a.oval((*P(1,23),*P(203,39)),'#D9DED5',None)
 a.poly([P(10,-24),P(49,-34),P(75,-70),P(147,-70),P(178,-36),P(205,-24),P(211,16),P(5,16)],color,width=max(2,int(3*s)))
 a.poly([P(68,-37),P(85,-59),P(113,-59),P(113,-37)],'#E3F0EC',width=max(1,int(2*s)))
 a.poly([P(120,-59),P(140,-59),P(161,-37),P(120,-37)],'#E3F0EC',width=max(1,int(2*s)))
 if driver:a.oval((*P(133,-55),*P(146,-42)),SKINS[1],None)
 a.line([P(118,-32),P(118,11)],NAVY,max(1,int(2*s)));a.line([P(130,-22),P(143,-22)],NAVY,max(1,int(3*s)))
 for dx in [48,169]:
  a.oval((*P(dx-19,0),*P(dx+19,38)),NAVY);a.oval((*P(dx-10,9),*P(dx+10,29)),PAPER,None)
  q=phase*3;a.line([P(dx+8*math.cos(q),19+8*math.sin(q)),P(dx-8*math.cos(q),19-8*math.sin(q))],NAVY,max(1,int(2*s)))
 a.rect((*P(191,-18),*P(210,-7)),GOLD,r=3,width=1)

def exhaust(a,x,y,t,strength=1):
 # Light gray tailpipe wisps rise and disperse; illustrative, not measured emissions.
 for n in range(5):
  age=(t*.32+n*.2)%1;r=5+age*17
  color=mix(rgb('#A6ABA8'),rgb(PAPER),1-strength*(1-age)*.52)
  xx=x-age*62+math.sin(t+n)*4;yy=y-age*72
  a.arc((xx-r,yy-r*.55,xx+r,yy+r*.55),25,285,color,2)

def school(a,x,y,s=1,label='SCHOOL'):
 def P(dx,dy):return(x+dx*s,y+dy*s)
 a.poly([P(0,0),P(130,-45),P(260,0)],TEAL,width=3)
 a.rect((*P(13,0),*P(247,150)),'#E9D9BE',r=4)
 for xx in [33,83,161,211]:
  a.rect((*P(xx-14,29),*P(xx+14,66)),'#C9E3E7',r=4,width=2);a.line([P(xx,29),P(xx,66)],width=2)
 a.rect((*P(101,87),*P(159,150)),TEAL,r=7);a.line([P(130,89),P(130,149)],PAPER,2)
 a.text(P(130,8),label,max(13,round(19*s)),bold=True,anchor='mt')

def cloud(a,x,y,s=1,color='#D8E0DF'):
 for dx,dy,r in [(0,10,23),(27,-5,30),(57,9,24)]:a.oval((x+(dx-r)*s,y+(dy-r)*s,x+(dx+r)*s,y+(dy+r)*s),color,None)
 a.rect((x-20*s,y+8*s,x+76*s,y+31*s),color,r=10,outline=None)
def sun(a,x,y,t,s=1):
 for i in range(10):q=i*math.tau/10+t*.15;a.line([(x+31*s*math.cos(q),y+31*s*math.sin(q)),(x+43*s*math.cos(q),y+43*s*math.sin(q))],GOLD,4)
 a.oval((x-24*s,y-24*s,x+24*s,y+24*s),GOLD,NAVY,2)
def tree(a,x,y,s=1):
 a.line([(x,y),(x,y-115*s)],'#8F705A',max(3,int(12*s)));a.oval((x-45*s,y-170*s,x+42*s,y-95*s),MINT,TEAL,2);a.oval((x-66*s,y-140*s,x-6*s,y-78*s),MINT,TEAL,2)
def clock(a,x,y,t,r=36):
 a.oval((x-r,y-r,x+r,y+r),PAPER);a.line([(x,y),(x+15*math.sin(t),y-19*math.cos(t))],NAVY,3);a.line([(x,y),(x+23*math.sin(t*2),y-23*math.cos(t*2))],CORAL,3)
def dashed(a,p1,p2,t=0,color=TEAL):
 dx=p2[0]-p1[0];dy=p2[1]-p1[1];dist=math.hypot(dx,dy)
 for step in range(-20,int(dist),22):
  u=max(0,(step+(t*24)%22)/dist);v=min(1,u+10/dist)
  if v>u:a.line([(p1[0]+u*dx,p1[1]+u*dy),(p1[0]+v*dx,p1[1]+v*dy)],color,4)

def base(title,index):
 im=Image.new('RGB',(W,H),PAPER);a=Art(im)
 rng=random.Random(27)
 for _ in range(2400):
  x,y=rng.randrange(W),rng.randrange(H);a.d.point((x,y),fill='#EFE6D6')
 a.rect((42,32,84,74),TEAL,r=13,outline=None);a.text((63,52),'D',28,PAPER,True,'mm');a.text((98,40),'DismissalCue',27,TEAL,True)
 if 3<=index<=7:a.text((1238,45),'Product vision • In development',17,TEAL,False,'ra')
 words=title.split();lines=[];line=''
 for word in words:
  test=(line+' '+word).strip()
  if a.d.textlength(test,font=font(40,True))>1160 and line:lines.append(line);line=word
  else:line=test
 if line:lines.append(line)
 for n,line in enumerate(lines[:2]):a.text((60,105+n*47),line,40,NAVY,True)
 a.line([(60,192),(220,192)],CORAL,5)
 # Subtitle safety zone intentionally has no art/text below y=594.
 return im

def frame(index,t,duration,title):
 u=t/duration;im=base_cache[(index,title)].copy();a=Art(im)
 if index==0:
  school(a,885,266,.82);tree(a,1204,410,.68);a.rect((40,468,1240,572),'#E6E9E0',r=26,outline=None)
  for n in range(6):a.line([(70+n*215,529),(175+n*215,529)],PAPER,4)
  for n,color in enumerate([TEAL,CORAL,GOLD,BLUE]):car(a,-95+n*330+ease(u)*80,448,1.18,color,t)
  person(a,220,410,.93,CORAL,1,'worried','phone',t);clock(a,332,270,t*1.2,39)
  for xx in [425,485,545]:a.oval((xx,280+math.sin(t*2+xx)*4,xx+10,290+math.sin(t*2+xx)*4),CORAL,None)
 elif index==1:
  school(a,740,294,1.12);a.line([(50,562),(1225,562)],'#DACFBB',3)
  # Idling car beside the curb; teacher is near its rear tailpipe.
  car(a,595,535,.88,BLUE,0);exhaust(a,592,548,t)
  weather=0 if t<weather_marks[0] else 1 if t<weather_marks[1] else 2;phase=(u*3)%1
  # Teacher stays recognizable as the weather changes around her.
  person(a,467+math.sin(t*1.2)*2,553,1.42,TEAL,2,'worried','umbrella',t,glasses=True)
  person(a,771,552,.79,CORAL,0,'worried','stand',t)
  person(a,867,552,.74,GOLD,1,'worried','stand',t+1)
  a.line([(541,353),(541,228)],NAVY,5);a.arc((535,346,555,372),0,190,width=4)
  a.poly([(405,238),(417,217),(442,191),(485,171),(534,165),(583,173),(625,195),(656,238),(609,225),(566,239),(522,226),(477,239),(433,226)],CORAL,width=4)
  a.line([(534,165),(522,226)],NAVY,2);a.line([(534,165),(433,226)],NAVY,2);a.line([(534,165),(609,225)],NAVY,2)
  if weather==0:
   cloud(a,160,246,1.4);cloud(a,1010,219,1.3)
   for n in range(45):x=(n*137+t*25)%1240;y=238+(n*83+t*165)%292;a.line([(x,y),(x-8,y+17)],BLUE,2)
   a.text((72,572),'Rain',20,TEAL,True)
  elif weather==1:
   cloud(a,170,248,1.35,'#DEE7EC')
   for n in range(38):x=(n*137+math.sin(t+n)*20)%1240;y=225+(n*83+t*36)%327;a.oval((x,y,x+5,y+5),'#92ADB9',None)
   a.text((72,572),'Cold',20,TEAL,True)
  else:sun(a,1090,250,t,1.35);a.text((72,572),'Heat',20,TEAL,True)
 elif index==2:
  a.oval((330,250,950,530),'#F5E3CE',None);person(a,431,546,1.23,TEAL,2,'worried','stand',t,glasses=True);person(a,844,546,1.23,CORAL,1,'worried','phone',t)
  # A gently breathing question mark provides a genuine editorial pause.
  size=round(138+math.sin(t*1.2)*4);a.text((640,398),'?',size,TEAL,True,'mm');a.oval((589,254,605,270),GOLD,None);a.oval((701,486,713,498),CORAL,None)
 elif index==3:
  centers=[(260,424),(640,378),(1020,424)];dashed(a,centers[0],centers[1],t);dashed(a,centers[1],centers[2],t)
  for x,y,color in [(260,424,MINT),(640,378,'#F2D7AD'),(1020,424,'#F4D2C9')]:a.oval((x-133,y-128,x+133,y+128),color,None)
  person(a,253,516,1.2,TEAL,0,pose='phone',phase=t);person(a,640,476,1.2,CORAL,2,pose='wave',phase=t,hijab=True);person(a,1020,516,1.2,BLUE,1,pose='point',phase=t,glasses=True)
  for x,label,y in [(260,'Parents',563),(640,'Classrooms',525),(1020,'School office',563)]:a.text((x,y),label,24,NAVY,True,'mm')
 elif index==4:
  a.oval((115,485,1190,575),'#E3E8D9',None);school(a,867,270,.9)
  car(a,115+ease(u)*60,450,1.17,TEAL,t)
  person(a,456,541,1.17,BLUE,0,pose='wave',phase=t)
  walk=min(1,u*1.5);person(a,760-105*ease(walk),539,.83,CORAL,1,pose='walk',phase=t*4);person(a,850-130*ease(walk),541,.72,GOLD,2,pose='walk',phase=t*4+1)
  person(a,982,553,1.26,TEAL,2,pose='point',phase=t,glasses=True)
  a.rect((427,262,767,321),PAPER,r=21,outline=TEAL,width=2);a.check(453,293);a.text((478,277),'School-approved pickup',21,TEAL,True)
  a.text((642,578),'Staff verify the physical handoff',22,NAVY,True,'mm')
 elif index==5:
  a.rect((76,240,603,545),PAPER,r=23,width=3);a.rect((76,240,603,302),TEAL,r=20,outline=None);a.text((103,258),'School-owned calendar',25,PAPER,True)
  for col,label in enumerate(['M','T','W','T','F']):a.text((128+97*col,326),label,20,NAVY,True,'mm')
  for row in range(3):
   for col in range(5):
    x=96+97*col;y=353+54*row;fill=MINT if (row+col)%3==0 else '#F2EADF';a.rect((x,y,x+66,y+37),fill,r=9,outline=None)
  a.rect((168,413,419,470),CORAL,r=10,outline=None);a.text((293,441),'Soccer Tue · Art Thu',19,NAVY,True,'mm')
  a.rect((97,488,582,533),MINT,r=10,outline=None);a.text((339,510),'Early dismissal · whole school',21,TEAL,True,'mm')
  person(a,765,549,1.2,LAV,2,pose='phone',phase=t,hijab=True);person(a,899,552,.85,CORAL,1,pose='wave',phase=t);clock(a,1054,356,t*.12,63)
  a.text((338,575),'Before a holiday weekend',21,TEAL,True,'mm');a.text((890,575),"Clubs: this child's later pickup",21,TEAL,True,'mm')
 elif index==6:
  person(a,277,559,1.45,CORAL,1,pose='phone',phase=t);person(a,1014,559,1.45,TEAL,2,pose='wave',phase=t,glasses=True)
  a.rect((470,230,811,532),PAPER,r=28,outline=TEAL,width=4);a.rect((495,252,786,312),MINT,r=15,outline=None);a.text((640,282),'School help',25,TEAL,True,'mm')
  for j,(label,col) in enumerate([('Clear next steps',TEAL),('Known school contact',TEAL),('Protected account help',TEAL)]):
   y=352+j*62;a.check(510,y+10,color=col);a.text((535,y),label,19,NAVY,True)
  dashed(a,(330,385),(455,385),t);dashed(a,(827,385),(953,385),t)
 elif index==7:
  school(a,505,242,1.34);sun(a,1134,253,t);tree(a,115,428,.93);a.rect((35,510,1245,575),'#DEE6D8',r=25,outline=None)
  car(a,75+ease(u)*155,486,1.08,TEAL,t);car(a,889+ease(u)*165,486,1.02,CORAL,t)
  exhaust(a,73+ease(u)*155,500,t,max(.12,1-u));exhaust(a,887+ease(u)*165,500,t+.5,max(.12,1-u))
  person(a,530,552,1.08,TEAL,2,pose='wave',phase=t,glasses=True);person(a,666,551,.75,GOLD,1,pose='walk',phase=t*3);person(a,747,550,.78,CORAL,0,pose='wave',phase=t)
  a.oval((586,317,699,398),PAPER,TEAL,3);a.check(640,357,2)
 elif index==8:
  # Board/community setting makes the audience concrete without a fake product UI.
  a.oval((213,286,1068,570),MINT,None);a.rect((387,237,895,397),PAPER,r=22,outline=TEAL,width=3);a.text((641,285),'A better dismissal day',32,TEAL,True,'mm');a.text((641,338),'Talk to your school, district or school board.',21,NAVY,False,'mm')
  person(a,333,551,1.07,TEAL,2,pose='wave',phase=t,hijab=True);person(a,537,556,.94,CORAL,1,pose='stand',phase=t,glasses=True);person(a,755,556,.94,BLUE,0,pose='stand',phase=t);person(a,960,551,1.07,GOLD,3,pose='wave',phase=t)
  a.rect((409,536,867,589),TEAL,r=26,outline=None);a.text((638,562),'dismissalcue.com',26,PAPER,True,'mm')
 # Tiny page dots provide rhythm without competing with subtitle lines.
 for n in range(9):a.oval((54+n*15,592,60+n*15,598),TEAL if n==index else '#DDD5C7',None)
 return im
base_cache={}
weather_marks=(3.72,4.753)
def caption_frame(im,global_time,captions):
 a=Art(im);a.rect((40,613,1240,704),NAVY,r=18,outline=None)
 matches=[c for c in captions if float(c['start'])<=global_time<float(c['end'])]
 if not matches:return im
 text=max(matches,key=lambda c:float(c['start']))['text'];size=29;lines=[];line=''
 for word in text.split():
  test=(line+' '+word).strip()
  if a.d.textlength(test,font=font(size,True))>1120 and line:lines.append(line);line=word
  else:line=test
 if line:lines.append(line)
 if len(lines)>2:raise ValueError('Caption needs more than two lines: '+text)
 y=657 if len(lines)==1 else 639
 for i,line in enumerate(lines):a.text((640,y+i*36),line,size,PAPER,True,'mm')
 return im

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('manifest',type=Path);ap.add_argument('--output',type=Path,default=Path('.local/story/silent.mp4'));ap.add_argument('--poster',type=Path);ap.add_argument('--contact-sheet',type=Path);ap.add_argument('--fps',type=int,default=30);ap.add_argument('--preview-only',action='store_true');ap.add_argument('--no-captions',action='store_true',help='Render a caption-free alternate');args=ap.parse_args()
 data=json.loads(args.manifest.read_text());scenes=data['scenes'];captions=data.get('captions',[])
 global weather_marks
 def phrase_time(phrase,fallback):
  for c in captions:
   text=c['text'].lower();offset=text.find(phrase)
   if offset>=0:
    # Caption chunks may contain all three weather phrases; interpolate within chunk.
    return float(c['start'])-float(scenes[1].get('start',0))+(float(c['end'])-float(c['start']))*offset/max(1,len(text))
  return fallback
 cold=phrase_time('cold',3.72)
 heat=phrase_time('hot afternoon',phrase_time('afternoon sun',4.753))
 weather_marks=(cold,heat)
 if len(scenes)!=9:raise ValueError('Story renderer needs exactly nine scenes')
 for i,s in enumerate(scenes):
  if not isinstance(s.get('title'),str) or not 1<=float(s.get('duration',0))<=30:raise ValueError('Each scene needs a title and duration1–30 seconds')
  base_cache[(i,s['title'])]=base(s['title'],i)
 args.output.parent.mkdir(parents=True,exist_ok=True);poster=args.poster or args.output.with_suffix('.poster.jpg');sheet=args.contact_sheet or args.output.with_suffix('.contact.jpg');poster.parent.mkdir(parents=True,exist_ok=True);sheet.parent.mkdir(parents=True,exist_ok=True)
 thumbs=[]
 for i,s in enumerate(scenes):
  im=frame(i,float(s['duration'])*.5,float(s['duration']),s['title']);
  if captions and not args.no_captions:im=caption_frame(im,float(s.get('start',sum(float(z['duration']) for z in scenes[:i])))+float(s['duration'])*.5,captions)
  im.thumbnail((640,360),Image.Resampling.LANCZOS);thumbs.append(im)
 contact=Image.new('RGB',(1920,1080),PAPER)
 for i,im in enumerate(thumbs):contact.paste(im,((i%3)*640,(i//3)*360))
 contact.save(sheet,quality=93);frame(7,3,float(scenes[7]['duration']),scenes[7]['title']).save(poster,quality=94)
 if args.preview_only:print(json.dumps({'poster':str(poster),'contact_sheet':str(sheet)}));return
 ffmpeg=os.environ.get('FFMPEG','ffmpeg');command=[ffmpeg,'-y','-hide_banner','-loglevel','error','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(args.fps),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(args.output)]
 process=subprocess.Popen(command,stdin=subprocess.PIPE)
 try:
  for i,s in enumerate(scenes):
   duration=float(s['duration']);count=round(duration*args.fps)
   for n in range(count):
    im=frame(i,n/args.fps,duration,s['title'])
    # Quarter-second paper fade avoids double-exposed titles between scenes.
    fade_frames=max(1,round(.125*args.fps));opacity=0
    if i>0 and n<fade_frames:opacity=1-ease(n/fade_frames)
    if i<len(scenes)-1 and n>=count-fade_frames:opacity=ease((n-(count-fade_frames))/fade_frames)
    if opacity:im=Image.blend(im,Image.new('RGB',(W,H),PAPER),opacity)
    if captions and not args.no_captions:im=caption_frame(im,float(s.get('start',sum(float(z['duration']) for z in scenes[:i])))+n/args.fps,captions)
    process.stdin.write(im.tobytes())
   print(f'Rendered scene {i+1}/9',flush=True)
  process.stdin.close();code=process.wait()
  if code:raise RuntimeError(f'Encoder failed ({code})')
 except BaseException:
  process.kill();process.wait();raise
 print(json.dumps({'video':str(args.output),'poster':str(poster),'contact_sheet':str(sheet),'fps':args.fps,'duration':sum(round(float(s['duration'])*args.fps)/args.fps for s in scenes)}))
if __name__=='__main__':main()
