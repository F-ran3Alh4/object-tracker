
# Real-Time Object Tracker

A real-time object tracking application developed using Python and OpenCV.

The application allows the user to select a specific object from a live webcam frame using a bounding box. The program then tracks the selected object using the CSRT (Discriminative Correlation Filter with Channel and Spatial Reliability) algorithm.

The application displays the tracking results, bounding box, tracking status, and approximate FPS in a live video window.

## 1. Requirements

- Python 3
- OpenCV (opencv-contrib-python)
- A working webcam

## 2. Installation

### Step 1: Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/F-ran3Alh4/object-tracker.git
cd object-tracker
```

### Step 2: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 3: Activate the Virtual Environment

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 4: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

## 3. How to Run

Run the Python file:

```bash
python tracker.py
```

After running the program:

1. The webcam starts and captures the first frame.
2. A selection window appears.
3. Select an object by drawing a bounding box using the mouse.
4. Press ENTER or SPACE to confirm the selection.
5. The program starts tracking the selected object.
6. Move the object in front of the webcam to observe the tracking results.

### Keyboard Controls

| Key | Action |
|-----|--------|
| R | Reselect an object |
| Q | Quit the program |
| ENTER / SPACE | Confirm the bounding box |
| C | Cancel the bounding box selection |

## 4. Implementation Details

The application uses OpenCV to capture live video from the webcam.

The user selects an object using `cv2.selectROI()`. The selected bounding box is used to initialize the CSRT tracker.

For each new frame, `tracker.update()` estimates the object's position.

When tracking succeeds, a green rectangle is drawn around the estimated object location, and the program displays "TRACKING".

When the tracker reports failure, the program displays "TRACKING LOST".

The application also calculates the approximate FPS using `time.perf_counter()`.

The user can press R to manually select the object again and initialize a new tracker.

## 5. Detailed Code Explanation

### 5.1 Importing Libraries

```python
import cv2
import time
```

The `cv2` library is used for computer vision operations.

In this project, it handles the webcam, object selection, CSRT tracking, bounding box drawing, and live video display.

The `time` library is used to calculate the video processing speed, measured in Frames Per Second (FPS).

### 5.2 Creating the CSRT Tracker

```python
def create_tracker():
    if hasattr(cv2, "TrackerCSRT_create"):
        return cv2.TrackerCSRT_create()
    return cv2.legacy.TrackerCSRT_create()
```

The `create_tracker()` function creates a new CSRT tracker.

The `hasattr()` function checks whether OpenCV contains `TrackerCSRT_create`.

This check is necessary because the location of the CSRT creation function differs between some OpenCV versions.

If the function is available directly under `cv2`, the program uses it.

Otherwise, the program attempts to create the tracker using the older `cv2.legacy` interface.

### 5.3 Selecting the Object

```python
def select_object(frame):
    box = cv2.selectROI("Select Object", frame, False)
    cv2.destroyWindow("Select Object")

    if box[2] == 0 or box[3] == 0:
        return None

    return box
```

The `select_object()` function receives a frame from the webcam.

The `cv2.selectROI()` function opens a window that allows the user to draw a rectangle around the target object.

The parameters are:

| Parameter | Description |
|-----------|-------------|
| "Select Object" | Name of the selection window |
| frame | The image used for object selection |
| False | Starts drawing the rectangle from a corner instead of its center |

After confirming the selection, the function returns four values:

`(x, y, w, h)`

- `x`: Horizontal position of the top-left corner.
- `y`: Vertical position of the top-left corner.
- `w`: Width of the bounding box.
- `h`: Height of the bounding box.

The `cv2.destroyWindow()` function closes the selection window.

If the width or height is zero, the function returns `None`, indicating that no valid object was selected.

Otherwise, the bounding box is returned.

### 5.4 Initializing the Webcam

```python
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
```

The `cv2.VideoCapture()` function opens the webcam.

The value `0` refers to the default camera.

`cv2.CAP_DSHOW` specifies the Windows DirectShow backend.

The program checks whether the camera opened successfully:

```python
if not camera.isOpened():
    print("Could not open camera")
    return
```

If the camera cannot be opened, the program displays an error message and exits the main function.

### 5.5 Setting the Camera Resolution

```python
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
```

The program requests a camera resolution of 640 × 480 pixels.

This resolution contains 307,200 pixels per frame.

Using a moderate resolution can reduce the amount of image data processed by the tracker.

The actual resolution depends on the camera and its supported settings.

### 5.6 Initializing Variables

```python
tracker = None
tracking = False
fps = 0
last_time = time.perf_counter()
```

The program initializes four variables:

| Variable | Description |
|----------|-------------|
| tracker | Stores the CSRT tracker object |
| tracking | Indicates whether tracking is active |
| fps | Stores the calculated frame rate |
| last_time | Stores the previous timing measurement |

The `time.perf_counter()` function provides a high-resolution timer suitable for measuring short time intervals.

### 5.7 Reading the First Frame

```python
ret, frame = camera.read()

if not ret:
    return
```

The `camera.read()` function captures a frame from the webcam.

It returns two values:

- `ret`: A Boolean indicating whether the frame was captured successfully.
- `frame`: The captured image.

If the frame cannot be read, the program exits the main function.

### 5.8 Initializing Object Tracking

```python
box = select_object(frame)

if box is None:
    return

tracker = create_tracker()
tracker.init(frame, box)
tracking = True
```

The user selects an object from the first frame.

If no valid bounding box is selected, the program exits.

Otherwise, a CSRT tracker is created.

The `tracker.init()` function initializes the tracker using the first frame and the selected bounding box.

The `tracking` variable is then set to `True` to indicate that tracking is active.

### 5.9 Processing Live Video

```python
while True:
    ret, frame = camera.read()

    if not ret:
        break
```

The `while True` loop continuously processes frames from the webcam.

For every iteration, the program captures a new frame.

If the frame cannot be read, the loop stops.

### 5.10 Calculating FPS

```python
now = time.perf_counter()
elapsed = now - last_time
last_time = now
```

The program records the current time and calculates the elapsed time since the previous measurement.

The frame rate is calculated using:

`FPS = 1 / elapsed`

The program also uses an exponential moving average:

```python
if elapsed > 0:
    current_fps = 1 / elapsed
    fps = current_fps if fps == 0 else 0.9 * fps + 0.1 * current_fps
```

This calculation smooths the displayed FPS value and reduces sudden fluctuations.

The displayed FPS estimates the frame-processing loop rate rather than measuring only the execution time of the CSRT algorithm.

### 5.11 Updating the Tracker

```python
if tracking:
    success, box = tracker.update(frame)
```

The program checks whether tracking is active.

The `tracker.update()` function processes the current frame and estimates the new position of the selected object.

It returns:

- `success`: Indicates whether the tracker reports successful tracking.
- `box`: Contains the estimated bounding box coordinates.

If tracking succeeds, the program updates the bounding box.

### 5.12 Drawing the Bounding Box

```python
if success:
    x, y, w, h = map(int, box)

    cv2.rectangle(
        frame, (x, y), (x + w, y + h),
        (0, 255, 0), 2
    )
```

The program converts the bounding box coordinates into integers.

The `cv2.rectangle()` function draws a green rectangle around the estimated object location.

The coordinates `(x, y)` represent the top-left corner.

The coordinates `(x + w, y + h)` represent the bottom-right corner.

The color `(0, 255, 0)` represents green in OpenCV's BGR color format.

The value `2` specifies the rectangle's line thickness.

### 5.13 Displaying the Tracking Status

```python
cv2.putText(
    frame, "TRACKING", (20, 40),
    cv2.FONT_HERSHEY_SIMPLEX, 0.8,
    (0, 255, 0), 2
)
```

The `cv2.putText()` function displays text on the video frame.

When tracking succeeds, the program displays "TRACKING" in green.

If the tracker reports failure:

```python
else:
    tracking = False
    tracker = None
```

The program stops tracking and clears the tracker reference.

It then displays "TRACKING LOST" in red.

The tracking status reflects the tracker's reported result and does not guarantee that the correct object is still being tracked.

### 5.14 Displaying FPS and Keyboard Instructions

The program uses `cv2.putText()` to display the approximate FPS.

```python
cv2.putText(
    frame, f"FPS: {fps:.1f}", (20, 80),
    cv2.FONT_HERSHEY_SIMPLEX, 0.7,
    (255, 255, 255), 2
)
```

The expression `{fps:.1f}` formats the FPS value to one decimal place.

The program also displays the keyboard instructions:

`R: Reselect | Q: Quit`

### 5.15 Displaying the Live Video

```python
cv2.imshow("Object Tracker", frame)
```

The `cv2.imshow()` function displays the current frame in a window named "Object Tracker".

The displayed frame includes the bounding box, tracking status, FPS, and keyboard instructions.

### 5.16 Handling Keyboard Input

```python
key = cv2.waitKey(1) & 0xFF
```

The program checks for keyboard input while processing window events.

If the user presses Q, the program exits the main loop.

```python
if key == ord("q"):
    break
```

If the user presses R, the program captures a new frame and opens the object selection window again.

```python
elif key == ord("r"):
    ret, new_frame = camera.read()

    if not ret:
        continue

    new_box = select_object(new_frame)
```

If a valid object is selected, the program creates and initializes a new CSRT tracker.

```python
if new_box is not None:
    tracker = create_tracker()
    tracker.init(new_frame, new_box)
    tracking = True
```

The program also resets the FPS calculation after reselection:

```python
last_time = time.perf_counter()
fps = 0
```

This prevents the time spent selecting the object from affecting the subsequent FPS calculation.

### 5.17 Releasing Resources

```python
finally:
    camera.release()
    cv2.destroyAllWindows()
```

The `finally` block ensures that the webcam is released and OpenCV windows are closed when execution leaves the `try` block.

The program starts by calling the `main()` function:

```python
if __name__ == "__main__":
    main()
```

This ensures that `main()` runs when the Python file is executed directly.

## 6. Testing and Performance

The application was tested using a live webcam.

| Test | Result |
|------|--------|
| Slow movement | Successful |
| Fast movement | Successful |
| Distance changes | Successful |
| Manual reselection | Successful |
| Observed FPS | Approximately 20 |

The tracker successfully followed the selected object during slow movement, fast movement, and changes in distance.

The application also supported manual object reselection using the R key.

The observed processing performance was approximately 20 FPS during testing.

Performance may vary depending on the computer, webcam, lighting, and object movement.

