import tempfile
import os
import face_recognition
import cv2
import streamlit as st

# Combined CSS styles
st.markdown("""
<style>
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
    """Custom button with loading animation"""
    if st.button(label, key=key, **kwargs):
        video_url = "https://raw.githubusercontent.com/DhruvMenon2003/My-App/master/vecteezy_cybersecurity-animation-footage-depicted-with-shield-and-cctv_48713365.mp4"
        st.video(video_url)
        return True
    return False

def home_page():
    """Home page with verification initiation"""
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

        if button_with_loading("🛡️ START VERIFICATION", key="verify_btn"):
            st.session_state.page = 'verify'

def verification_page():
    """Face verification workflow"""
    if 'verified' not in st.session_state:
        st.session_state.verified = None
    if 'reference_img' not in st.session_state:
        st.session_state.reference_img = None

    st.title("Secure Face Verification 🔒")
    st.session_state.verification_started = True

    if st.session_state.get('verification_started'):
        uploaded_file = st.file_uploader("Upload your reference photo", 
                                       type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                tmp_file.write(uploaded_file.getbuffer())
                st.session_state.reference_img = tmp_file.name
            
            st.markdown("""
            <div class="camera-box">
                <h3>🔍 Real-Time Verification</h3>
                <p>Look directly into your camera</p>
            </div>
            """, unsafe_allow_html=True)
            
            reference_image = face_recognition.load_image_file(st.session_state.reference_img)
            reference_encoding = face_recognition.face_encodings(reference_image)[0]
            
            video_capture = cv2.VideoCapture(0)
            verified = False

            for _ in range(50):  # Check for 50 frames
                ret, frame = video_capture.read()
                if not ret:
                    continue

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_encodings = face_recognition.face_encodings(frame_rgb)

                for face_encoding in face_encodings:
                    match = face_recognition.compare_faces([reference_encoding], face_encoding)
                    if match[0]:
                        verified = True
                        break

                if verified:
                    break
            
            video_capture.release()
            st.session_state.verified = verified

            if st.session_state.reference_img and os.path.exists(st.session_state.reference_img):
                os.remove(st.session_state.reference_img)

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
            
            if st.button("Try Again 🔄"):
                st.session_state.clear()
                st.rerun()

def main():
    """Main app controller"""
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    
    if st.session_state.page == 'home':
        home_page()
    elif st.session_state.page == 'verify':
        verification_page()

if __name__ == "__main__":
    main()
