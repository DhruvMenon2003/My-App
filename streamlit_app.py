# streamlit_app.py
import streamlit as st
import tempfile
import os
from deepface import DeepFace
import cv2

# Combined CSS for all pages
st.markdown("""
<style>
    /* Landing page styles */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    .verify-btn {
        animation: pulse 2s infinite;
        background: linear-gradient(145deg, #4CAF50, #45a049);
        border: none;
        color: white;
        padding: 20px 40px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 24px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .verify-btn:hover {
        animation: none;
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(0,0,0,0.25);
    }
    
    /* Verification page styles */
    .verified {
        color: #4CAF50;
        font-size: 24px;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #4CAF50;
        text-align: center;
    }
    .failed {
        color: #ff4444;
        font-size: 24px;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #ff4444;
        text-align: center;
    }
    .camera-box {
        border: 2px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

def button_with_loading(label, key=None, **kwargs):
    """Custom button with video animation"""
    if st.button(label, key=key, **kwargs):
        video_url = "https://raw.githubusercontent.com/DhruvMenon2003/My-App/master/vecteezy_cybersecurity-animation-footage-depicted-with-shield-and-cctv_48713365.mp4"
        st.video(video_url)
        return True
    return False

def landing_page():
    """Initial verification landing page"""
    st.title('🎈 Kaboose User Verification')
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div style="text-align: center;">
                <h3 style="color: #2c3e50;">Let's make sure it's you</h3>
                <p style="color: #7f8c8d;">Real-Time Video verification in just 1-2 seconds!</p>
            </div>
        """, unsafe_allow_html=True)

        if button_with_loading("🛡️ START VERIFICATION", key="verify_btn", 
                            help="Click to begin identity verification"):
            st.session_state.page = "verification"
            st.rerun()

def verification_page():
    """Face verification process page"""
    st.title("Secure Face Verification 🔒")
    
    if 'verified' not in st.session_state:
        st.session_state.verified = None
    if 'reference_img' not in st.session_state:
        st.session_state.reference_img = None

    # Upload reference image
    uploaded_file = st.file_uploader("Upload your reference photo", 
                                   type=["jpg", "jpeg", "png"],
                                   accept_multiple_files=False)
    
    if uploaded_file is not None and not st.session_state.verified:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            st.session_state.reference_img = tmp_file.name
        
        st.markdown("""
        <div class="camera-box">
            <h3>🔍 Real-Time Verification</h3>
            <p>Look directly into your camera</p>
        </div>
        """, unsafe_allow_html=True)

        with tempfile.TemporaryDirectory() as temp_db:
            os.link(st.session_state.reference_img, f"{temp_db}/reference.jpg")
            
            try:
                result = DeepFace.stream(
                    db_path=temp_db,
                    model_name="Facenet512",
                    detector_backend="retinaface",
                    enable_face_analysis=False,
                    time_threshold=2,
                    frame_threshold=5
                )
                
                st.session_state.verified = bool(result)
                
            except Exception as e:
                st.error(f"Verification error: {str(e)}")
                st.session_state.verified = False

        if st.session_state.reference_img and os.path.exists(st.session_state.reference_img):
            os.remove(st.session_state.reference_img)

    # Display results
    if st.session_state.verified is not None:
        if st.session_state.verified:
            st.markdown("""
            <div class="verified">
                ✅ Verified Successfully!<br>
                <span style="font-size: 18px;">You may now proceed</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="failed">
                ❌ Verification Failed<br>
                <span style="font-size: 18px;">Please try again or contact support 📧 hello@kaboose.app</span>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Try Again 🔄", use_container_width=True):
                st.session_state.clear()
                st.rerun()

def main():
    """Main app controller"""
    if 'page' not in st.session_state:
        st.session_state.page = "landing"
    
    if st.session_state.page == "landing":
        landing_page()
    elif st.session_state.page == "verification":
        verification_page()

if __name__ == "__main__":
    main()
