"""Render the fictional Driveline walkthrough. Requires Pillow and ffmpeg.

Run from the website directory: python3 tools/render_demo.py
Optional: DRIVELINE_FONT_DIR points to a directory containing Arial.ttf and Arial Bold.ttf.
"""
from pathlib import Path
import math
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[1] / 'media'
OUT.mkdir(exist_ok=True)
FONT = Path(os.environ.get('DRIVELINE_FONT_DIR', '/System/Library/Fonts/Supplemental'))
FONTS = {(s, b): ImageFont.truetype(str(FONT / ('Arial Bold.ttf' if b else 'Arial.ttf')), s)
         for s in (14, 16, 18, 20, 22, 24, 28, 32, 40) for b in (False, True)}
NAVY, PANEL, BLUE, GREEN = '#0F172A', '#1E293B', '#3B82F6', '#34D399'
WHITE, MUTED = '#F8FAFC', '#94A3B8'
SCENES = [
    ('A calmer school pickup', 'One family. Two children. A coordinated journey home.',
     'ARRIVAL', 'Approaching campus', 'Sign-in with MFA already complete',
     ['School-issued family 1800', 'Alex Taylor  /  1800/1', 'Sam Taylor  /  1800/2'],
     'Geofence entry wakes the app; arrival still requires near-school checks.'),
    ('Check in near school', 'Select eligible children and confirm arrival once.',
     'PARENT APP', 'Ready to check in', 'Near-school presence + pickup rights checked',
     ['Selected: Alex  /  1800/1', 'Selected: Sam  /  1800/2', 'One confirmation for both children'],
     'Fresh presence and authorization checks must pass before check-in is accepted.'),
    ('Join the release queue', 'Arrival and classroom calls are separate events.',
     'DISPATCH CONSOLE', 'Family 1800 is queued', 'Children stay in class until the car is closer',
     ['01   Family 1742     At curb', '02   Family 1926     Moving forward', '03   Family 1800     Queued'],
     'Each child has one active pickup claim. Authorized parents receive an arrival alert.'),
    ('Call at the right moment', 'As the car moves forward, the classroom receives the call.',
     'CLASSROOM VIEW', 'Family 1800 called', 'Teacher receives the classroom call',
     ['Alex  /  1800/1     Called', 'Sam  /  1800/2      Called', 'Hallway display: tag 1800'],
     'The teacher acknowledges the call and follows the school\u2019s staging procedure.'),
    ('Staff confirm the handoff', 'The school retains its physical release procedure.',
     'CURB STAFF', 'Ready for handoff', 'Staff verify the authorized collector',
     ['Collector: Jordan Taylor', 'Alex + Sam  /  Family 1800', 'Staff confirmation required'],
     'Only staff confirmation records the handoff; arrival alone never releases a child.'),
    ('A clear pickup record', 'From arrival to handoff, every step has a place.',
     'PICKUP HISTORY', 'Pickup complete', 'Parent notification + recorded handoff',
     ['Children: Alex and Sam Taylor', 'Collector: Jordan Taylor', 'Confirmed by: Morgan, curb staff'],
     'Illustrative planned workflow. Fictional people and campus; no live services used.'),
]

def ease(x):
    x = max(0, min(1, x))
    return x*x*(3-2*x)

def frame(t):
    scene = min(5, int(t // 8))
    u = (t % 8) / 8
    title, subtitle, role, heading, detail, rows, caption = SCENES[scene]
    im = Image.new('RGB', (1280, 720), NAVY)
    d = ImageDraw.Draw(im)
    def txt(x, y, text, size=20, color=WHITE, bold=False):
        d.text((x, y), text, font=FONTS[size, bold], fill=color)
    def box(bounds, fill=PANEL, radius=16, outline=None):
        d.rounded_rectangle(bounds, radius=radius, fill=fill, outline=outline, width=2)
    box((40, 28, 74, 62), BLUE, 9)
    txt(49, 32, 'D', 24, bold=True)
    txt(86, 31, 'Driveline', 28, bold=True)
    box((936, 30, 1240, 62), '#25354C', 16)
    txt(955, 38, 'SIMULATION  /  FICTIONAL DATA', 16, MUTED, True)
    txt(40, 94, title, 40, bold=True)
    txt(41, 149, subtitle, 22, MUTED)

    # Campus diagram and a smoothly advancing car.
    box((40, 202, 714, 563), '#15243A')
    txt(64, 222, 'MAPLE GROVE SCHOOL', 16, MUTED, True)
    d.ellipse((244, 256, 666, 530), fill='#173A47', outline='#28645D', width=2)
    txt(281, 281, 'NEAR-SCHOOL ZONE', 14, GREEN, True)
    box((407, 319, 634, 410), '#334966', 8)
    d.polygon([(389, 320), (521, 269), (651, 320)], fill='#496284')
    box((487, 310, 557, 332), '#E2E8F0', 4)
    txt(496, 314, 'SCHOOL', 14, NAVY, True)
    for wx in (429, 470, 551, 592):
        box((wx, 349, wx+24, 373), '#7DD3FC', 3)
    box((509, 363, 537, 410), '#0F172A', 3)
    d.line((65, 465, 689, 465), fill='#475569', width=64)
    for x in range(70, 690, 48):
        d.line((x, 465, x+24, 465), fill='#94A3B8', width=2)
    txt(506, 513, 'PICKUP CURB', 14, MUTED, True)
    xs = [104 + 196*ease(u), 300, 300+55*ease(u), 355+115*ease(u), 470, 470+235*ease(u)]
    cx = xs[scene]
    if scene == 2:
        for gx in (450, 561):
            box((gx-28, 443, gx+28, 484), '#64748B', 8)
    if scene in (3, 4):
        for j in range(2):
            px, py = 545+j*29, 424 + (12*ease(u) if scene == 4 else 0)
            d.ellipse((px-5, py-7, px+5, py+3), fill=GREEN)
            d.line((px, py+3, px, py+15), fill=GREEN, width=4)
    box((cx-35, 442, cx+35, 484), BLUE, 10)
    box((cx-12, 446, cx+15, 479), '#BFDBFE', 5)
    for dx in (-23, 21):
        box((cx+dx-5, 437, cx+dx+5, 446), '#020617', 3)
        box((cx+dx-5, 479, cx+dx+5, 489), '#020617', 3)
    if scene < 5:
        box((cx-33, 493, cx+34, 516), '#2563EB', 6)
        txt(cx-20, 496, '1800', 16, bold=True)
    txt(65, 532, 'Illustrative campus layout', 14, MUTED)

    if scene in (0, 1):
        # A fictional parent and readable phone UI make the check-in action explicit.
        box((738, 202, 1240, 563), PANEL)
        txt(757, 224, 'PARENT / GUARDIAN', 14, '#60A5FA', True)
        # Parent portrait; the touch indicator below depicts interaction while parked.
        d.ellipse((783, 279, 837, 337), fill='#DCA882')
        d.pieslice((779, 269, 840, 320), 180, 355, fill='#302A35')
        d.ellipse((793, 303, 797, 307), fill=NAVY)
        d.ellipse((821, 303, 825, 307), fill=NAVY)
        d.arc((800, 308, 819, 322), 10, 165, fill='#704330', width=2)
        box((800, 329, 822, 349), '#DCA882', 6)
        box((771, 344, 850, 412), '#2563EB', 26)
        txt(780, 423, 'Jordan', 22, bold=True)
        txt(770, 452, 'Family 1800', 16, MUTED)
        step = 'Approaching' if scene == 0 else ('Select children' if u < .43 else 'Tap Check in' if u < .58 else 'Checking...' if u < .70 else 'You are checked in')
        txt(755, 495, step, 16, GREEN if scene == 1 and u >= .70 else WHITE, True)
        txt(755, 525, 'Parked to check in' if scene == 1 else 'Already signed in', 14, MUTED)

        # Phone chassis, screen, and familiar native-app affordances.
        box((927, 189, 1221, 572), '#020617', 30, '#475569')
        box((939, 201, 1209, 560), '#F8FAFC', 22)
        box((1038, 206, 1110, 214), '#020617', 4)
        txt(954, 226, 'Driveline', 22, '#0F172A', True)
        txt(1160, 233, '2:50', 14, '#64748B')
        txt(954, 260, 'Maple Grove School', 16, '#334155', True)
        txt(954, 282, 'Signed in / MFA verified', 14, '#64748B')
        in_zone = scene == 1 or u > .78
        box((951, 307, 1197, 333), '#DCFCE7' if in_zone else '#E2E8F0', 7)
        txt(961, 313, 'Near school / Ready' if in_zone else 'Waiting for near-school presence', 14, '#166534' if in_zone else '#475569', True)
        confirmed = scene == 1 and u >= .70
        if confirmed:
            d.ellipse((1048, 352, 1098, 402), fill='#10B981')
            d.line([(1060, 377), (1070, 386), (1087, 366)], fill='white', width=4)
            txt(984, 412, 'You are checked in', 22, '#0F172A', True)
            txt(967, 443, 'Alex + Sam / Family 1800', 18, '#475569')
            box((954, 476, 1194, 516), '#DBEAFE', 9)
            txt(986, 487, 'Queue position: 03', 20, '#1D4ED8', True)
            txt(979, 526, 'Please remain in your car', 14, '#64748B')
        else:
            for j, name in enumerate(('Alex Taylor', 'Sam Taylor')):
                y = 343+j*58
                selected = scene == 1 and u >= (.15 if j == 0 else .34)
                box((951, y, 1197, y+51), '#EFF6FF' if selected else '#FFFFFF', 8, '#93C5FD' if selected else '#CBD5E1')
                txt(963, y+6, name, 18, '#0F172A', True)
                txt(963, y+29, f'1800/{j+1}  /  Eligible for pickup', 14, '#64748B')
                box((1167, y+10, 1187, y+30), '#2563EB' if selected else '#FFFFFF', 4, '#2563EB' if selected else '#94A3B8')
                if selected:
                    d.line([(1171, y+20), (1176, y+25), (1183, y+15)], fill='white', width=2)
            ready = scene == 1 and u >= .34
            checking = scene == 1 and u >= .58
            box((953, 476, 1195, 519), '#2563EB' if ready else '#CBD5E1', 10)
            button = 'Verifying arrival...' if checking else 'Check in (2 children)' if ready else 'Select your children' if scene == 1 else 'Check in near school'
            txt(969, 489, button, 18, '#FFFFFF' if ready else '#64748B', True)
            txt(980, 535, 'One check-in for both children', 14, '#64748B')

        # Moving fingertip and expanding touch rings demonstrate the actual taps.
        if scene == 1 and u < .60:
            beats = [(0.15, 1177, 363), (.34, 1177, 421), (.56, 1077, 497)]
            for beat, tx, ty in beats:
                dt = u-beat
                if -.09 <= dt <= .065:
                    approach = ease((dt+.09)/.09)
                    fx, fy = tx+22*(1-approach), ty+30*(1-approach)
                    if dt >= 0:
                        radius = 9+dt*270
                        d.ellipse((tx-radius, ty-radius, tx+radius, ty+radius), outline='#60A5FA', width=3)
                    # A fingertip, palm, and blue cuff; keep tap targets visible.
                    box((fx+5, fy+22, fx+39, fy+63), '#DCA882', 12, '#B77F59')
                    box((fx-6, fy, fx+8, fy+44), '#EBC19E', 7, '#B77F59')
                    box((fx+6, fy+55, fx+42, fy+70), '#2563EB', 4)
                    break
        box((1040, 551, 1109, 555), '#64748B', 2)
    else:
        box((738, 202, 1240, 563), PANEL)
        txt(764, 224, role, 14, '#60A5FA', True)
        txt(764, 256, heading, 28, bold=True)
        txt(764, 297, detail, 18, MUTED)
        for i, row in enumerate(rows):
            y = 339+i*52
            box((762, y, 1216, y+42), '#28384F', 8)
            d.ellipse((777, y+16, 787, y+26), fill=GREEN if scene != 2 or i == 2 else MUTED)
            txt(800, y+11, row, 18)
        status = ['Approaching school', 'Check in with selected children', 'Arrival accepted  /  position 03',
                  'Classroom call acknowledged', 'Confirm handoff', 'Handoff recorded'][scene]
        if scene == 1 and u > .52:
            status = 'Check-in accepted'
        if scene == 4 and u > .62:
            status = 'Staff confirmed handoff'
        box((762, 507, 1216, 544), '#12574C' if scene == 5 or (scene in (1,4) and u > .62) else '#2563EB', 8)
        txt(781, 516, status, 18, bold=True)
    txt(40, 590, caption, 20, '#E2E8F0')
    labels = ['Approach', 'Check in', 'Queue', 'Call', 'Handoff', 'Record']
    for i, label in enumerate(labels):
        x = 40+i*202
        box((x, 640, x+187, 644), '#334155', 2)
        if i <= scene:
            end = x+187*(u if i == scene else 1)
            if end > x+2:
                box((x, 640, end, 644), GREEN if i < scene else BLUE, 2)
        txt(x, 658, f'0{i+1}  {label}', 16, WHITE if i == scene else MUTED, i == scene)
    # Short fades between chapters keep transitions gentle without hiding labels for long.
    fade = min(1, (t % 8)/.25) if scene else min(1, t/.4)
    if fade < 1:
        im = Image.blend(Image.new('RGB', im.size, NAVY), im, fade)
    return im

if __name__ == '__main__':
    fps, seconds = 24, 48
    target = OUT / 'driveline-simulation-demo.mp4'
    command = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-vcodec', 'rawvideo',
               '-pix_fmt', 'rgb24', '-s', '1280x720', '-r', str(fps), '-i', '-', '-an',
               '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p',
               '-movflags', '+faststart', str(target)]
    proc = subprocess.Popen(command, stdin=subprocess.PIPE)
    try:
        for n in range(fps*seconds):
            proc.stdin.write(frame(n/fps).tobytes())
        proc.stdin.close()
        if proc.wait() != 0:
            raise RuntimeError('ffmpeg failed')
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait()
    frame(14.5).save(OUT / 'driveline-simulation-poster.jpg', quality=92)
    print(target)
