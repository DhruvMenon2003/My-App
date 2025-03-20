import streamlit as st
import os
import tempfile
import deepface_cv2
import cv2
import numpy as np

# Streamlit UI
st.title("Real-Time Face Verification with DeepFace.stream")

# Step 1: Verify button
if st.button("Verify"):
    # Step 2: Upload Image
    uploaded_file = st.file_uploader("Upload a picture (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        # Step 3: Save uploaded file temporarily
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, uploaded_file.name)
        
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.image(temp_path, caption="Uploaded Image", use_column_width=True)
        st.success("Image uploaded successfully!")

        # Step 4: Start DeepFace.stream for real-time verification
        st.warning("Verifying... Look at the camera!")

        try:
            # Run DeepFace.stream for real-time face verification
            DeepFace.stream(db_path=temp_dir, model_name="VGG-Face", detector_backend="opencv")
            
            # If DeepFace.stream succeeds, show a verified message
            st.success("✅ Verified! Face match successful.")

        except Exception as e:
            st.error(f"❌ Not Verified! Face does not match. Error: {e}")
