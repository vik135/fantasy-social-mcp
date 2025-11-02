# Exact Commands to Deploy

## After creating your GitHub repo, run these:

```bash
# Connect to GitHub (replace YOUR_USERNAME with your actual GitHub username)
cd ~/fantasy-social-mvp
git remote add origin https://github.com/YOUR_USERNAME/fantasy-social-mvp.git

# Push your code
git push -u origin main
```

When prompted, enter your GitHub username and password.
(Note: GitHub might ask you to use a Personal Access Token instead of password)

## If you get a password error:

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Give it a name like "Streamlit Deploy"
4. Check "repo" scope
5. Click "Generate token"
6. Copy the token (you won't see it again!)
7. Use this token as your password when pushing

---

## Once pushed to GitHub:

1. Go to: https://share.streamlit.io
2. Click "Sign in with GitHub"
3. Click "New app"
4. Select:
   - Repository: fantasy-social-mvp
   - Branch: main
   - Main file path: app.py
5. Click "Deploy"
6. Wait 2-3 minutes
7. Get your URL! 🎉

It will look like: `https://your-username-fantasy-social-mvp.streamlit.app`
