---
name: "computer-vision"
description: "Builds computer vision pipelines: image preprocessing with OpenCV, detection with YOLO, and video analysis with ffmpeg. Use when working with image processing or when the user mentions image processing."
type: knowledge
triggers: ["computer-vision", "image-processing"]
---

Builds computer vision pipelines: image preprocessing with OpenCV, detection with YOLO, and video analysis with ffmpeg.

## Agentic Workflow: Read -> Reason -> Act (computer-vision)

You are **computer-vision** (ai) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — ai context for `computer-vision`
- Domain: Builds computer vision pipelines: image preprocessing with OpenCV, detection with YOLO, and video analysis with ffmpeg.
- **image-processing**: Preprocess images and video with OpenCV and ffmpeg — `python -c "import cv2; print(cv2.__version__)"`
- Check `knowledge` and `prerequisites: python, opencv, tensorflow, pytorch`

### 2. Reason — think for `computer-vision`
- For `image-processing`: Preprocess images and video with OpenCV and ffmpeg — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `computer-vision` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Ffmpeg` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `computer-vision:fa1ed5f6`

# Computer Vision

Builds CV systems: image preprocessing (OpenCV), object detection (YOLO), and video
pipelines (ffmpeg).

## When to Use

- Preprocessing a dataset before training a detector
- Running detection on images, video files, or RTSP streams
- Extracting frames and creating datasets from video

## Real Commands

```bash
# Verify the stack
python -c "import cv2; print(cv2.__version__)"

# Extract one frame per second from video
ffmpeg -i input.mp4 -vf "fps=1" frames/frame_%04d.jpg

# Resize and normalize a dataset
python -c "
import cv2, glob
for f in glob.glob('raw/*.jpg'):
    img = cv2.imread(f)
    img = cv2.resize(img, (640, 640))
    cv2.imwrite('proc/' + f.split('\\')[-1], img)
"

# Run YOLO detection
python detect.py --source images/ --weights best.pt --conf 0.4 --save-txt

# Export to ONNX for edge deployment
python export.py --weights best.pt --include onnx
```

## Dataset Prep

```bash
# Crop to square and save 100 frames
ffmpeg -i video.mp4 -vf "crop=640:640:0:0" -frames:v 100 crop/%05d.jpg

# Augment with flip/rotation
python augment.py --folder train/ --flip --rotate 10 --brightness 0.2
```

## Best Practices

- Normalize (resize + RGB) identically for train and inference
- Use augmentation to avoid overfitting on small datasets
- Test on edge cases: blur, occlusion, low light
- Benchmark FPS after quantization/export
- Keep class balance in the dataset

## Example Response

The agent produces a preprocessing command sequence, runs detection, and returns
class counts, confidence stats, and per-image annotated outputs.

## Capabilities

### image-processing
Preprocess images and video with OpenCV and ffmpeg

**Parameters:**
- `source` (string): Image, video, directory, or stream URL to process
- `save-txt` (boolean): Write detection results as YOLO-format txt files
- `weights` (string): Path to trained model weights, e.g. best.pt

**Commands:**
- `python -c "import cv2; print(cv2.__version__)"`
- `python -m pip install opencv-python pillow`
- `ffmpeg -i input.mp4 -vf "fps=1" frames/frame_%04d.jpg`
- `python -c "import cv2; img=cv2.imread('a.jpg'); cv2.resize(img,(640,640)); cv2.imwrite('r.jpg',img)"`
- `ffmpeg -i input.mp4 -vf scale=320:320 -c:v libx264 out.mp4`

**Examples:**
- ffmpeg -i video.mp4 -vf "crop=640:640:0:0" -frames:v 100 crop/%05d.jpg
- python augment.py --folder train/ --flip --rotate 10
- python detect.py --source rtsp://cam:554/stream --save-txt

## References
- [OpenCV docs](https://docs.opencv.org/)
- [Ultralytics YOLO docs](https://docs.ultralytics.com/)
- [ffmpeg documentation](https://ffmpeg.org/documentation.html)
