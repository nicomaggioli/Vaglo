"""Render the narrated 85-second walkthrough from real frontend captures.
Captures use isolated synthetic fixtures, never the customer database.
The edit adds a pointer, reading pauses, and captions. UI states are captured,
not recreated. Requires Pillow, numpy, imageio-ffmpeg (requirements-media.txt).
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import imageio_ffmpeg,subprocess,json,math,textwrap
R=Path(__file__).resolve().parents[1];A=R/'assets';S=A/'demo-stills'
SC=json.loads((R/'tools/demo-scenes.json').read_text())
W,H,FPS=1440,1000,24
shots={p.stem:Image.open(p).convert('RGB').resize((1440,900),Image.Resampling.LANCZOS) for p in S.glob('*.webp')}
font=lambda n:ImageFont.truetype(str(A/'fonts/inter.ttf'),n)
F12,F14,F20=font(12),font(14),font(20)
def ease(x):x=max(0,min(1,x));return x*x*(3-2*x)
def shot_for(t,s):
 name=s['shot']
 # Scroll frames were captured while scrolling the real interface.
 if 31.3<=t<33.7:
  k=min(10,int((t-31.3)/2.4*10));return shots[f'scroll-{k:02}']
 if 39.9<=t<41.3:
  k=min(14,10+int((t-39.9)/1.4*4));return shots[f'scroll-{k:02}']
 if 35.5<=t<37:return shots['04-team-options']
 if 37<=t<39:return shots['04-team-alternate']
 if 71<=t<76:return shots['09-search']
 return shots[name]
# Screen coordinates correspond to controls used during capture.
paths=[(0,650,510),(3,422,297),(7.8,390,223),(9.6,390,223),(10,200,250),(14,217,272),(17,510,414),(20,310,170),(22.7,310,170),(23,465,430),(28,660,510),(31,800,618),(34.6,905,229),(35.5,1033,229),(36.7,840,271),(37,840,544),(38.5,838,544),(39,838,229),(40,800,650),(44,922,835),(46.5,772,170),(47,270,246),(51,261,481),(54,1004,171),(56.7,1004,171),(57,740,470),(63,543,553),(66.6,1398,35),(67,103,318),(69,570,132),(71,570,132),(74.7,106,361),(76,398,262),(81,798,318),(85,798,318)]
clicks=[9.6,22.7,35.5,36.7,38.5,46.8,56.7,66.6,67.1,69.5,75.8]
def pointer(t):
 for j in range(len(paths)-1):
  a,b=paths[j:j+2]
  if a[0]<=t<b[0]:
   e=ease((t-a[0])/(b[0]-a[0]));return a[1]+(b[1]-a[1])*e,a[2]+(b[2]-a[2])*e
 return paths[-1][1:]
def frame(t):
 s=next(s for s in SC if s['start']<=t<s['end']);im=Image.new('RGB',(W,H),'#0b0d11');im.paste(shot_for(t,s),(0,32));d=ImageDraw.Draw(im)
 d.text((22,8),'Ellery  /  Product walkthrough',font=F12,fill='#fff')
 d.text((680,8),s['chapter'],font=F12,fill='#aab4ac')
 d.text((1242,8),'SAMPLE WORKSPACE',font=F12,fill='#65fc9f')
 x,y=pointer(t);y+=32
 for click in clicks:
  if 0<=t-click<.42:
   rad=9+26*(t-click)/.42;d.ellipse((x-rad,y-rad,x+rad,y+rad),outline='#28cb68',width=3)
 pts=[(x,y),(x+1,y+24),(x+8,y+18),(x+14,y+30),(x+20,y+27),(x+14,y+15),(x+24,y+14)]
 d.polygon(pts,fill='#0b0d11',outline='white',width=2)
 # Plain, permanently visible explanatory subtitles; voice track is optional.
 d.rectangle((0,933,W,H),fill='#0b0d11')
 d.text((26,950),s['caption'],font=F20,fill='#fff')
 d.text((1320,953),f'{int(t)//60}:{int(t)%60:02} / 1:25',font=F14,fill='#aeb8b0')
 d.rectangle((0,995,W*t/85,999),fill='#65fc9f')
 return im
ff=imageio_ffmpeg.get_ffmpeg_exe()
cmd=[ff,'-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-i',str(A/'demo-narration.m4a'),'-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart','-t','85',str(A/'ellery-demo.mp4')]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for i in range(FPS*85):
 p.stdin.write(frame(i/FPS).tobytes())
 if i%240==0:print('Rendered',i/FPS,'seconds',flush=True)
p.stdin.close();assert p.wait()==0
for sec in [3,14,27,35,38,43,52,60,72,80]:frame(sec).save(A/f'demo-frame-{sec}.jpg',quality=92)
def tc(x):return f'00:{int(x)//60:02}:{int(x)%60:02}.000'
(A/'demo.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{tc(s["start"])} --> {tc(s["end"])}\n{s["voice"]}' for s in SC)+'\n')
print('Finished:',A/'ellery-demo.mp4')
