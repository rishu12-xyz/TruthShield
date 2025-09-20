# TruthShield — Streamlit Demo (Prototype)

This repository contains a single-file Streamlit demo for TruthShield — a prototype for detecting misinformation, deepfakes, and non-consensual deepfake nudes (demo heuristics only).

## Files
- `app.py` — Streamlit application (text credibility, ELA image check, NSFW hint)
- `requirements.txt` — Python dependencies
- `.env` — Environment variables (create this if needed)

## Deploy to Streamlit Cloud (Recommended)
1. Fork or create a new GitHub repository
2. Push these files to your repository:
   ```bash
   git init
   git add app.py requirements.txt README.md
   git commit -m "Initial commit"
   git remote add origin your-repo-url
   git push -u origin main
   ```
3. Go to https://share.streamlit.io and sign in
4. Click "New app"
5. Select your repository, branch (main), and app.py as the main file
6. Click "Deploy"
7. Wait for the build to complete (usually 2-3 minutes)

### Troubleshooting Deployment
If you encounter deployment issues:
1. Check the build logs on Streamlit Cloud
2. Ensure all dependencies are correctly listed in requirements.txt
3. Verify Python version compatibility (recommended: Python 3.9-3.11)
4. Clear browser cache if the app doesn't update after deployment

## Deploy to Hugging Face Spaces (streamlit)
1. Create a new Space at https://huggingface.co/spaces (choose Streamlit).
2. Upload `app.py` and `requirements.txt` to the Space.
3. The Space will build and provide a public URL.

## Run locally
```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Important safety notes
This demo uses heuristics (ELA & a naive skin heuristic). **Do not** use this as a final detector for non-consensual content or legal actions. For production:
- Use vetted datasets & consent-checked training data,
- Implement robust privacy, reporting & takedown workflows,
- Add human review for any flagged content.
