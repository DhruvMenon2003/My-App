import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av
import cv2
import numpy as np

class VideoVerifier(VideoProcessorBase):
    def __init__(self):
        self.verified = False
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        # Simulate face detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) > 0:
            self.verified = True
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        
        return av.VideoFrame.from_ndarray(img, format="bgr24")

def main():
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
        .success-message {
            color: #4CAF50;
            font-size: 1.5em;
            animation: fadeIn 1s;
        }
        @keyframes fadeIn {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }
    </style>
    """, unsafe_allow_html=True)

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

        if st.button("🛡️ START VERIFICATION", key="verify_btn", help="Click to begin identity verification"):
            st.session_state.start_verification = True

        if 'start_verification' in st.session_state and st.session_state.start_verification:
            ctx = webrtc_streamer(
                key="verification",
                video_processor_factory=VideoVerifier,
                rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
            )
            
            if ctx.video_processor:
                with st.spinner('Verifying identity...'):
                    if ctx.video_processor.verified:
                        st.session_state.verified = True
                        st.session_state.start_verification = False
                        st.experimental_rerun()

        if 'verified' in st.session_state and st.session_state.verified:
            st.markdown("""
                <div class="success-message">
                    ✅ Verification Successful!<br>
                    🎉 Welcome to Kaboose! 🚀
                </div>
            """, unsafe_allow_html=True)
            del st.session_state.verified

if __name__ == "__main__":
    main()
