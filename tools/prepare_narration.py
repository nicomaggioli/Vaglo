"""Rebuild the edited voice track from the preserved ElevenLabs source takes."""
from pathlib import Path
import json, wave, subprocess, tempfile, math
import imageio_ffmpeg

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'assets'
META=A/'narration-production.json'

def read_wave(path):
    with wave.open(str(path)) as w:
        return w.getparams(),w.readframes(w.getnframes())

def write_wave(path,params,data):
    with wave.open(str(path),'wb') as w:
        w.setparams(params);w.writeframes(data)

def prepare():
    m=json.loads(META.read_text());ff=imageio_ffmpeg.get_ffmpeg_exe()
    with tempfile.TemporaryDirectory() as temporary:
        temp=Path(temporary)
        def process(settings,key):
            raw=temp/f'{key}-raw.wav'
            subprocess.run([ff,'-loglevel','error','-y','-i',str(A/settings['source']),'-ar','44100','-ac','1',str(raw)],check=True)
            params,data=read_wave(raw);stride=params.nchannels*params.sampwidth
            cursor=0;pieces=[]
            for start,end in settings['cuts_seconds']:
                pieces.append(data[round(cursor*params.framerate)*stride:round(start*params.framerate)*stride]);cursor=end
            pieces.append(data[round(cursor*params.framerate)*stride:])
            cut=temp/f'{key}-cut.wav';write_wave(cut,params,b''.join(pieces))
            if settings['tempo']!=1:
                processed=temp/f'{key}-processed.wav'
                subprocess.run([ff,'-loglevel','error','-y','-i',str(cut),'-af',f'atempo={settings["tempo"]}',str(processed)],check=True)
                return read_wave(processed)
            return read_wave(cut)
        params,base=process(m['base'],'base');stride=params.nchannels*params.sampwidth
        cursor=0;pieces=[];shift=0
        for replacement in m['replacements']:
            start,end=replacement['base_start'],replacement['base_end']
            pieces.append(base[round(cursor*params.framerate)*stride:round(start*params.framerate)*stride])
            clip_params,clip=process(replacement,replacement['key'])
            assert clip_params[:3]==params[:3]
            replacement['duration']=len(clip)/(params.framerate*stride)
            replacement['start']=start+shift
            replacement['end']=replacement['start']+replacement['duration']
            pieces.append(clip);cursor=end;shift+=replacement['duration']-(end-start)
        pieces.append(base[round(cursor*params.framerate)*stride:]);combined=b''.join(pieces)
        write_wave(A/m['edited'],params,combined)
        m['audio_duration']=len(combined)/(params.framerate*stride)
        m['video_duration']=math.ceil(m['audio_duration']+1.8)
        META.write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n')
        print('Prepared audio:',m['audio_duration'],'seconds; video:',m['video_duration'])

if __name__=='__main__':prepare()
