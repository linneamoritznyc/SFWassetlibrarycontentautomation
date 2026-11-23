import subprocess, glob, os, shutil
import numpy as np
from PIL import Image
from pptx import Presentation
from pptx.util import Emu
PX = 9525
F = '23-11-2026-cic-student-voices-v27.pptx'
def render(path):
    shutil.rmtree('cr', ignore_errors=True); os.makedirs('cr'); shutil.copy(path, 'cr/a.pptx')
    subprocess.run('cd cr && timeout 200 soffice --headless --convert-to pdf a.pptx >/dev/null 2>&1 && pdftoppm -r 96 -png a.pdf a', shell=True)
    return [np.asarray(Image.open(f).convert('RGB')).astype(int) for f in sorted(glob.glob('cr/a-*.png'))]
def measure(img, frame_top, frame_bot, left, right):
    sx = img.shape[1] / 1080
    a = img[int(frame_top * sx) + 8:int(frame_bot * sx) - 8, int(left * sx) + 60:int((left + (right - left) * 0.55) * sx)]
    bright = (a.max(axis=2) > 150) & ((a.max(axis=2) - a.min(axis=2)) < 120)
    rows = np.where(bright.sum(axis=1) > 14)[0]
    return (rows[0] + int(frame_top * sx) + 8) / sx, (rows[-1] + int(frame_top * sx) + 8) / sx
