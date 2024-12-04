import cv2
from ultralytics import YOLO, solutions
import socket
import threading
import queue

model = YOLO(r"..\models\yolo11m.pt")

cap = cv2.VideoCapture(r"videos\traffic_camera_ongoing.mp4")
assert cap.isOpened(), "Error reading video file"

line_points = [(158, 624), (486, 624)]

counter = solutions.ObjectCounter(
    show=True,
    region=line_points,
    model=r"..\models\yolo11m.pt",
    line_width=1,
    draw_tracks=False,
    show_out=False,
    classes=[2, 5, 7]
)

host = 'LAPTOP-ASHISH'
port = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

lane_id = "Lane_1"
message_queue = queue.Queue()

def handle_server_communication(sock, queue):
    global previous_signal
    try:
        while True:
            if not queue.empty():
                message = queue.get()
                try:
                    sock.sendall(message.encode())
                    print(f"Sent to server: {message}")
                except Exception as e:
                    print(f"Error sending data to server: {e}")
                    break

            try:
                response = sock.recv(1024).decode()
                if response != previous_signal:
                    print(f"Traffic light status for {lane_id}: {response}")
                    previous_signal = response
            except Exception as e:
                print(f"Error receiving server response: {e}")
                break
    except Exception as e:
        print(f"Communication thread error: {e}")
    finally:
        print("Closing socket")
        sock.close()

communication_thread = threading.Thread(target=handle_server_communication, args=(client_socket, message_queue))
communication_thread.daemon = True
communication_thread.start()

previous_density = None

try:
    while cap.isOpened():
        success, im0 = cap.read()
        if not success:
            print("Video processing completed.")
            break
        
        try:
            im0 = counter.count(im0)
        except Exception as e:
            print(f"Error during counting: {e}")
            break

        current_density = sum(vehicle_data['IN'] for vehicle_data in counter.classwise_counts.values())
        
        if current_density != previous_density:
            message_queue.put(f"{lane_id}:{current_density}")
            previous_density = current_density

except KeyboardInterrupt:
    print("Client stopped manually.")
finally:
    cap.release()
    client_socket.close()
    print("Connection closed.")
