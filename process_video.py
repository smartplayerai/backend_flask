import cv2
import numpy as np

def process_cricket_video(video_path):
    cap = cv2.VideoCapture(video_path)
    
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Define color range for ball detection
    lower_pink = np.array([160, 30, 50])
    upper_pink = np.array([180, 255, 255])

    output_path = "output.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_pink, upper_pink)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            if len(largest_contour) >= 5:
                (cx, cy), r = cv2.minEnclosingCircle(largest_contour)
                center = (int(cx), int(cy))
                if mask[center[1], center[0]] > 0:
                    cv2.circle(frame, center, int(r), (8, 255, 8), 2)

        out.write(frame)

    cap.release()
    out.release()

    return output_path