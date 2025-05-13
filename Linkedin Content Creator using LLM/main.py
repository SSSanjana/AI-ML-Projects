# main.py
# -------------------- Import Statements --------------------
import re
import io
import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import streamlit as st
from PIL import Image

from few_shot import FewShotPosts
from post_generator import generate_post
from post_analyzer import analyze_post
from compare import compare_posts
from line_chart import create_comparison_line_chart
from stability_sdk import client as stable_diffusion

# -------------------- Stability AI API Key --------------------
# Stability AI API key (nivetha acc key)
STABILITY_API_KEY = "sk-pdzAfTpJIelm8JQPtlKzvhCiRIcltdV790q6rzIWY6Ki151S"

# Initialize Stable Diffusion client
stable_client = stable_diffusion.StabilityInference(
    key=STABILITY_API_KEY,
    verbose=True,
    engine="stable-diffusion-xl-1024-v1-0"
)

# -------------------- Custom Styling --------------------
st.markdown("""
    <style>
        .stApp {
            display: flex;
            flex-direction: row;
        }
        .sidebar {
            width: 250px;
            background: #14213d;
            padding: 20px;
            color: #ffffff;
            height: 100vh;
        }
        .main-content {
            flex-grow: 1;
            padding: 40px;
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            color: #ffffff;
        }
        .title {
            font-size: 42px;
            font-weight: 800;
            font-family: 'Poppins', sans-serif;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }
        .subtitle {
            font-size: 22px;
            font-weight: 500;
            font-family: 'Lora', serif;
            color: #e0e0e0;
            margin-bottom: 30px;
        }
        .output-box {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(255, 255, 255, 0.2);
            margin-top: 20px;
            font-size: 18px;
            color: #0a1931;
            border-left: 5px solid #ffffff;
            font-family: 'Lora', serif;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------- Sidebar Navigation --------------------
with st.sidebar:
    nav_option = st.radio("Navigation", ["Generate Post", "Analyze Post"])

# -------------------- BrandBoost Header --------------------
st.markdown(
    """
    <div style='padding-top: 30px; padding-bottom: 10px; display: flex; flex-direction: column; align-items: flex-start; margin-left: 25%;'>
        <div style='display: flex; align-items: center; gap: 12px;'>
            <h1 style='font-size: 3em; font-weight: bold; margin: 0;'>BRANDBOOST🚀</h1>
        </div>
        <p style='font-size: 1.2em; margin: 5px 0 0 4px;'>AI-Powered LinkedIn Post Generator</p>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------- Generate Image Function --------------------
def generate_image(prompt):
    sanitized_prompt = (
        f"{prompt}, ultra HD, cinematic lighting, 8K, realistic, no text, no words, no letters, "
        "no captions, no symbols, no watermarks, no numbers, no logos, highly detailed, clean background"
    )

    try:
        response = stable_client.generate(sanitized_prompt)

        for resp in response:
            for artifact in resp.artifacts:
                if artifact.type == 1:
                    return Image.open(io.BytesIO(artifact.binary))
    except Exception as e:
        print("Image generation failed:", e)

    return None

# -------------------- Generate Post Page --------------------
if nav_option == "Generate Post":
    length_options = ["Short", "Medium", "Long"]
    language_options = ["English", "Hinglish"]
    fs = FewShotPosts()
    tags = fs.get_tags()

    col1, col2, col3 = st.columns(3)
    with col1:
        selected_tag = st.selectbox("🔖 Topic", options=tags)
    with col2:
        selected_length = st.selectbox("🔏 Length", options=length_options)
    with col3:
        selected_language = st.selectbox("🔣 Language", options=language_options)

    description = st.text_area("📝 Description (Optional)", placeholder="Provide specific details to personalize your post...")

    if st.button("✨ Generate Post and Image"):
        with st.spinner("Generating your LinkedIn post..."):
            post = generate_post(selected_length, selected_language, selected_tag, description)
            st.session_state.generated_post = post

    post = st.session_state.get("generated_post", "")

    if post:
        st.markdown(f"## Here is a LinkedIn post on {selected_tag}:")
        st.markdown(f'<div class="output-box">{post}</div>', unsafe_allow_html=True)

        # Generate and show image
        if "generated_image" not in st.session_state or st.session_state.get("image_post") != post:
            with st.spinner("Generating an image for your post..."):
                generated_image = generate_image(post)
                if generated_image:
                    st.session_state.generated_image = generated_image
                    st.session_state.image_post = post
                else:
                    st.session_state.generated_image = None

        if st.session_state.generated_image:
            st.image(st.session_state.generated_image, caption="Generated Image for Your Post")
        elif st.session_state.generated_image is None:
            st.error("Failed to generate an image. Please try again.")

        # -------------------- Compare Section --------------------
        st.markdown("<h4 style='margin-bottom: 5px;'>📝 Compare your LinkedIn post:</h4>", unsafe_allow_html=True)
        other_post_input = st.text_area("", height=150, placeholder="Paste another AI-generated post to compare")

        if st.button("🔍 Compare with Other AI Post"):
            if other_post_input.strip() == "":
                st.warning("Please paste a post to compare.")
            else:
                with st.spinner("Comparing BrandBoost post with the other AI-generated post..."):
                    comparison_text, scores_dict = compare_posts(post, other_post_input)

                    if scores_dict:
                        brandboost_scores = scores_dict.get("BrandBoost", {})
                        other_scores = scores_dict.get("OtherAI", {})

                        st.markdown("## 🥊 Post Comparison Results")
                        st.markdown(f"<div class='output-box'>{comparison_text}</div>", unsafe_allow_html=True)

                        fig = create_comparison_line_chart(brandboost_scores, other_scores)
                        st.pyplot(fig)
                    else:
                        st.error("Could not parse scores for comparison.")

# -------------------- Analyze Post Page --------------------
elif nav_option == "Analyze Post":
    st.markdown("### 📊 Post Performance Metrics")

    post_input = st.text_area("📝 Enter Post Content", placeholder="Paste your LinkedIn post here to analyze...")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        likes = st.number_input("👍 Likes", min_value=0, step=1, value=0)

    with col2:
        comments = st.number_input("💬 Comments", min_value=0, step=1, value=0)

    with col3:
        reposts = st.number_input("🔁 Reposts", min_value=0, step=1, value=0)

    with col4:
        bookmarks = st.number_input("🔖 Impressions", min_value=0, step=1, value=0)

    if st.button("📈 Analyze Post"):
        with st.spinner("Analyzing post..."):
            analysis = analyze_post(post_input, likes, comments, reposts, bookmarks)
            st.markdown("## 📋 Here is the analysis report")

            st.markdown("#### 🧩 1. Breakdown")
            st.markdown(analysis.get("structure", "Not Available"))

            st.markdown("#### 🎯 2. Tone and Emotional Feel")
            st.markdown(analysis.get("tone", "Not Available"))

            st.markdown("#### 🧠 3. Post Type")
            st.markdown(analysis.get("post_type", "Not Available"))

            st.markdown("#### 📊 4. Performance")
            st.markdown(analysis.get("performance", "Not Available"))

            st.markdown("#### 🛠️ 5. Suggestions to Improve")
            st.markdown(analysis.get("suggestions", "Not Available"))

            st.markdown("#### ✍️ 6. Rewritten (Your Style)")
            st.markdown(analysis.get("rewritten", "Not Available"))

            st.markdown("#### 🌐 7. Platforms to Repurpose")
            st.markdown(analysis.get("platforms", "Not Available"))

            st.markdown("#### 🎯 8. Target Audience")
            st.markdown(analysis.get("audience", "Not Available"))

