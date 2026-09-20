# computer-vision

Builds computer vision pipelines: image preprocessing with OpenCV, detection with YOLO, and video analysis with ffmpeg.

## Instructions

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