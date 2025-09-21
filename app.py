import streamlit as stimport streamlit as st

import numpy as npfrom PIL import Image, ImageChops, ImageEnhance

from PIL import Image, ImageChops, ImageEnhanceimport io

import requestsimport re

import reimport numpy as np

from urllib.parse import urlparse

import io# Configure the Streamlit page

st.set_page_config(

# Page configuration    page_title="TruthShield — Demo",

st.set_page_config(    layout="centered",

    page_title="TruthShield - Media Credibility Checker",    initial_sidebar_state="collapsed"

    page_icon="🛡️",)

    layout="wide",st.title("TruthShield — Misinformation & Deepfake Detector (Streamlit Demo)")

    initial_sidebar_state="collapsed"st.write("Prototype demo: text/link credibility check, image ELA visualization, and NSFW/deepfake hint.")

)

SENSATIONAL = [

# Custom CSS for better styling    "shocking", "unbelievable", "you won't believe", "secret", "exposed",

st.markdown("""    "breaking", "urgent", "miracle", "guaranteed", "click here", "free money"

<style>]

    .main-header {TRUSTED_DOMAINS = ["thehindu.com", "indianexpress.com", "bbc.com", "reuters.com", "apnews.com", "factcheck.org"]

        text-align: center;

        padding: 1rem 0;def text_score(text):

        margin-bottom: 2rem;    t = (text or "").strip()

    }    score = 70

    .metric-container {    rationale = []

        background-color: #f0f2f6;    if not t:

        padding: 1rem;        return 0, "No Input", ["No text provided"]

        border-radius: 0.5rem;

        margin: 1rem 0;    low = t.lower()

    }    found_ks = [kw for kw in SENSATIONAL if kw in low]

    .warning-box {    if found_ks:

        background-color: #fff3cd;        score -= 6 * len(found_ks)

        border: 1px solid #ffeaa7;        rationale.append(f"Sensational keywords found: {', '.join(found_ks)}")

        border-radius: 0.5rem;

        padding: 1rem;    excl = low.count("!")

        margin: 1rem 0;    if excl > 0:

    }        score -= min(5, excl) * 3

    .info-box {        rationale.append(f"Exclamation marks: {excl}")

        background-color: #d4edda;

        border: 1px solid #c3e6cb;    uppercase_chars = sum(1 for c in t if c.isupper())

        border-radius: 0.5rem;    if uppercase_chars > max(10, len(t)//3):

        padding: 1rem;        score -= 8

        margin: 1rem 0;        rationale.append("Excessive uppercase characters")

    }

</style>    m = re.search(r"https?://([^/]+)/?", t)

""", unsafe_allow_html=True)    if m:

        domain = m.group(1).replace("www.", "")

def analyze_text_credibility(text, url=None):        if domain in TRUSTED_DOMAINS:

    """Analyze text credibility using heuristic scoring"""            score += 10

    score = 50  # Start with neutral score            rationale.append(f"Trusted domain detected: {domain}")

    flags = []        else:

                rationale.append(f"External domain detected: {domain} (not in trusted list)")

    # Sensational keywords (reduce credibility)

    sensational_keywords = [    score = max(0, min(100, score))

        'shocking', 'unbelievable', 'amazing', 'incredible', 'mind-blowing',    label = "Real" if score >= 70 else ("Suspicious" if score >= 45 else "Likely Fake")

        'devastating', 'explosive', 'breaking', 'urgent', 'must read',    return int(score), label, rationale

        'you won\'t believe', 'doctors hate', 'secret', 'exposed',

        'leaked', 'conspiracy', 'cover-up', 'hidden truth'@st.cache_data(ttl=3600)  # Cache results for 1 hour

    ]def ela_image(pil_img, quality=90):

        """Perform Error Level Analysis on the image."""

    text_lower = text.lower()    try:

    sensational_count = sum(1 for keyword in sensational_keywords if keyword in text_lower)        if pil_img is None:

    if sensational_count > 0:            raise ValueError("No image provided")

        penalty = min(sensational_count * 5, 25)            

        score -= penalty        img_rgb = pil_img.convert("RGB")

        flags.append(f"Contains {sensational_count} sensational keyword(s)")        buf = io.BytesIO()

            img_rgb.save(buf, "JPEG", quality=quality)

    # Excessive capitalization        buf.seek(0)

    caps_ratio = sum(1 for c in text if c.isupper()) / len(text) if text else 0        jpg = Image.open(buf).convert("RGB")

    if caps_ratio > 0.15:        diff = ImageChops.difference(img_rgb, jpg)

        score -= 15        diff_enh = ImageEnhance.Brightness(diff).enhance(10.0)

        flags.append("Excessive capitalization detected")        arr = np.array(diff_enh).astype(float)

            avg = arr.mean()

    # Excessive punctuation        score = 100 - min(90, avg)

    exclamation_count = text.count('!')        score = max(0.0, min(100.0, score))

    question_count = text.count('?')        label = "Real" if score >= 70 else ("Suspicious" if score >= 45 else "Likely Manipulated")

    if exclamation_count > 3:        return diff_enh, float(score), label

        score -= min(exclamation_count * 2, 20)    except ValueError as ve:

        flags.append(f"Excessive exclamation marks ({exclamation_count})")        st.error(str(ve))

            return None, 0.0, "Error"

    # URL analysis if provided    except Exception as e:

    if url:        st.error(f"Error analyzing image: {str(e)}")

        parsed_url = urlparse(url)        return None, 0.0, "Error"

        domain = parsed_url.netloc.lower()

        @st.cache_data(ttl=3600)  # Cache results for 1 hour

        # Trusted domains (boost credibility)def nsfw_hint(pil_img):

        trusted_domains = [    """Analyze image for potential NSFW content using a simple heuristic."""

            'bbc.com', 'reuters.com', 'ap.org', 'npr.org',    try:

            'pbs.org', 'cnn.com', 'nytimes.com', 'washingtonpost.com',        if pil_img is None:

            'wsj.com', 'theguardian.com', 'nature.com', 'science.org'            raise ValueError("No image provided")

        ]            

                small = pil_img.resize((64,64)).convert("RGB")

        # Suspicious domains (reduce credibility)        arr = np.array(small).astype(int)

        suspicious_indicators = [        skin_pixels = ((arr[:,:,0] > 100) & (arr[:,:,1] > 80) & (arr[:,:,2] > 60))

            '.tk', '.ml', '.ga', '.cf',  # Free domains        ratio = skin_pixels.mean()

            'fake', 'hoax', 'satire', 'onion'        return (ratio > 0.15), float(ratio)

        ]    except ValueError as ve:

                st.error(str(ve))

        if any(trusted in domain for trusted in trusted_domains):        return False, 0.0

            score += 20    except Exception as e:

            flags.append("Source from trusted domain")        st.error(f"Error processing image: {str(e)}")

        elif any(suspicious in domain for suspicious in suspicious_indicators):        return False, 0.0

            score -= 25

            flags.append("Suspicious domain detected")tab1, tab2, tab3 = st.tabs(["Text / Link Check", "Image ELA & NSFW Hint", "About & Notes"])

        

        # HTTPS checkwith tab1:

        if parsed_url.scheme == 'https':    st.subheader("Text / Link Credibility Check")

            score += 5    user_text = st.text_area("Paste headline, post text, or URL", height=140)

        else:    if st.button("Verify Text"):

            score -= 10        if not user_text or not user_text.strip():

            flags.append("Non-secure HTTP connection")            st.warning("Please paste some text or a URL to verify.")

            else:

    # Grammar and spelling (simple heuristic)            score, label, rationale = text_score(user_text)

    sentences = re.split(r'[.!?]+', text)            st.metric("Credibility Score", f"{score}/100")

    if len(sentences) > 1:            st.markdown(f"**Verdict:** {label}")

        avg_sentence_length = len(text.split()) / len(sentences)            if rationale:

        if avg_sentence_length < 3:  # Very short sentences might indicate poor quality                st.markdown("**Rationale:**")

            score -= 10                for r in rationale:

            flags.append("Unusually short sentences")                    st.write("- " + r)

                st.caption("Prototype heuristic. Replace with fine-tuned NLP model for production.")

    # Ensure score is within bounds

    score = max(0, min(100, score))with tab2:

        st.subheader("Image ELA (Error Level Analysis) & NSFW Hint")

    return score, flags    uploaded = st.file_uploader("Upload image (JPEG/PNG)", type=["jpg", "jpeg", "png"])

    if uploaded is not None:

def perform_ela_analysis(image):        try:

    """Perform Error Level Analysis on uploaded image"""            img = Image.open(uploaded)

    try:            st.image(img, caption="Original", use_column_width=True)

        # Convert to RGB if necessary            if st.button("Analyze Image"):

        if image.mode != 'RGB':                ela_vis, integrity_score, ela_label = ela_image(img)

            image = image.convert('RGB')                nsfw_flag, nsfw_ratio = nsfw_hint(img)

                        st.image(ela_vis, caption="ELA Visualization", use_column_width=True)

        # Save as JPEG with specific quality                st.metric("Integrity Score", f"{integrity_score:.1f}/100")

        temp_buffer = io.BytesIO()                st.markdown(f"**ELA Verdict:** {ela_label}")

        image.save(temp_buffer, format='JPEG', quality=95)                st.markdown(f"**NSFW Hint:** {'Yes 🚨' if nsfw_flag else 'No'} (skin-ratio={nsfw_ratio:.2f})")

        temp_buffer.seek(0)                st.caption("ELA is a heuristic visualization. NSFW hint is a crude demo — do not rely on it for decisions.")

                except Exception as e:

        # Reload the compressed image            st.error("Could not process the uploaded image. Make sure it is a valid image file.")

        compressed_image = Image.open(temp_buffer)

        with tab3:

        # Calculate difference    st.header("About this demo")

        ela_image = ImageChops.difference(image, compressed_image)    st.write("""

        **TruthShield (Streamlit Demo)** is a lightweight, single-file prototype intended for hackathon demonstration purposes.

        # Enhance the differenceIt includes:

        extrema = ela_image.getextrema()- A text/link credibility heuristic (quick demo),

        max_diff = max([ex[1] for ex in extrema])- ELA visualization for images, and

        if max_diff > 0:- A naive NSFW/deepfake hint (skin-tone heuristic).

            scale = 255.0 / max_diff

            ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)**Important:** This demo uses heuristics and is NOT suitable for production or legal enforcement.

        For production, replace heuristics with:

        # Calculate integrity score based on ELA variance- Fine-tuned RoBERTa/BERT for fake-news detection,

        ela_array = np.array(ela_image)- Xception / Deepfake detectors (FaceForensics models) for vision,

        variance = np.var(ela_array)- OpenNSFW2 or fine-tuned CNN for NSFW detection,

        - Perceptual hashing + web search for traceback.

        # Normalize variance to score (higher variance = lower integrity)""")

        integrity_score = max(0, min(100, 100 - (variance / 1000)))
        
        return ela_image, integrity_score
    
    except Exception as e:
        st.error(f"Error in ELA analysis: {str(e)}")
        return None, 0

def detect_nsfw_heuristic(image):
    """Simple skin-tone ratio based NSFW detection (very basic heuristic)"""
    try:
        # Convert to RGB
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize for faster processing
        image = image.resize((100, 100))
        
        # Convert to numpy array
        img_array = np.array(image)
        
        # Define skin tone ranges (very basic)
        # This is a simplified heuristic and not accurate for production use
        skin_pixels = 0
        total_pixels = img_array.shape[0] * img_array.shape[1]
        
        for i in range(img_array.shape[0]):
            for j in range(img_array.shape[1]):
                r, g, b = img_array[i, j]
                
                # Basic skin tone detection (very rough heuristic)
                if (r > 95 and g > 40 and b > 20 and 
                    max(r, g, b) - min(r, g, b) > 15 and 
                    abs(r - g) > 15 and r > g and r > b):
                    skin_pixels += 1
        
        skin_ratio = skin_pixels / total_pixels
        
        # Flag if skin ratio is unusually high (>30%)
        is_flagged = skin_ratio > 0.3
        
        return skin_ratio, is_flagged
    
    except Exception as e:
        st.error(f"Error in NSFW detection: {str(e)}")
        return 0, False

# Main app
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ TruthShield</h1>
        <p>Media Credibility & Integrity Checker</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📝 Text/Link Credibility", "🖼️ Image Analysis", "ℹ️ About & Notes"])
    
    with tab1:
        st.header("Text & Link Credibility Analysis")
        st.markdown("Analyze text content and URLs for credibility indicators using heuristic scoring.")
        
        # Text input
        text_input = st.text_area(
            "Enter text to analyze:",
            height=150,
            placeholder="Paste the text content you want to analyze for credibility..."
        )
        
        # URL input
        url_input = st.text_input(
            "Enter URL (optional):",
            placeholder="https://example.com/article"
        )
        
        if st.button("🔍 Analyze Credibility", type="primary"):
            if text_input.strip():
                with st.spinner("Analyzing credibility..."):
                    score, flags = analyze_text_credibility(text_input, url_input if url_input.strip() else None)
                
                # Display results
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    color = "normal"
                    if score >= 70:
                        color = "normal"
                        status = "High"
                    elif score >= 40:
                        color = "normal" 
                        status = "Medium"
                    else:
                        color = "inverse"
                        status = "Low"
                    
                    st.metric(
                        label="Credibility Score",
                        value=f"{score}/100",
                        delta=status
                    )
                
                with col2:
                    st.metric(
                        label="Flags Detected",
                        value=len(flags)
                    )
                
                with col3:
                    word_count = len(text_input.split())
                    st.metric(
                        label="Word Count",
                        value=word_count
                    )
                
                # Display flags
                if flags:
                    st.markdown("### ⚠️ Detected Issues:")
                    for flag in flags:
                        st.markdown(f"- {flag}")
                else:
                    st.markdown("""
                    <div class="info-box">
                        <strong>✅ No major credibility issues detected</strong>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Interpretation
                st.markdown("### 📊 Score Interpretation:")
                if score >= 70:
                    st.success("**High Credibility**: Content shows good credibility indicators.")
                elif score >= 40:
                    st.warning("**Medium Credibility**: Some concerns detected. Verify with additional sources.")
                else:
                    st.error("**Low Credibility**: Multiple red flags detected. Exercise caution.")
            
            else:
                st.warning("Please enter some text to analyze.")
    
    with tab2:
        st.header("Image Analysis")
        st.markdown("Upload an image for Error Level Analysis (ELA) and basic integrity checking.")
        
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['jpg', 'jpeg', 'png'],
            help="Upload JPG, JPEG, or PNG images for analysis"
        )
        
        if uploaded_file is not None:
            # Load image
            image = Image.open(uploaded_file)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Original Image")
                st.image(image, use_column_width=True)
                
                # Basic image info
                st.markdown("**Image Information:**")
                st.markdown(f"- Format: {image.format}")
                st.markdown(f"- Mode: {image.mode}")
                st.markdown(f"- Size: {image.size[0]} × {image.size[1]} pixels")
            
            with col2:
                st.markdown("#### ELA Analysis")
                
                with st.spinner("Performing ELA analysis..."):
                    ela_image, integrity_score = perform_ela_analysis(image)
                
                if ela_image:
                    st.image(ela_image, use_column_width=True)
                    st.caption("Bright areas indicate potential manipulation")
                else:
                    st.error("Failed to perform ELA analysis")
            
            # Metrics row
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="Integrity Score",
                    value=f"{integrity_score:.1f}/100"
                )
            
            with col2:
                # NSFW detection
                with st.spinner("Checking content..."):
                    skin_ratio, is_nsfw_flagged = detect_nsfw_heuristic(image)
                
                st.metric(
                    label="Skin Tone Ratio",
                    value=f"{skin_ratio:.2%}"
                )
            
            with col3:
                file_size = len(uploaded_file.getvalue()) / 1024  # KB
                st.metric(
                    label="File Size",
                    value=f"{file_size:.1f} KB"
                )
            
            # Analysis results
            st.markdown("### 🔍 Analysis Results:")
            
            if integrity_score >= 70:
                st.success("**High Integrity**: Image shows minimal signs of manipulation.")
            elif integrity_score >= 40:
                st.warning("**Medium Integrity**: Some inconsistencies detected.")
            else:
                st.error("**Low Integrity**: Significant manipulation indicators found.")
            
            if is_nsfw_flagged:
                st.markdown("""
                <div class="warning-box">
                    <strong>⚠️ Content Warning:</strong> Image may contain inappropriate content based on skin tone analysis.
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("### ℹ️ ELA Explanation:")
            st.markdown("""
            Error Level Analysis (ELA) highlights areas of an image that have different compression levels,
            which can indicate digital manipulation. In the ELA image:
            - **Bright areas**: Potentially edited or manipulated regions
            - **Dark areas**: Likely original, unmodified content
            - **Uniform brightness**: Consistent compression throughout
            """)
    
    with tab3:
        st.header("About TruthShield")
        
        st.markdown("""
        ### 🛡️ What is TruthShield?
        
        TruthShield is a **prototype** media credibility and integrity checker that uses heuristic-based analysis 
        to help users evaluate text content and images. This tool is designed for educational and research purposes.
        
        ### 🔧 Features
        
        **Text/Link Credibility Check:**
        - Analyzes text for sensational keywords and excessive punctuation
        - Evaluates domain trustworthiness
        - Provides credibility scoring based on multiple factors
        
        **Image Analysis:**
        - Error Level Analysis (ELA) for detecting potential manipulation
        - Basic integrity scoring
        - Simple content flagging based on skin tone ratios
        
        ### ⚠️ Important Limitations
        
        **This is a PROTOTYPE and NOT suitable for production use:**
        
        - **Heuristic-based only**: Uses simple rules, not advanced AI/ML models
        - **Limited accuracy**: May produce false positives and false negatives
        - **Not comprehensive**: Cannot detect all forms of misinformation or manipulation
        - **Educational purpose**: Designed to demonstrate concepts, not replace expert analysis
        
        ### 🎯 Intended Use
        
        - Educational demonstrations of credibility checking concepts
        - Research and development of media analysis tools
        - Understanding basic principles of content verification
        
        ### 🚫 NOT Suitable For
        
        - Professional fact-checking or journalism
        - Legal or forensic analysis
        - High-stakes decision making
        - Automated content moderation
        
        ### 🔬 Technical Details
        
        **Text Analysis:**
        - Keyword-based sentiment analysis
        - Domain reputation checking
        - Punctuation and capitalization analysis
        
        **Image Analysis:**
        - JPEG compression difference detection
        - Pixel-level variance calculation
        - Basic skin tone color space analysis
        
        ### 📚 Learn More
        
        To build more robust media verification tools, consider:
        - Advanced machine learning models
        - Blockchain-based provenance tracking  
        - Professional fact-checking databases
        - Reverse image search APIs
        - Natural language processing for deeper text analysis
        
        ### 🤝 Disclaimer
        
        This tool is provided "as is" without warranty. Users should always:
        - Verify information through multiple sources
        - Consult professional fact-checkers for important decisions
        - Understand the limitations of automated analysis
        - Use critical thinking alongside any automated tools
        """)
        
        st.markdown("---")
        st.markdown("*Built with Streamlit | Version 1.0 | Educational Prototype*")

if __name__ == "__main__":
    main()