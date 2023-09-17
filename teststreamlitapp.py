import streamlit as st
from PIL import Image
import tempfile
import os
from colorAndShape import identify
from testcloudapi import detect_text
from scraper import get_headlines
from interactions import find_drug_interactions


# Function to process the uploaded image
def process_image(image_path):
    # Load the image using PIL
    img = Image.open(image_path)

    # Example processing: Convert the image to grayscale
    img = img.convert('L')

    # Save the processed image to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
        processed_image_path = temp_file.name
        img.save(processed_image_path, format='PNG')

    return processed_image_path

def main():
    st.title('Drug Wizard')
    st.image('drugWizard.webp', caption = None, width=250)

    # Create a file uploader widget
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    ocr_completed = False
    

    if uploaded_image is not None:

        # Store the uploaded image in a temporary file
        temp_image_path = os.path.join(tempfile.gettempdir(), uploaded_image.name)
        with open(temp_image_path, "wb") as f:
            f.write(uploaded_image.read())

        # Display the uploaded image
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

        # Show the image processing options for testing
        st.sidebar.subheader("Image Processing Options")

        # Color and Shape
        if st.sidebar.checkbox("Color and Shape"):
            pill = identify(temp_image_path)
            st.write("Color and Shape: ")
            st.write(pill)
        
        # Optical Character Recognition
        if st.sidebar.checkbox("Optical Character Recognition"):
            ocr_completed = True
            texts = detect_text(temp_image_path)
            st.write("Recognized text:")
            st.write(texts)

        # Pill Identification via Scraping
        if ocr_completed == True:
            if st.sidebar.checkbox("Pill Identification via Scraping"):
                headlines = get_headlines(texts)
                st.write("Headlines:")
                for text in headlines:
                    st.write(text)

        # Pill Identification via Image Processing using OpenFDA API
        if ocr_completed == True:
            if st.sidebar.checkbox("Pill Interactions via OpenFDA API"):
                st.write("Pill Interactions via OpenFDA API:")
                interactions = find_drug_interactions(texts)
                st.write(interactions)
    

if __name__ == "__main__":
    main()