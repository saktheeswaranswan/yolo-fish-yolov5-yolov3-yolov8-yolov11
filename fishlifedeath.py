import cv2
import torch
import csv
import os

# Load your custom YOLOv5 model from best.pt
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)

# Specify the video file path and CSV output filename
video_path = "video.mp4"  # Replace with your MP4 file path
output_csv = "detections.csv"

# Create or overwrite the CSV file with header row
with open(output_csv, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["frame", "class", "confidence", "xmin", "ymin", "xmax", "ymax"])

# Open video capture
cap = cv2.VideoCapture(video_path)
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break  # End of video

    frame_count += 1

    # Run inference on the current frame
    results = model(frame)
    # results.xyxy[0] contains detections in [xmin, ymin, xmax, ymax, confidence, class] format
    detections = results.xyxy[0].cpu().numpy()

    # Append detections to the CSV file
    with open(output_csv, mode="a", newline="") as f:
        writer = csv.writer(f)
        for det in detections:
            xmin, ymin, xmax, ymax, conf, cls = det
            class_name = model.names[int(cls)]
            writer.writerow([frame_count, class_name, f"{conf:.2f}", int(xmin), int(ymin), int(xmax), int(ymax)])

    # OPTIONAL: Visualize detections on the frame
    for det in detections:
        xmin, ymin, xmax, ymax, conf, cls = det
        label = f"{model.names[int(cls)]} {conf:.2f}"
        cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)
        cv2.putText(frame, label, (int(xmin), int(ymin) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
