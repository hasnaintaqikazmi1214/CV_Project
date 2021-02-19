# CV_Project
Deep Mask Monitoring

# Run Code by command

python3 main.py -i input/market.mp4 -o output/output.avi -y yolo-coco

# Social Distancing

A Social Distance Monitoring Tool using OpenCV.

# Description

Firstly humans are identified in a video stream using YOLO(You Only Look Once)- a special kind of Convolutional Neural Network. 

P.S.- Due to the large size of yolo.weights file it could not be uploaded. It can be downloaded from https://pjreddie.com/media/files/yolov3.weights

Each person detected is bounded by a rectangular box in order to locate the person.

The camera perspective is transformed to a bird-eye view (top down) for effectively computing euclidean distance between people.

The surrounding boxes are classified as follows-

1) Red-High Risk

2) Yellow-Medium Risk

3) Green-Low Risk

Face Mask are also detected in video and persons are classfied into two groups i.e With Mask with green bounding box and Without Mask with red bounding box

Another aspect incorporated was tracking people. This was accomplished using SORT(Simple Online Realtime Tracking) technique.

Each person is assigned a unique identity which is carried forward in subsequent frames.

This can be useful for further statistical analysis and computing violation metrics.

# Augmented Model performance:

## Accuracy Graph:

<a href="Accuracy.pdf" class="image fit" type="application/pdf"></a>
![alt text](https://github.com/hasnaintaqikazmi1214/CV_Project/blob/main/accuracy.png)

## Loss Graph:
![alt text](https://github.com/hasnaintaqikazmi1214/CV_Project/blob/main/loss.png)

# Datasets:

1) Kaggle Dataset: https://www.kaggle.com/ashishjangra27/face-mask-12k-images-dataset
2) Github Dataset: https://github.com/prajnasb/observations/tree/master/experiements/data

# Pre-Train Model Weights Link:
https://drive.google.com/file/d/1tGT4sfl0XeN3HGUBuF-GIf4kJ-IetBfM/view?usp=sharing

# How to Load Pre-Train Weights
load_model = keras.models.load_model("your_model_name") 
Put pre-train weights in Yolo folder and use as under
e.g. load_model_file = os.path.sep.join([args["yolo"], "model-017.model"])

## References

1) Social Distancing-https://github.com/deepak112/Social-Distancing-AI

2) People Tracking-https://github.com/abewley/sort

3) Monitoring COVID-19 social distancing with person detection and tracking via fine-tuned YOLO v3 and Deepsort techniques-https://arxiv.org/abs/2005.01385
