
import supervision as sv
import cv2

VIDEO = r"videos\crowded_road_crossing.mp4"

video_info = sv.VideoInfo.from_video_path(VIDEO)
generator = sv.get_video_frames_generator(VIDEO)
iterator = iter(generator)

frame = next(iterator) # First fame of the video

cv2.imwrite(r"images\first_frame_crowded_road_corssing.png", frame) # save first frame