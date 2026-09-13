"""Render VAGLO's original 42s film. pip install pillow numpy imageio-ffmpeg.
Input: assets/dashboard.webp (real dashboard styling, entirely synthetic data).
Run from any directory. No live services or private records are used.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import imageio_ffmpeg, subprocess, wave, math, tempfile
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'assets'
W,H,FPS,SECONDS=1280,720,24,42
BG=(15,39,29); LIME=(212,241,148); PAPER=(244,246,232); MUTED=(166,190,163)
fonts={}
def font(size,serif=False):
 key=(size,serif)
 if key not in fonts: fonts[key]=ImageFont.truetype(str(A/'fonts'/('instrument-serif-italic.ttf' if serif else 'dm-sans.ttf')),size)
 return fonts[key]
def txt(im,xy,s,size=25,c=PAPER,serif=False):
 ImageDraw.Draw(im).text(xy,s,font=font(size,serif),fill=c,stroke_width=0)
def smooth(v): return max(0,min(1,v))**2*(3-2*max(0,min(1,v)))
def box(im,xy,fill,outline=None,r=12,width=1): ImageDraw.Draw(im).rounded_rectangle(xy,r,fill=fill,outline=outline,width=width)
def line(im,pts,fill,width=1): ImageDraw.Draw(im).line(pts,fill=fill,width=width)
def logo(im,x,y,scale=1,color=PAPER):
 d=ImageDraw.Draw(im)
 for n in range(3):
  yy=y+n*13*scale
  d.line([(x,yy),(x+19*scale,yy+11*scale),(x+38*scale,yy)],fill=color,width=max(1,int(5*scale)))
 txt(im,(x+53*scale,y-9*scale),'VAGLO',int(33*scale),color)
base=np.zeros((H,W,3),dtype=np.uint8)
yy,xx=np.mgrid[0:H,0:W]
glow=np.exp(-((xx-940)**2/(2*370**2)+(yy-390)**2/(2*300**2)))
for i,c in enumerate(BG): base[:,:,i]=np.clip(c+glow*(17 if i!=1 else 25),0,255)
bg=Image.fromarray(base)
def background(t=0,tag='PRODUCT FILM'):
 im=bg.copy();d=ImageDraw.Draw(im)
 # Fine orbital geometry gives the film a spatial, architectural quality.
 for rad in [200,330,460,590]:
  cx,cy=930+12*math.sin(t/4),350
  d.ellipse((cx-rad,cy-rad,cx+rad,cy+rad),outline=(42,68,44),width=1)
 logo(im,49,39,.63)
 txt(im,(49,664),'VAGLO  /  YOUR NEXT CHAPTER',10,MUTED)
 txt(im,(990,664),tag,10,MUTED)
 line(im,[(50,643),(1230,643)],(59,80,48))
 line(im,[(50,643),(50+1180*min(t/SECONDS,1),643)],LIME,2)
 return im
shot=Image.open(A/'dashboard.webp').convert('RGB')
def paste_shadow(im,pic,xy,angle=0):
 p=pic.convert('RGBA')
 if angle:p=p.rotate(angle,Image.Resampling.BICUBIC,expand=True)
 x,y=map(int,xy)
 sh=Image.new('RGBA',(p.width+80,p.height+80));sh.paste((0,0,0,80),(40,40,p.width+40,p.height+40));sh=sh.filter(ImageFilter.GaussianBlur(20));im.paste(sh,(x-40,y-20),sh);im.paste(p,(x,y),p)
def tag(im,x,y,text,col=LIME):
 size=font(13).getbbox(text)[2]+26
 box(im,(x,y,x+size,y+32),(40,65,44),col,6);txt(im,(x+13,y+7),text,13,col)
def poster():
 im=background(0,'')
 # No words on the poster: the website supplies the accessible headline.
 im=bg.copy()
 for r in [200,320,440,560]:ImageDraw.Draw(im).ellipse((940-r,380-r,940+r,380+r),outline=(54,79,47),width=1)
 pic=shot.resize((965,543),Image.Resampling.LANCZOS)
 paste_shadow(im,pic,(450,138),angle=5)
 # A clear score callout lifts one product detail out of the interface.
 box(im,(844,516,1130,612),(236,243,221),r=10)
 txt(im,(869,528),'92%',39,(37,70,42));txt(im,(972,535),'A stronger fit.',17,(37,70,42));txt(im,(972,560),'A clearer next move.',12,(94,113,82))
 im.save(A/'trailer-poster.jpg',quality=91,optimize=True)

def document_card(title,kicker,rows):
 im=Image.new('RGB',(357,430),(249,249,240));d=ImageDraw.Draw(im)
 txt(im,(27,22),'VAGLO',17,(29,64,43));txt(im,(27,72),kicker,10,(99,122,76));txt(im,(26,103),title,45,(29,64,43),True)
 line(im,[(27,240),(330,240)],(42,72,44),2)
 for i,(a,b) in enumerate(rows):
  y=258+i*43;txt(im,(27,y),a,12,(43,68,45));txt(im,(286,y),b,11,(119,135,104));line(im,[(27,y+31),(330,y+31)],(218,224,207))
 txt(im,(27,407),'ILLUSTRATIVE PACKAGE  /  SAMPLE DATA',8,(118,130,105))
 return im
DOCS=[document_card('Your people.\nTheir expertise.','SECTION E / RESUMES',[('Personnel qualifications','01'),('Relevant project experience','02'),('Professional registrations','03')]),document_card('Your work.\nYour proof.','SECTION F / PROJECT SHEETS',[('Project overview','01'),('Scope and delivery','02'),('Direct relevance','03')]),document_card('Your strongest\ncase.','SF330 / QUALIFICATIONS',[('Team resumes','E'),('Project experience','F'),('Your approach','H')])]
def scene(t):
 im=background(t)
 if t<8:
  k=smooth(t/.95);off=int((1-k)*30)
  txt(im,(70,178+off),'Your best work',72)
  txt(im,(70,266+off),'deserves your',72)
  txt(im,(70,344+off),'next win.',108,LIME,True)
  if t>2:
   a=smooth((t-2)/1); overlay=Image.new('RGBA',im.size);txt(overlay,(76,512),'Your experience. Put to work.',23,(*MUTED,int(255*a)));im.paste(overlay,(0,0),overlay)
  # Quiet signal dots track around the circles.
  d=ImageDraw.Draw(im)
  for r,phase in [(200,0),(330,1.5),(460,2.4)]:
   ang=t*.09+phase; x=930+math.cos(ang)*r;y=350+math.sin(ang)*r;d.ellipse((x-4,y-4,x+4,y+4),fill=LIME)
 elif t<18:
  q=t-8;k=smooth(q/1.2)
  txt(im,(53,107),'01 / DISCOVER',12,LIME)
  txt(im,(49,142),'Find the work',55)
  txt(im,(49,199),'worth your time.',66,LIME,True)
  txt(im,(53,300),'Relevant opportunities.',20,MUTED)
  txt(im,(53,331),'Ranked around your firm.',20,MUTED)
  # Zoom gently into the real dashboard's analyzed column.
  scale=1+max(0,q-3)*.017
  pic=shot.resize((int(880*scale),int(495*scale)),Image.Resampling.LANCZOS)
  paste_shadow(im,pic,(502+int((1-k)*220),115-int((scale-1)*120)))
  if q>2:tag(im,59,400,'SAM.gov  →  Your opportunity pipeline')
  if q>4:
   box(im,(692,447,1020,566),(239,246,225),r=10)
   txt(im,(716,457),'92%',52,(37,70,42));txt(im,(844,467),'Fit score',18,(37,70,42));txt(im,(844,498),'See the reasoning.',13,(94,113,82))
  txt(im,(53,599),'ACTUAL DASHBOARD STYLING  /  SAMPLE DATA',10,MUTED)
 elif t<28:
  q=t-18
  txt(im,(53,107),'02 / BUILD',12,LIME)
  txt(im,(49,143),'Turn experience',53)
  txt(im,(49,203),'into your edge.',69,LIME,True)
  txt(im,(53,310),'Your people. Your projects.',20,MUTED)
  txt(im,(53,342),'One connected SF330.',20,MUTED)
  tag(im,57,412,'Built from your firm’s own record')
  for i,pic in enumerate(DOCS):
   k=smooth((q-i*.65)/1.15)
   x=579+i*103+int((1-k)*300);y=153+i*9+int(math.sin(q*.65+i)*4)
   paste_shadow(im,pic,(x,y),angle=8-i*8)
  txt(im,(53,599),'ILLUSTRATIVE PACKAGE ASSEMBLY',10,MUTED)
 elif t<37:
  q=t-28
  txt(im,(53,107),'03 / REVIEW',12,LIME)
  txt(im,(49,151),'Less uncertainty.',54)
  txt(im,(49,215),'More confidence.',66,LIME,True)
  txt(im,(53,320),'Requirements checked.',20,MUTED)
  txt(im,(53,352),'Missing facts made visible.',20,MUTED)
  tag(im,57,433,'Your team makes the final call')
  x=623+int((1-smooth(q/.8))*150)
  box(im,(x,135,x+580,583),(242,246,232),r=13)
  txt(im,(x+28,159),'THE REVIEW CHECKPOINT',11,(93,115,76))
  txt(im,(x+28,202),'A clear path to ready.',32,(33,61,38))
  rows=[('Project experience documented','Section F · supporting records attached'),('Team participation mapped','Section G · matched to project history'),('Confirm personnel availability','Firm confirmation required')]
  for i,(a,b) in enumerate(rows):
   if q<i*.7+.4:continue
   y=276+i*81
   line(im,[(x+28,y-7),(x+548,y-7)],(210,220,196))
   color=(98,124,72) if i<2 else (155,119,42)
   ImageDraw.Draw(im).ellipse((x+29,y+9,x+57,y+37),fill=color)
   
   if i<2:line(im,[(x+36,y+23),(x+41,y+28),(x+50,y+17)],(255,255,240),2)
   else:txt(im,(x+40,y+11),'!',15,(255,255,240))
   txt(im,(x+74,y+6),a,17,(33,61,38));txt(im,(x+74,y+34),b,12,(108,126,90))
  txt(im,(x+29,545),'A missing fact stays visible until your team resolves it.',12,(107,125,90))
  txt(im,(53,599),'ILLUSTRATIVE REVIEW  /  HUMAN APPROVAL',10,MUTED)
 else:
  q=t-37
  logo(im,485,159,1.18,LIME)
  a='Your next chapter.';b='Starts with VAGLO.'
  for text,y,size,s in [(a,284,68,False),(b,357,86,True)]:
   width=font(size,s).getbbox(text)[2];txt(im,((1280-width)/2,y),text,size,LIME if s else PAPER,s)
  txt(im,(477,516),'Discover. Build. Review.',24,MUTED)
 # Fade through dark on each cut; short ramps preserve rhythm.
 cuts=[0,8,18,28,37,42]
 near=min(abs(t-c) for c in cuts)
 fade=smooth(near/.35)
 if fade<1:im=Image.blend(Image.new('RGB',im.size,BG),im,fade)
 return im

def soundtrack(path):
 sr=44100;t=np.arange(sr*SECONDS)/sr;audio=np.zeros_like(t)
 # Original A-minor ambient score. No samples or licensed music.
 chords=[(110,164.81,220,261.63),(87.31,130.81,174.61,220),(130.81,196,261.63,329.63),(98,146.83,196,246.94)]
 for start in range(0,SECONDS,7):
  freqs=chords[(start//7)%4];local=t-start;env=np.clip(local/1.8,0,1)*np.clip((8-local)/2,0,1);env[local<0]=0
  for f in freqs:
   audio+=.035*env*(np.sin(2*np.pi*f*t)+.25*np.sin(2*np.pi*(f*2.002)*t))
 for beat in np.arange(8,37,.625):
  dt=t-beat;on=dt>=0;decay=np.exp(-np.maximum(dt,0)*13)*on
  audio+=.11*np.sin(2*np.pi*(48*dt+2*(1-np.exp(-np.maximum(dt,0)*20))))*decay
 # Subtle descending tonal transitions at each chapter, and sparse high arpeggio.
 for i,start in enumerate(np.arange(8,37,1.25)):
  dt=t-start;on=dt>=0;f=[440,523.25,659.25,783.99][i%4]
  audio+=.025*np.sin(2*np.pi*f*dt)*np.exp(-np.maximum(dt,0)*3)*on
 audio*=np.clip(t/2,0,1)*np.clip((SECONDS-t)/2,0,1)
 audio=np.tanh(audio*1.5)*.65
 stereo=np.column_stack((audio,np.roll(audio,220))).astype(np.float32)
 with wave.open(str(path),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((stereo*32767).astype('<i2').tobytes())

if __name__=='__main__':
 poster()
 with tempfile.TemporaryDirectory() as tmp:
  tmp=Path(tmp);soundtrack(tmp/'score.wav');ff=imageio_ffmpeg.get_ffmpeg_exe()
  cmd=[ff,'-hide_banner','-loglevel','error','-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',str(tmp/'score.wav'),'-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t',str(SECONDS),str(A/'vaglo-trailer.mp4')]
  proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
  for frame in range(FPS*SECONDS):
   t=frame/FPS;im=scene(t);proc.stdin.write(im.tobytes())
   if frame%240==0:print(f'Rendered {frame/FPS:.0f}s / {SECONDS}s',flush=True)
  proc.stdin.close()
  if proc.wait()!=0:raise RuntimeError('Video encoding failed')
  for t in [3,12,23,32,39]:scene(t).save(A/f'trailer-frame-{t}.jpg',quality=85)
 print('Trailer complete:',A/'vaglo-trailer.mp4')
