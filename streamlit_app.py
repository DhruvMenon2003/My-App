import streamlit as st
import time
def button_with_loading(label, key=None, **kwargs):
    """
    Custom button that shows a cybersecurity animation video when clicked.
    Returns True if the button was clicked.
    """
    if st.button(label, key=key, **kwargs):
        video_url = "https://github.com/DhruvMenon2003/My-App/blob/master/vecteezy_cybersecurity-animation-footage-depicted-with-shield-and-cctv_48713365.mp4"
        st.video(video_url)
        return True
    return False
def main():
    # Custom CSS for animations
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
    </style>
    """, unsafe_allow_html=True)

    st.title('🎈  Kaboose User Verification')
    
    # Centered layout
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
            st.session_state.verify_clicked = True

        st.markdown("<br><br>", unsafe_allow_html=True)

if __name__ == "__main__":
    # Integrate with existing Logic
    main()



