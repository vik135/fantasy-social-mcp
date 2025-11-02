# How to Deploy Fantasy Football Social Online (FREE)

This guide will help you deploy the app to Streamlit Cloud so anyone can access it via a URL.

## Step 1: Create a GitHub Account (if you don't have one)

1. Go to https://github.com
2. Click "Sign up"
3. Follow the instructions

## Step 2: Upload Your Code to GitHub

### Option A: Using GitHub Desktop (Easiest)
1. Download GitHub Desktop: https://desktop.github.com
2. Install and sign in with your GitHub account
3. Click "File" → "Add Local Repository"
4. Select the `fantasy-social-mvp` folder
5. Click "Publish repository"
6. Make sure "Keep this code private" is UNCHECKED (or checked if you want it private)
7. Click "Publish Repository"

### Option B: Using Terminal (If you're comfortable)
```bash
cd fantasy-social-mvp
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/fantasy-social-mvp.git
git push -u origin main
```

## Step 3: Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click "Sign up" and use your GitHub account
3. Click "New app"
4. Select:
   - **Repository**: `fantasy-social-mvp` (or whatever you named it)
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click "Deploy"
6. Wait 2-3 minutes for it to deploy

## Step 4: Share the URL

Once deployed, you'll get a URL like:
```
https://your-app-name.streamlit.app
```

Share this URL with anyone! They can:
- Create an account by entering their Sleeper username
- Or use test accounts: `fantasy_guru`, `the_commish`, etc.

## Troubleshooting

**App won't start?**
- Make sure `requirements.txt` is in the repository
- Check the logs in Streamlit Cloud dashboard

**Database issues?**
- The database will be empty initially
- First user to visit should run through signup
- You can create test data by adding a page to run `create_test_data.py`

**Want to update the app?**
- Just push changes to GitHub
- Streamlit Cloud will auto-deploy updates

## Making Updates

After deployment, to update the app:
1. Make changes to your local code
2. In GitHub Desktop: Write a summary, click "Commit to main"
3. Click "Push origin"
4. Streamlit Cloud auto-updates in ~1 minute

---

**Need help?** Check the Streamlit docs: https://docs.streamlit.io/streamlit-community-cloud
