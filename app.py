import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

az_key = st.secrets["az_key"]
# Initialize Computer Vision Client
#https://aianalysisimage1209-prediction.cognitiveservices.azure.com/
computervision_client = ComputerVisionClient('https://aianalysisimage1209-prediction.cognitiveservices.azure.com/', CognitiveServicesCredentials(az_key))

def analyze_image(image):
    
    return analysis


def display_analysis(analysis):
    st.write(f"  Line Drawing Type: {analysis.image_type.line_drawing_type}")

st.title('Dr. Lee Azure Computer Vision App')

uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'png', 'jpeg'])
url = st.text_input("Or enter Image URL:")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Classifying...")
    analysis = analyze_image(image)
    #display_analysis(analysis)

elif url:
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        content_type = response.headers.get('Content-Type', '')
        if 'image' in content_type:
            image = Image.open(BytesIO(response.content))
            st.image(image, caption='Image from URL.', use_column_width=True)
            st.write("")
            st.write("Classifying...")
            analysis = analyze_image(image)
            display_analysis(analysis)
        else:
            st.error("The URL does not point to a valid image. Content-Type received was " + content_type)
            
    except requests.RequestException as e:
        st.error(f"Failed to fetch image due to request exception: {str(e)}")
        
    except requests.HTTPError as e:
        st.error(f"HTTP Error occurred: {str(e)}")
        
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
