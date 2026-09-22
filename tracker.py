
import cv2
import time


# Create the CSRT object tracker
def create_tracker():
    if hasattr(cv2, "TrackerCSRT_create"):
        return cv2.TrackerCSRT_create()
    return cv2.legacy.TrackerCSRT_create()

# Let the user select an object using a bounding box
def select_object(frame):
    box = cv2.selectROI("Select Object", frame, False)
    cv2.destroyWindow("Select Object")

    # Return None if no object was selected
    if box[2] == 0 or box[3] == 0:
        return None

    return box

def main():
    # Open the webcam
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not camera.isOpened():
        print("Could not open camera")
        return

    # Set the camera resolution
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Initialize tracking variables
    tracker = None
    tracking = False
    fps = 0
    last_time = time.perf_counter()

    try:
        # Capture the first frame
        ret, frame = camera.read()

        if not ret:
            return

        # Select the object to track
        box = select_object(frame)

        if box is None:
            return

        # Initialize the tracker with the selected object
        tracker = create_tracker()
        tracker.init(frame, box)
        tracking = True

        # Process webcam frames continuously
        while True:
            ret, frame = camera.read()

            if not ret:
                break

            # Calculate and smooth the FPS
            now = time.perf_counter()
            elapsed = now - last_time
            last_time = now

            if elapsed > 0:
                current_fps = 1 / elapsed
                fps = current_fps if fps == 0 else 0.9 * fps + 0.1 * current_fps

            # Update the object's position
            if tracking:
                success, box = tracker.update(frame)

                if success:
                    x, y, w, h = map(int, box)

                    # Draw a green box around the tracked object
                    cv2.rectangle(
                        frame, (x, y), (x + w, y + h),
                        (0, 255, 0), 2
                    )

                    # Display the tracking status
                    cv2.putText(
                        frame, "TRACKING", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 255, 0), 2
                    )

                else:
                    # Stop tracking if the object is lost
                    tracking = False
                    tracker = None

            # Display a warning when tracking fails
            if not tracking:
                cv2.putText(
                    frame, "TRACKING LOST", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (0, 0, 255), 2
                )

            # Display the current FPS
            cv2.putText(
                frame, f"FPS: {fps:.1f}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (255, 255, 255), 2
            )

            # Display keyboard controls
            cv2.putText(
                frame, "R: Reselect | Q: Quit", (20, 460),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                (255, 255, 255), 2
            )

            # Show the live video
            cv2.imshow("Object Tracker", frame)

            key = cv2.waitKey(1) & 0xFF

            # Press Q to quit
            if key == ord("q"):
                break

            # Press R to select another object
            elif key == ord("r"):
                ret, new_frame = camera.read()

                if not ret:
                    continue

                new_box = select_object(new_frame)

                if new_box is not None:
                    # Initialize a new tracker
                    tracker = create_tracker()
                    tracker.init(new_frame, new_box)
                    tracking = True

                # Reset FPS after object selection
                last_time = time.perf_counter()
                fps = 0
                
    finally:
        # Release the webcam and close all windows
        camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()