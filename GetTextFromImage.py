import requests
import time
# If you are using a Jupyter notebook, uncomment the following line.
#%matplotlib inline
import matplotlib.pyplot as plt
from matplotlib.patches import (Rectangle, Polygon)
from PIL import Image
from io import BytesIO

# Key to authorize use of the API
subscription_key = "ae5e5176d4fd495a8de45f0822812765"
assert subscription_key

# Where to send the API request
vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"

def printReadText(word_info_dict = {}):
    onlyText = ""
    for word in word_info_dict:
        onlyText += word["text"]
        onlyText += " "
    print(onlyText)

def readMachineText(image_path):
    # Specify API function URL
    ocr_url = vision_base_url + "ocr"

    # Read the image into a byte array
    image_data = open(image_path, "rb").read()
    headers    = {'Ocp-Apim-Subscription-Key': subscription_key,
                  'Content-Type': 'application/octet-stream',
                   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}
    params     = {'language': 'unk', 'detectOrientation': 'true'}
    response = requests.post(
        ocr_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()

    analysis = response.json()

    # Extract the word bounding boxes and text.
    # line_infos = [region["lines"] for region in analysis["regions"]]
    read_words = []
    '''for region in line_infos:
        read_line_words = []
        for line in region:
            read_line_words = [word_info["text"] for word_info in line["words"]]
        read_words.append(read_line_words)'''
    for region in analysis['regions']:
        for line in region['lines']:
            line_words = []
            for word in line['words']:
                line_words.append(word['text'])
            read_words.append(line_words)
            
    return read_words
    
    ## Print out all combinations of words that are next to each other
    # word_text = [word["text"] for word in word_infos]
    # cycleSubStrings(word_text)
    # printReadText(word_infos)
        
def readHandwrittenText(image_path):
    # Specify API function URL
    text_recognition_url = vision_base_url + "recognizeText"
    
    # Read the image into a byte array
    image_data = open(image_path, "rb").read()
    # Note: The request parameter changed for APIv2.
    # For APIv1, it is 'handwriting': 'true'.
    headers    = {'Ocp-Apim-Subscription-Key': subscription_key,
                  'Content-Type': 'application/octet-stream',
                   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}
    params     = {'mode': 'Handwritten'}
    response = requests.post(
        text_recognition_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()

    # Extracting handwritten text requires two API calls: One call to submit the
    # image for processing, the other to retrieve the text found in the image.

    # Holds the URI used to retrieve the recognized text.
    operation_url = response.headers["Operation-Location"]

    # The recognized text isn't immediately available, so poll to wait for completion.
    analysis = {}
    poll = True
    while (poll):
        response_final = requests.get(
            response.headers["Operation-Location"], headers=headers)
        analysis = response_final.json()
        time.sleep(1)
        if ("recognitionResult" in analysis):
            poll= False 
        if ("status" in analysis and analysis['status'] == 'Failed'):
            poll= False

    read_words = []
    if ("recognitionResult" in analysis):
        # Extract the recognized text, with bounding boxes.
        read_words = [(line["text"]).split() for line in analysis["recognitionResult"]["lines"]]
    return read_words

##
## Everything past here is sort of unnecessary
def readMachineTextRemoteFile():
    # Specify API function URL
    ocr_url = vision_base_url + "ocr"

    # Set image_url to the URL of an image that you want to analyze.
    image_url = input("Enter URL of image: ")

    headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}
    params  = {'language': 'unk', 'detectOrientation': 'true'}
    data    = {'url': image_url}
    response = requests.post(ocr_url, headers=headers, params=params, json=data)
    response.raise_for_status()

    analysis = response.json()

    # Extract the word bounding boxes and text.
    line_infos = [region["lines"] for region in analysis["regions"]]
    read_words = []
    for line in line_infos:
        for word_metadata in line:
            for word_info in word_metadata["words"]:
                read_words.append(word_info["text"])
    return read_words
    
    ## Print out all combinations of words that are next to each other
    # word_text = [word["text"] for word in word_infos]
    # cycleSubStrings(word_text)
    # printReadText(word_infos)
        
def readHandwrittenTextRemoteFile():
    # Specify API function URL
    text_recognition_url = vision_base_url + "recognizeText"

    # Set image_url to the URL of an image that you want to analyze.
    image_url = input("Enter URL of image: ")

    headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}
    # Note: The request parameter changed for APIv2.
    # For APIv1, it is 'handwriting': 'true'.
    params  = {'mode': 'Handwritten'}
    data    = {'url': image_url}
    response = requests.post(
        text_recognition_url, headers=headers, params=params, json=data)
    response.raise_for_status()

    # Extracting handwritten text requires two API calls: One call to submit the
    # image for processing, the other to retrieve the text found in the image.

    # Holds the URI used to retrieve the recognized text.
    operation_url = response.headers["Operation-Location"]

    # The recognized text isn't immediately available, so poll to wait for completion.
    analysis = {}
    poll = True
    while (poll):
        response_final = requests.get(
            response.headers["Operation-Location"], headers=headers)
        analysis = response_final.json()
        time.sleep(1)
        if ("recognitionResult" in analysis):
            poll= False 
        if ("status" in analysis and analysis['status'] == 'Failed'):
            poll= False

    polygons=[]
    if ("recognitionResult" in analysis):
        # Extract the recognized text, with bounding boxes.
        polygons = [(line["boundingBox"], line["text"])
            for line in analysis["recognitionResult"]["lines"]]

    for line in polygons:
        print(line[1]);
