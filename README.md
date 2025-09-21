# 🛡️ TruthShield - Media Credibility Checker# TruthShield — Streamlit Demo (Prototype)



A prototype Streamlit application for analyzing text credibility and image integrity using heuristic-based methods.This repository contains a single-file Streamlit demo for TruthShield — a prototype for detecting misinformation, deepfakes, and non-consensual deepfake nudes (demo heuristics only).



## ⚠️ Important Notice## Files

- `app.py` — Streamlit application (text credibility, ELA image check, NSFW hint)

**This is a PROTOTYPE application for educational and demonstration purposes only.** It uses basic heuristics and is NOT suitable for production use, professional fact-checking, or high-stakes decision making.- `requirements.txt` — Python dependencies

- `.env` — Environment variables (create this if needed)

## 🚀 Features

## Deploy to Streamlit Cloud (Recommended)

### 📝 Text/Link Credibility Analysis1. Fork or create a new GitHub repository

- **Sensational Keyword Detection**: Identifies potentially biased or sensational language2. Push these files to your repository:

- **Domain Reputation**: Checks against known trusted and suspicious domains   ```bash

- **Writing Quality Assessment**: Analyzes capitalization, punctuation, and sentence structure   git init

- **Security Check**: Verifies HTTPS usage   git add app.py requirements.txt README.md

- **Credibility Scoring**: Provides 0-100 credibility score with detailed feedback   git commit -m "Initial commit"

   git remote add origin your-repo-url

### 🖼️ Image Analysis   git push -u origin main

- **Error Level Analysis (ELA)**: Detects potential digital manipulation through compression analysis   ```

- **Integrity Scoring**: Provides numerical assessment of image authenticity3. Go to https://share.streamlit.io and sign in

- **Content Flagging**: Basic NSFW detection using skin tone ratios4. Click "New app"

- **Technical Metadata**: Displays image format, size, and file information5. Select your repository, branch (main), and app.py as the main file

6. Click "Deploy"

### ℹ️ Educational Resources7. Wait for the build to complete (usually 2-3 minutes)

- Detailed explanations of analysis methods

- Limitations and proper use guidelines### Troubleshooting Deployment

- Technical implementation detailsIf you encounter deployment issues:

1. Check the build logs on Streamlit Cloud

## 🛠️ Installation & Local Development2. Ensure all dependencies are correctly listed in requirements.txt

3. Verify Python version compatibility (recommended: Python 3.9-3.11)

### Prerequisites4. Clear browser cache if the app doesn't update after deployment

- Python 3.8 or higher

- pip package manager## Deploy to Hugging Face Spaces (streamlit)

1. Create a new Space at https://huggingface.co/spaces (choose Streamlit).

### Quick Start2. Upload `app.py` and `requirements.txt` to the Space.

3. The Space will build and provide a public URL.

1. **Clone or download the repository**

   ```bash## Run locally

   git clone <your-repo-url>```bash

   cd truthshieldpython3 -m venv venv

   ```source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

2. **Install dependencies**streamlit run app.py

   ```bash```

   pip install -r requirements.txt

   ```## Important safety notes

This demo uses heuristics (ELA & a naive skin heuristic). **Do not** use this as a final detector for non-consensual content or legal actions. For production:

3. **Run the application**- Use vetted datasets & consent-checked training data,

   ```bash- Implement robust privacy, reporting & takedown workflows,

   streamlit run app.py- Add human review for any flagged content.

   ```

4. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If it doesn't open automatically, navigate to the URL shown in your terminal

## 🌐 Deployment Options

### Option 1: Streamlit Cloud (Recommended)

1. **Prepare your repository:**
   - Ensure all files (`app.py`, `requirements.txt`, `README.md`) are in your GitHub repository
   - Make sure the repository is public or you have Streamlit Cloud access to private repos

2. **Deploy to Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository, branch (usually `main`), and main file (`app.py`)
   - Click "Deploy"

3. **Configuration (if needed):**
   - No additional configuration required
   - The app will automatically install dependencies from `requirements.txt`

### Option 2: Hugging Face Spaces

1. **Create a new Space:**
   - Go to [huggingface.co/spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Choose "Streamlit" as the SDK
   - Set space name (e.g., `truthshield-demo`)

2. **Upload files:**
   - Upload `app.py`, `requirements.txt`, and `README.md` to your space
   - Ensure `app.py` is in the root directory

3. **Configuration:**
   - Create an `app.py` file (already provided)
   - The `requirements.txt` will be automatically detected
   - Your space will build and deploy automatically

## 📁 Project Structure

```
truthshield/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── .gitignore         # Git ignore file (optional)
```

## 🔧 Technical Implementation

### Text Analysis Features
- **Keyword Scoring**: Penalizes sensational language (-5 points per keyword)
- **Punctuation Analysis**: Detects excessive exclamation marks and questions
- **Capitalization Check**: Flags content with >15% capital letters
- **Domain Verification**: Trusted domains (+20 points), suspicious domains (-25 points)
- **Security Protocol**: HTTPS bonus (+5 points), HTTP penalty (-10 points)

### Image Analysis Features
- **ELA Processing**: JPEG compression difference analysis with brightness enhancement
- **Variance Calculation**: Statistical analysis of compression artifacts
- **Skin Tone Detection**: RGB color space analysis for content flagging
- **Integrity Scoring**: Normalized scoring based on pixel variance

## 📊 Dependencies

- **streamlit**: Web app framework
- **pillow**: Image processing and manipulation
- **numpy**: Numerical computing for image analysis
- **requests**: HTTP requests for potential future features

## ⚠️ Limitations & Disclaimers

### What This Tool IS:
- An educational demonstration of credibility checking concepts
- A prototype for understanding media analysis principles
- A starting point for more sophisticated analysis tools

### What This Tool IS NOT:
- A replacement for professional fact-checking
- Suitable for legal or forensic analysis
- Accurate enough for automated decision-making
- A comprehensive misinformation detection system

### Known Limitations:
- **False Positives**: May flag legitimate content as suspicious
- **False Negatives**: May miss sophisticated manipulation
- **Cultural Bias**: Domain and keyword lists may reflect cultural biases
- **Simple Heuristics**: Uses basic rules rather than AI/ML models
- **Limited Scope**: Cannot detect all forms of misinformation

## 🚀 Future Enhancements (Educational)

To build a production-ready system, consider:

- **Advanced ML Models**: Deep learning for text and image analysis
- **Multi-Modal Analysis**: Combined text-image credibility assessment
- **Real-Time Database**: Dynamic trusted/suspicious domain lists
- **Reverse Image Search**: Integration with reverse image search APIs
- **Social Media Integration**: Platform-specific credibility indicators
- **Blockchain Verification**: Cryptographic content provenance
- **Expert Integration**: Human fact-checker workflow tools

## 🤝 Contributing & Feedback

This is an educational prototype. For learning purposes, you might explore:

- Adding new heuristic rules
- Improving the user interface
- Implementing additional image analysis techniques
- Expanding the trusted domain database
- Adding support for different file formats

## 📄 License

This project is intended for educational use. Please respect appropriate usage guidelines and remember that this is a prototype tool.

## 🆘 Troubleshooting

### Common Issues:

1. **Import Errors**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Streamlit Not Found**
   ```bash
   pip install streamlit
   ```

3. **Image Upload Issues**
   - Ensure image files are in supported formats (JPG, JPEG, PNG)
   - Check file size limits (typically <200MB for Streamlit Cloud)

4. **Deployment Failures**
   - Verify all files are in the repository root
   - Check that `requirements.txt` has correct package versions
   - Ensure Python version compatibility (3.8+)

### Getting Help:

- Check the Streamlit [documentation](https://docs.streamlit.io)
- Review deployment platform specific guides
- Verify all dependencies are correctly specified

---

**Remember: This tool is for educational purposes only. Always verify information through multiple reliable sources and use critical thinking when evaluating media content.**