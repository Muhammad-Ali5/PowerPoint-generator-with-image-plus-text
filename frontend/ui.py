import streamlit as st
import requests
import os
import time

# Backend API URL
API_URL = "http://127.0.0.1:8000/generate_ppt"

# Page config
st.set_page_config(
    page_title="AI PowerPoint Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern dark design with better text visibility
st.markdown("""
<style>
    /* Main background - Dark grey */
    .stApp {
        background: #0f0f0f;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 3rem 0;
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
        border-radius: 24px;
        margin-bottom: 2.5rem;
        box-shadow: 0 20px 60px 0 rgba(124, 58, 237, 0.3);
    }
    
    .main-header h1 {
        color: #ffffff;
        font-size: 3.5rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }
    
    .main-header p {
        color: #e9d5ff;
        font-size: 1.3rem;
        margin-top: 0.8rem;
        font-weight: 400;
    }
    
    /* Card styling - Dark grey */
    .card {
        background: #1a1a1a;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
        margin: 1rem 0;
        border: 1px solid #2a2a2a;
    }
    
    /* All text inside cards should be light */
    .card * {
        color: #e5e5e5;
    }
    
    /* Input labels - light and bold */
    label {
        color: #f5f5f5 !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Input fields - Dark with light text and visible cursor */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #3a3a3a;
        padding: 0.85rem 1rem;
        font-size: 1.05rem;
        color: #ffffff !important;
        background-color: #262626 !important;
        font-weight: 500;
        caret-color: #a855f7 !important;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:hover {
        border-color: #7c3aed;
        background-color: #2a2a2a !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #a855f7;
        box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.2);
        color: #ffffff !important;
        background-color: #2a2a2a !important;
        outline: none;
    }
    
    /* Placeholder text */
    .stTextInput > div > div > input::placeholder {
        color: #737373 !important;
        opacity: 1 !important;
    }
    
    /* Slider */
    .stSlider {
        padding: 1.5rem 0;
    }
    
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #7c3aed 0%, #a855f7 100%);
    }
    
    .stSlider label {
        color: #f5f5f5 !important;
        font-weight: 600 !important;
    }
    
    /* Slider value */
    .stSlider [data-testid="stTickBarMin"],
    .stSlider [data-testid="stTickBarMax"] {
        color: #a3a3a3 !important;
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
        color: #ffffff !important;
        border: none;
        padding: 1rem 2rem;
        font-size: 1.15rem;
        font-weight: 700;
        border-radius: 14px;
        transition: all 0.3s ease;
        box-shadow: 0 8px 24px 0 rgba(124, 58, 237, 0.4);
        text-transform: none;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 32px 0 rgba(124, 58, 237, 0.6);
        background: linear-gradient(135deg, #8b5cf6 0%, #c084fc 100%);
    }
    
    /* Download button */
    .stDownloadButton > button {
        width: 100%;
        background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
        color: #ffffff !important;
        border: none;
        padding: 1rem 2rem;
        font-size: 1.15rem;
        font-weight: 700;
        border-radius: 14px;
        transition: all 0.3s ease;
        box-shadow: 0 8px 24px 0 rgba(16, 185, 129, 0.4);
        cursor: pointer;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 32px 0 rgba(16, 185, 129, 0.6);
        background: linear-gradient(135deg, #34d399 0%, #6ee7b7 100%);
    }
    
    /* Metrics */
    .stMetric {
        background: #262626;
        padding: 1.5rem;
        border-radius: 14px;
        border: 1px solid #3a3a3a;
    }
    
    .stMetric label {
        color: #d4d4d4 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #a855f7 !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
    }
    
    /* Success message */
    .success-box {
        background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
        color: #ffffff;
        padding: 1.8rem;
        border-radius: 16px;
        text-align: center;
        font-size: 1.4rem;
        font-weight: 700;
        margin: 1.5rem 0;
        animation: slideIn 0.5s ease;
        box-shadow: 0 8px 24px 0 rgba(16, 185, 129, 0.4);
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Feature cards */
    .feature-card {
        background: #1a1a1a;
        padding: 2rem;
        border-radius: 18px;
        text-align: center;
        margin: 0.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.3);
        border: 1px solid #2a2a2a;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 12px 32px 0 rgba(124, 58, 237, 0.3);
        border-color: #7c3aed;
    }
    
    .feature-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-card h3 {
        color: #f5f5f5 !important;
        margin: 0.8rem 0;
        font-weight: 700;
        font-size: 1.3rem;
    }
    
    .feature-card p {
        color: #a3a3a3 !important;
        margin: 0;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    /* Markdown headings */
    h1, h2, h3, h4, h5, h6 {
        color: #f5f5f5 !important;
        font-weight: 700 !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #7c3aed 0%, #a855f7 100%);
    }
    
    /* Status text */
    .stMarkdown {
        color: #e5e5e5;
    }
    
    /* Error messages */
    .stAlert {
        border-radius: 12px;
        background: #262626;
        border: 1px solid #3a3a3a;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Ensure all paragraph text is visible */
    p {
        color: #d4d4d4;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #3a3a3a;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #7c3aed;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🎨 AI PowerPoint Generator</h1>
    <p>Create stunning presentations with AI-generated content and images</p>
</div>
""", unsafe_allow_html=True)

# Features section
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <h3>AI Content</h3>
        <p>Smart slide generation with Google Gemini</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🖼️</div>
        <h3>AI Images</h3>
        <p>Beautiful images for every slide</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">⚡</div>
        <h3>Fast & Easy</h3>
        <p>Generate in seconds, download instantly</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main content area
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    # Input Form
    st.markdown("### 📝 Create Your Presentation")
    
    topic = st.text_input(
        "Presentation Topic",
        placeholder="e.g., The Future of Artificial Intelligence",
        help="Enter the main topic for your presentation",
        key="topic_input"
    )
    
    slide_count = st.slider(
        "Number of Slides",
        min_value=1,
        max_value=10,
        value=5,
        help="Choose how many slides you want"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    generate_btn = st.button("✨ Generate Presentation", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📊 Quick Stats")
    st.metric("Slides to Generate", slide_count)
    st.metric("Estimated Time", f"{slide_count * 10} sec")
    st.markdown('</div>', unsafe_allow_html=True)

# Generation logic
if generate_btn:
    if not topic:
        st.error("⚠️ Please enter a topic for your presentation")
    else:
        # Progress container
        progress_container = st.container()
        
        with progress_container:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.markdown("🔄 **Connecting to AI backend...**")
            progress_bar.progress(10)
            time.sleep(0.3)
            
            try:
                status_text.markdown("🧠 **Generating slide content with AI...**")
                progress_bar.progress(30)
                
                payload = {"topic": topic, "slide_count": slide_count}
                response = requests.post(API_URL, json=payload, stream=True)
                
                status_text.markdown("🎨 **Creating images for each slide...**")
                progress_bar.progress(60)
                
                if response.status_code == 200:
                    progress_bar.progress(90)
                    status_text.markdown("📦 **Assembling your presentation...**")
                    
                    time.sleep(0.5)
                    progress_bar.progress(100)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Success message
                    st.markdown("""
                    <div class="success-box">
                        🎉 Presentation Generated Successfully!
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Download section
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown("### 📥 Download Your Presentation")
                    
                    col_dl1, col_dl2 = st.columns([3, 1])
                    
                    with col_dl1:
                        st.download_button(
                            label="💾 Download PowerPoint",
                            data=response.content,
                            file_name=f"{topic.replace(' ', '_')}.pptx",
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                            use_container_width=True
                        )
                    
                    with col_dl2:
                        st.markdown(f"<p style='font-size: 1.1rem; font-weight: 600; margin-top: 0.5rem;'>{slide_count} slides</p>", unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                else:
                    st.error(f"❌ Error: {response.status_code} - {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to the backend. Make sure the FastAPI server is running.")
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
            
            finally:
                if 'progress_bar' in locals():
                    progress_bar.empty()
                if 'status_text' in locals():
                    status_text.empty()

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #e0e7ff; padding: 2rem;">
    <p style="font-size: 1rem; color: #e0e7ff;">Powered by Google Gemini & Pollinations.ai • Built with ❤️ using Streamlit & FastAPI</p>
</div>
""", unsafe_allow_html=True)
