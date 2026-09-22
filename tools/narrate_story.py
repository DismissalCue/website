"""Generate the original Bella narration and timestamped captions for the cartoon.

ELEVENLABS_API_KEY is read only from the environment. One paid generation per uncached
script. Provider audio/alignment is cached privately under .local/story. Pass FFMPEG.
API reference: https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps
"""
from pathlib import Path
import base64, hashlib, json, math, os, re, subprocess, urllib.request, wave
ROOT=Path(__file__).resolve().parents[1]
MEDIA=ROOT/'media'; WORK=ROOT/'.local/story'
FFMPEG=os.environ.get('FFMPEG','ffmpeg')
def run(args):
    subprocess.run([FFMPEG,'-y','-hide_banner','-loglevel','error',*args],check=True)
def stamp(t):
    ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'
def main():
    WORK.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((MEDIA/'dismissalcue-story.json').read_text())
    full='\n\n'.join(s['text'] for s in manifest['scenes'])
    payload={'text':full,'model_id':'eleven_multilingual_v2','voice_settings':{'stability':0.65,'similarity_boost':0.75,'style':0.15,'use_speaker_boost':True,'speed':1.0}}
    fingerprint=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
    cache=WORK/(fingerprint+'.json')
    if not cache.exists():
        key=os.environ.get('ELEVENLABS_API_KEY','')
        if not key:raise RuntimeError('Narration credential is not configured')
        if not re.fullmatch(r'[A-Za-z0-9_-]+',key):raise RuntimeError('Invalid credential format')
        request_file=WORK/'request.json';request_file.write_text(json.dumps(payload))
        response=subprocess.run(['curl','--silent','--show-error','--fail','--config','-','--max-time','120','--header','Content-Type: application/json','--data-binary','@'+str(request_file),'https://api.elevenlabs.io/v1/text-to-speech/hpp4J3VqNfWAUOO0d1Us/with-timestamps?output_format=mp3_44100_128'],input='header = "xi-api-key: '+key+'"\n',text=True,capture_output=True)
        if response.returncode:raise RuntimeError('Narration generation failed; no published asset changed')
        data=response.stdout.encode()
        result=json.loads(data)
        if not result.get('audio_base64') or not result.get('alignment'):raise RuntimeError('Provider response missing audio or timing')
        cache.write_bytes(data);cache.chmod(0o600)
    result=json.loads(cache.read_text());alignment=result['alignment'];characters=''.join(alignment['characters'])
    if characters!=full:raise RuntimeError('Alignment text differs; review before rendering')
    starts=alignment['character_start_times_seconds'];ends=alignment['character_end_times_seconds']
    if len(starts)!=len(full) or len(ends)!=len(full):raise RuntimeError('Incomplete caption timing')
    raw=WORK/'original-bella.mp3';raw.write_bytes(base64.b64decode(result['audio_base64'],validate=True))
    decoded=WORK/'original-bella.wav'
    run(['-i',str(raw),'-ar','48000','-ac','1','-c:a','pcm_s16le',str(decoded)])
    with wave.open(str(decoded)) as audio: pcm=audio.readframes(audio.getnframes())
    cursor=0;offset=0;captions=[];clips=[]
    for i,scene in enumerate(manifest['scenes']):
        text=scene['text'];first=full.index(text,cursor);last=first+len(text);cursor=last
        cut=max(0,starts[first]-0.08);finish=ends[last-1]+0.18
        lead=0.25;tail=1.0 if i in (2,8) else 0.6
        duration=math.ceil((finish-cut+lead+tail)*30)/30
        scene.update(duration=duration,start=offset)
        clip=WORK/f'voice-{i+1:02}.wav'
        samples=bytes(round(lead*48000)*2)+pcm[round(cut*48000)*2:round(finish*48000)*2]
        length=round(duration*48000)*2
        samples=(samples+bytes(max(0,length-len(samples))))[:length]
        with wave.open(str(clip),'wb') as audio:
            audio.setnchannels(1);audio.setsampwidth(2);audio.setframerate(48000);audio.writeframes(samples)
        clips.append(clip)
        # Sentence/phrase boundaries are tied to provider character timestamps.
        words=list(re.finditer(r'\S+',text));group=[]
        for j,word in enumerate(words):
            group.append(word)
            length=group[-1].end()-group[0].start()
            if length>=62 or word.group()[-1] in '.?!' or j==len(words)-1:
                a,b=group[0].start(),group[-1].end();caption=text[a:b]
                captions.append({'start':offset+lead+starts[first+a]-cut,'end':min(offset+duration-0.15,offset+lead+ends[first+b-1]-cut+0.12),'text':caption})
                group=[]
        offset+=duration
    listing=WORK/'clips.txt';listing.write_text(''.join("file '"+str(p)+"'\n" for p in clips))
    run(['-f','concat','-safe','0','-i',str(listing),'-af','loudnorm=I=-16:TP=-1.5:LRA=11','-ar','48000',str(WORK/'narration.wav')])
    manifest['duration']=offset;manifest['captions']=captions
    (MEDIA/'dismissalcue-story.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (MEDIA/'dismissalcue-story.en.vtt').write_text('WEBVTT\n\n'+''.join(f'{stamp(c["start"])} --> {stamp(c["end"])}\n{c["text"]}\n\n' for c in captions))
    (MEDIA/'dismissalcue-story-transcript.txt').write_text(manifest['title']+'\nDismissalCue — product vision, in development\n\n'+'\n\n'.join(s['text'] for s in manifest['scenes'])+'\n')
    print(f'Original Bella narration ready: {offset:.2f}s, {len(captions)} timestamped captions; cached generation.')
if __name__=='__main__':main()
