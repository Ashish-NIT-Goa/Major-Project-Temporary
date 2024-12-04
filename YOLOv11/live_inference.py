from ultralytics import solutions

# Pass a model as an argument
solutions.inference(model="..\models\yolo11m.pt")

### Make sure to run the file using command `streamlit run <file-name.py>`