import socket
import cv2
import time
from ultralytics import YOLO, solutions
import threading
from queue import Queue

def read_frames(cap, frame_queue):
    while True:
        success, frame = cap.read()
        if not success:
            break
        frame_queue.put(frame)

def start_client():
    host = 'LAPTOP-ASHISH'  # Replace with the server's IP address
    port = 12345  # The same port as the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    model = YOLO(r"..\models\yolov10m.pt")
    cap = cv2.VideoCapture(r"D:\Major Project\videos\vehicle_counting_2.mp4")
    assert cap.isOpened(), "Error reading video file"

    line_points = [(20, 400), (1080, 400)]
    counter = solutions.ObjectCounter(
        show=True,
        region=line_points,
        model=r"..\models\yolo11m.pt",
        line_width=1,
        draw_tracks=False,
)

    frame_queue = Queue(maxsize=10)
    threading.Thread(target=read_frames, args=(cap, frame_queue)).start()
    previous_message = ""

    try:
        while True:
            if not frame_queue.empty():
                im0 = frame_queue.get()
                tracks = model.track(im0, persist=True, show=False)
                im0 = counter.count(im0)

                # Serialize the current count
                current_message = str(counter.classwise_counts)

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

                time.sleep(0.1)  # Small delay to allow for frame processing

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cap.release()
        cv2.destroyAllWindows()
        client_socket.close()

if __name__ == "__main__":
    start_client()