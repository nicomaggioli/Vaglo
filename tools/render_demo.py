"""Full 4K/60fps tour: native sample-dashboard captures and ElevenLabs narration."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess, json, imageio_ffmpeg, functools
R=Path(__file__).resolve().parents[1]; A=R/'assets'; S=A/'demo-stills'
M=json.loads((A/'narration-production.json').read_text())
SC=json.loads((R/'tools/demo-scenes.json').read_text())
W,H,FPS,DURATION=3840,2160,60,M['video_duration']
def mapped(t):return (t-sum(max(0,min(t,b)-a) for a,b in M['cuts_seconds'] if t>a))/M['tempo']
@functools.lru_cache(maxsize=32)
def shot(name):
    im=Image.open(S/f'{name}.webp').convert('RGB')
    assert im.size==(W,H),f'{name}: expected native 4K, got {im.size}'
    return im
def ease(x):
    x=max(0,min(1,x));return x*x*(3-2*x)
# Source-audio times preserve the semantic cut points before silence/tempo editing.
EDIT=[(0,'20-help'),(8.53,'06-documents'),(10.995,'02-analysis'),
(20.35,'01-pipeline'),(36.14,'02-analysis'),(45.733,'11-analysis-scope'),
(54.59,'03-projects'),(66.451,'04-team'),(72.147,'04-team-alternate'),
(78.723,'05-matrix'),(90.368,'12-generators'),(97.522,'06-documents'),
(107.167,'07-proposal'),(119.925,'13-analysis-feedback'),(127.101,'14-feedback'),
(133.023,'08-library'),(137.8,'09-search-med'),(138.0,'09-search'),
(140.429,'10-personnel'),(144.504,'15-subconsultants'),(152.384,'16-intake'),
(163.413,'17-proposals'),(168.05,'18-scoring'),(171.7,'19-metrics'),
(176.414,'20-help'),(178.96,'21-folders'),(182.31,'22-roadmap'),
(185.32,'23-lifecycle'),(188.1,'24-availability'),
(191.371,'01-pipeline'),(197.2,'07-proposal')]
EDIT=[(mapped(t),name) for t,name in EDIT]
TOP,RIGHT=337,2880
# Scroll actual captured content; preserve the fixed header and assistant panel.
def scroll_canvas(items):
    canvas=Image.new('RGB',(RIGHT,4300),'white')
    for name,offset in items:canvas.paste(shot(name).crop((0,TOP,RIGHT,H)),(0,round(offset*8/3)))
    return canvas
BEFORE=scroll_canvas([('03-projects',0),('04-team',676.125)])
AFTER=scroll_canvas([('03-projects',0),('04-team-alternate',674.8125),('05-matrix',839.4375)])
def scroll_frame(offset,alt=False):
    im=shot('03-projects').copy();y=round(offset*8/3)
    im.paste((AFTER if alt else BEFORE).crop((0,y,RIGHT,y+H-TOP)),(0,TOP));return im
cursor=Image.new('RGBA',(256,320));d=ImageDraw.Draw(cursor)
d.polygon([(12,8),(12,218),(62,173),(109,270),(145,251),(98,159),(165,151)],fill='#16181b',outline='white',width=11)
cursor=cursor.resize((48,60),Image.Resampling.LANCZOS)
TEAM=mapped(66.451);MATRIX=mapped(78.723)
# Only brief navigation gestures; the small pointer clears the reading area.
actions=[(mapped(36.14),(1250,740),(840,465)),(mapped(54.59),(850,700),(825,460)),(mapped(72.147),(2010,620),(2080,365)),(mapped(137.8),(2140,490),(2790,255))]
end=Image.new('RGB',(W,H),'white');d=ImageDraw.Draw(end)
font=lambda n:ImageFont.truetype(str(A/'fonts/geist.ttf'),n)
d.text((W/2,H/2-110),'rhodo',font=font(196),fill='#0b0d11',anchor='mm')
d.text((W/2,H/2+90),'Find the opportunities worth pursuing.',font=font(55),fill='#58645a',anchor='mm')
def frame(t):
    if t>=M['audio_duration']-.15:return end
    name=next(name for start,name in reversed(EDIT) if start<=t);im=shot(name)
    if TEAM-.25<=t<TEAM+.4:im=scroll_frame(676.125*ease((t-TEAM+.25)/.65))
    elif MATRIX-.25<=t<MATRIX+.35:im=scroll_frame(674.8125+(839.4375-674.8125)*ease((t-MATRIX+.25)/.6),True)
    for b,p,q in actions:
        if b-.5<=t<b:
            k=ease((t-b+.5)/.5);x=round(p[0]+(q[0]-p[0])*k);y=round(p[1]+(q[1]-p[1])*k)
            im=im.copy();im.paste(cursor,(x,y),cursor)
    return im

def render():
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    cmd=[ff,'-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-i',str(A/'demo-narration-elevenlabs.wav'),'-c:v','libx264','-preset','veryfast','-crf','16','-threads','4','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-af','apad','-movflags','+faststart','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-t',str(DURATION),str(A/'rhodo-demo.mp4')]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE);previous=None;pixels=None
    try:
        for i in range(FPS*DURATION):
            im=frame(i/FPS)
            if im is not previous:pixels=im.tobytes();previous=im
            p.stdin.write(pixels)
            if i%(FPS*10)==0:print(f'Rendered {i/FPS:.0f}/{DURATION}s',flush=True)
    finally:p.stdin.close()
    assert p.wait()==0
    print('Finished:',A/'rhodo-demo.mp4')
if __name__=='__main__':render()
