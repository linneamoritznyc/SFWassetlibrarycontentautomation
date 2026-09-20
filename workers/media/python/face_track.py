"""
Where the speaker is, twice a second.

Samples the video, finds the largest face in each sample, and prints a JSON
track of horizontal centres. The TypeScript side smooths it and turns it into
an ffmpeg crop expression, so this stays a single job: look, and say what you
saw.

A frame with no face gets a null. Half a workshop video is someone's hands in
compost, and pretending to know where a face is would be worse than saying
nothing: the smoother holds the last known position instead.

    python3 face_track.py VIDEO [--start 12.5] [--duration 40] [--every 0.5]
"""

import argparse
import json
import os
import sys

try:
    import cv2
except ImportError:  # pragma: no cover
    print(json.dumps({"error": "opencv is not installed in this image"}), file=sys.stderr)
    sys.exit(2)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    parser.add_argument("--start", type=float, default=0.0)
    parser.add_argument("--duration", type=float, default=0.0)
    parser.add_argument("--every", type=float, default=0.5)
    args = parser.parse_args()

    cascade_path = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")
    if not os.path.exists(cascade_path):
        print(json.dumps({"error": "no face cascade in this opencv build"}), file=sys.stderr)
        return 2

    cascade = cv2.CascadeClassifier(cascade_path)
    capture = cv2.VideoCapture(args.video)
    if not capture.isOpened():
        print(json.dumps({"error": "could not open the video"}), file=sys.stderr)
        return 2

    fps = capture.get(cv2.CAP_PROP_FPS) or 25.0
    frames = capture.get(cv2.CAP_PROP_FRAME_COUNT) or 0
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    end = args.start + args.duration if args.duration > 0 else (frames / fps if fps else 0)
    samples = []
    t = args.start

    while t < end:
        capture.set(cv2.CAP_PROP_POS_MSEC, t * 1000.0)
        ok, frame = capture.read()
        if not ok:
            break

        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        grey = cv2.equalizeHist(grey)

        # Faces smaller than a twelfth of the frame are usually someone in the
        # background, not the speaker.
        minimum = max(40, height // 12)
        faces = cascade.detectMultiScale(
            grey, scaleFactor=1.15, minNeighbors=6, minSize=(minimum, minimum)
        )

        if len(faces) > 0:
            # The largest face is the one nearest the camera, which is the one
            # talking in nearly every workshop shot.
            x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
            samples.append({"t": round(t, 3), "x": int(x + w / 2), "confidence": float(w * h) / (width * height)})
        else:
            samples.append({"t": round(t, 3), "x": None, "confidence": 0.0})

        t += args.every

    capture.release()

    print(json.dumps({"width": width, "height": height, "fps": fps, "samples": samples}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
