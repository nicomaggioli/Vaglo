"""48-second 4K/60fps walkthrough of real frontend states with synthetic data.
Native screenshots, smooth editorial scrolling and a restrained pointer overlay.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess, json, imageio_ffmpeg
R=Path(__file__).resolve().parents[1]; A=R/'assets'; S=A/'demo-stills'
W,H,FPS,DURATION=3840,2160,60,48
SC=json.loads((R/'tools/demo-scenes.json').read_text())
shots={p.stem:Image.open(p).convert('RGB') for p in S.glob('*.webp')}
assert all(im.size==(W,H) for im in shots.values())
def ease(x):
    x=max(0,min(1,x)); return x*x*(3-2*x)
TOP,RIGHT=337,2880
# Stitch actual scroll captures, preserving fixed header/chat and native pixels.
def scroll_canvas(items):
    canvas=Image.new('RGB',(RIGHT,4300),'white')
    for name,offset in items:
        canvas.paste(shots[name].crop((0,TOP,RIGHT,H)),(0,round(offset*8/3)))
    return canvas
before=scroll_canvas([('03-projects',0),('04-team',676.125)])
after=scroll_canvas([('03-projects',0),('04-team-alternate',674.8125),('05-matrix',839.4375)])
def scroll_frame(offset,alt=False):
    im=shots['03-projects'].copy(); y=round(offset*8/3)
    im.paste((after if alt else before).crop((0,y,RIGHT,y+H-TOP)),(0,TOP))
    return im
cursor=Image.new('RGBA',(256,320)); d=ImageDraw.Draw(cursor)
d.polygon([(12,8),(12,218),(62,173),(109,270),(145,251),(98,159),(165,151)],fill='#16181b',outline='white',width=11)
cursor=cursor.resize((48,60),Image.Resampling.LANCZOS)
FIT,PROJECTS,TEAM,MATRIX,DOCS,PROPOSAL,LIBRARY,PEOPLE=[x['start'] for x in SC[1:]]
ALT=TEAM+2.0;SEARCH=LIBRARY+3.1
# Brief pointer gestures, then a clear unobstructed view.
actions=[(FIT-.53,FIT,(1270,780),(840,465)),(PROJECTS-.52,PROJECTS,(860,700),(825,460)),(ALT-.55,ALT,(2060,650),(2080,365)),(SEARCH-.52,SEARCH,(2090,570),(2790,255)),(PEOPLE-.53,PEOPLE,(1760,700),(230,826))]
end=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(end)
font=lambda n:ImageFont.truetype(str(A/'fonts/geist.ttf'),n)
d.text((W/2,H/2-160),'rhodo',font=font(196),fill='#0b0d11',anchor='mm')
d.text((W/2,H/2+52),'Find the opportunities worth pursuing.',font=font(55),fill='#58645a',anchor='mm')
def frame(t):
    if t>=46.8:return end.copy()
    scene=next(s for s in SC if s['start']<=t<s['end'])
    im=shots[scene['shot']].copy()
    if TEAM-.25<=t<TEAM+.4:im=scroll_frame(676.125*ease((t-TEAM+.25)/.65))
    elif TEAM+.4<=t<ALT:im=shots['04-team'].copy()
    elif ALT<=t<MATRIX-.25:im=shots['04-team-alternate'].copy()
    elif MATRIX-.25<=t<MATRIX+.35:im=scroll_frame(674.8125+(839.4375-674.8125)*ease((t-MATRIX+.25)/.6),True)
    if SEARCH<=t<SEARCH+.16:im=shots['09-search-med'].copy()
    elif SEARCH+.16<=t<PEOPLE:im=shots['09-search'].copy()
    for a,b,p,q in actions:
        if a<=t<b:
            k=ease((t-a)/(b-a));x=round(p[0]+(q[0]-p[0])*k);y=round(p[1]+(q[1]-p[1])*k)
            im.paste(cursor,(x,y),cursor)
    return im

def tc(x):
    ms=round(x*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'
(A/'demo.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{tc(s["start"])} --> {tc(s["end"])}\n{s["voice"]}' for s in SC)+'\n')
ff=imageio_ffmpeg.get_ffmpeg_exe()
cmd=[ff,'-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-i',str(A/'demo-narration-elevenlabs.wav'),'-c:v','libx264','-preset','veryfast','-crf','16','-threads','4','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-af','apad','-movflags','+faststart','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-t',str(DURATION),str(A/'rhodo-demo.mp4')]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
try:
    for i in range(FPS*DURATION):
        p.stdin.write(frame(i/FPS).tobytes())
        if i%(FPS*5)==0:print('Rendered',i/FPS,'seconds',flush=True)
finally:p.stdin.close()
assert p.wait()==0
for sec in [3,8,12,14.7,16,18,19.8,21,25,29,33,35,39,43]:frame(sec).save(A/f'demo-frame-{sec}.jpg',quality=95)
print('Finished:',A/'rhodo-demo.mp4')
