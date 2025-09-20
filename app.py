import streamlit as st
from PIL import Image, ImageChops, ImageEnhance
import io
import re
import numpy as np

# Configure the Streamlit page
st.set_page_config(
    page_title="TruthShield — Demo",
    layout="centered",
    initial_sidebar_state="collapsed"
)
st.title("TruthShield — Misinformation & Deepfake Detector (Streamlit Demo)")
st.write("Prototype demo: text/link credibility check, image ELA visualization, and NSFW/deepfake hint.")

SENSATIONAL = [
    "shocking", "unbelievable", "you won't believe", "secret", "exposed",
    "breaking", "urgent", "miracle", "guaranteed", "click here", "free money"
]
TRUSTED_DOMAINS = ["thehindu.com", "indianexpress.com", "bbc.com", "reuters.com", "apnews.com", "factcheck.org"]

def text_score(text):
    t = (text or "").strip()
    score = 70
    rationale = []
    if not t:
        return 0, "No Input", ["No text provided"]

    low = t.lower()
    found_ks = [kw for kw in SENSATIONAL if kw in low]
    if found_ks:
        score -= 6 * len(found_ks)
        rationale.append(f"Sensational keywords found: {', '.join(found_ks)}")

    excl = low.count("!")
    if excl > 0:
        score -= min(5, excl) * 3
        rationale.append(f"Exclamation marks: {excl}")

    uppercase_chars = sum(1 for c in t if c.isupper())
    if uppercase_chars > max(10, len(t)//3):
        score -= 8
        rationale.append("Excessive uppercase characters")

    m = re.search(r"https?://([^/]+)/?", t)
    if m:
        domain = m.group(1).replace("www.", "")
        if domain in TRUSTED_DOMAINS:
            score += 10
            rationale.append(f"Trusted domain detected: {domain}")
        else:
            rationale.append(f"External domain detected: {domain} (not in trusted list)")

    score = max(0, min(100, score))
    label = "Real" if score >= 70 else ("Suspicious" if score >= 45 else "Likely Fake")
    return int(score), label, rationale

@st.cache_data(ttl=3600)  # Cache results for 1 hour
def ela_image(pil_img, quality=90):
    """Perform Error Level Analysis on the image."""
    try:
        if pil_img is None:
            raise ValueError("No image provided")
            
        img_rgb = pil_img.convert("RGB")
        buf = io.BytesIO()
        img_rgb.save(buf, "JPEG", quality=quality)
        buf.seek(0)
        jpg = Image.open(buf).convert("RGB")
        diff = ImageChops.difference(img_rgb, jpg)
        diff_enh = ImageEnhance.Brightness(diff).enhance(10.0)
        arr = np.array(diff_enh).astype(float)
        avg = arr.mean()
        score = 100 - min(90, avg)
        score = max(0.0, min(100.0, score))
        label = "Real" if score >= 70 else ("Suspicious" if score >= 45 else "Likely Manipulated")
        return diff_enh, float(score), label
    except ValueError as ve:
        st.error(str(ve))
        return None, 0.0, "Error"
    except Exception as e:
        st.error(f"Error analyzing image: {str(e)}")
        return None, 0.0, "Error"

@st.cache_data(ttl=3600)  # Cache results for 1 hour
def nsfw_hint(pil_img):
    """Analyze image for potential NSFW content using a simple heuristic."""
    try:
        if pil_img is None:
            raise ValueError("No image provided")
            
        small = pil_img.resize((64,64)).convert("RGB")
        arr = np.array(small).astype(int)
        skin_pixels = ((arr[:,:,0] > 100) & (arr[:,:,1] > 80) & (arr[:,:,2] > 60))
        ratio = skin_pixels.mean()
        return (ratio > 0.15), float(ratio)
    except ValueError as ve:
        st.error(str(ve))
        return False, 0.0
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return False, 0.0

tab1, tab2, tab3 = st.tabs(["Text / Link Check", "Image ELA & NSFW Hint", "About & Notes"])

with tab1:
    st.subheader("Text / Link Credibility Check")
    user_text = st.text_area("Paste headline, post text, or URL", height=140)
    if st.button("Verify Text"):
        if not user_text or not user_text.strip():
            st.warning("Please paste some text or a URL to verify.")
        else:
            score, label, rationale = text_score(user_text)
            st.metric("Credibility Score", f"{score}/100")
            st.markdown(f"**Verdict:** {label}")
            if rationale:
                st.markdown("**Rationale:**")
                for r in rationale:
                    st.write("- " + r)
            st.caption("Prototype heuristic. Replace with fine-tuned NLP model for production.")

with tab2:
    st.subheader("Image ELA (Error Level Analysis) & NSFW Hint")
    uploaded = st.file_uploader("Upload image (JPEG/PNG)", type=["jpg", "jpeg", "png"])
    if uploaded is not None:
        try:
            img = Image.open(uploaded)
            st.image(img, caption="Original", use_column_width=True)
            if st.button("Analyze Image"):
                ela_vis, integrity_score, ela_label = ela_image(img)
                nsfw_flag, nsfw_ratio = nsfw_hint(img)
                st.image(ela_vis, caption="ELA Visualization", use_column_width=True)
                st.metric("Integrity Score", f"{integrity_score:.1f}/100")
                st.markdown(f"**ELA Verdict:** {ela_label}")
                st.markdown(f"**NSFW Hint:** {'Yes 🚨' if nsfw_flag else 'No'} (skin-ratio={nsfw_ratio:.2f})")
                st.caption("ELA is a heuristic visualization. NSFW hint is a crude demo — do not rely on it for decisions.")
        except Exception as e:
            st.error("Could not process the uploaded image. Make sure it is a valid image file.")

with tab3:
    st.header("About this demo")
    st.write("""
**TruthShield (Streamlit Demo)** is a lightweight, single-file prototype intended for hackathon demonstration purposes.
It includes:
- A text/link credibility heuristic (quick demo),
- ELA visualization for images, and
- A naive NSFW/deepfake hint (skin-tone heuristic).

**Important:** This demo uses heuristics and is NOT suitable for production or legal enforcement.
For production, replace heuristics with:
- Fine-tuned RoBERTa/BERT for fake-news detection,
- Xception / Deepfake detectors (FaceForensics models) for vision,
- OpenNSFW2 or fine-tuned CNN for NSFW detection,
- Perceptual hashing + web search for traceback.
""")
