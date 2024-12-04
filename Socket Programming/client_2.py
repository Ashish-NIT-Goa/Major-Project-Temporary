import cv2
from ultralytics import YOLO, solutions
import socket

model = YOLO(r"..\models\yolo11m.pt")

cap = cv2.VideoCapture(r"videos\traffic_camera_ongoing.mp4")
assert cap.isOpened(), "Error reading video file"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))


# Define line points
# line_points = [(85, 227), (385, 219)] # Init Object Counter
line_points = [(158, 624), (486, 624)] # Init Object Counter for traffic camera ongoing

# Init Object Counter
counter = solutions.ObjectCounter(
    show=True,
    region=line_points,
    model=r"..\models\yolo11m.pt",
    line_width=1,
    draw_tracks=False,
    show_out=False,
    classes = [2, 5, 7]
)

host = 'LAPTOP-ASHISH'  # Replace with the server's IP address
port = 12345  # The same port as the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))


previous_message = ""
while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        break
    im0 = counter.count(im0)
    current_message = str(counter.classwise_counts)
    # video_writer.write(im0)
    # Check if the serialized message has changed
    if current_message != previous_message:
        client_socket.sendall(current_message.encode())
        print(f"Sent to server: {current_message}")
        previous_message = current_message
        # Receive response from the server
        response = client_socket.recv(1024)
        print(f"Server response: {response.decode()}")
    else:
        print("No change in count")

cap.release()
# video_writer.release()
cv2.destroyAllWindows()