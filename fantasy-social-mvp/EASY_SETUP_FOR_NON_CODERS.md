# 🏈 Fantasy Football Social - Setup for Non-Coders

Hey! Want to try out the Fantasy Football Social app? Here are the **easiest** ways to get started:

---

## ✨ Option 1: Just Use the Link (EASIEST)

If someone already deployed this, just:
1. Click the link they sent you
2. Enter your Sleeper username
3. Start posting!

**Don't have a Sleeper account?** Use one of these test accounts:
- Username: `fantasy_guru`
- Username: `the_commish`
- Username: `waiver_wire_king`
- Username: `taco_tuesday`
- Username: `analytics_andy`

---

## 💻 Option 2: Run on Your Computer (Needs Someone to Set Up Once)

### For the Tech-Savvy Person (One-Time Setup):

**On Mac:**
1. Open Terminal (search for "Terminal" on your Mac)
2. Copy and paste these commands one at a time, pressing Enter after each:

```bash
# Navigate to your Downloads or wherever you want the app
cd ~/Downloads

# Copy the fantasy-social-mvp folder here if you haven't already

# Go into the folder
cd fantasy-social-mvp

# Install Python dependencies
pip3 install -r requirements.txt

# Create test data (optional but recommended)
python3 create_test_data.py

# Run the app
streamlit run app.py
```

3. A browser window will open automatically!
4. If not, go to: http://localhost:8501

**On Windows:**
1. Open Command Prompt (search for "cmd")
2. Copy and paste these commands one at a time, pressing Enter after each:

```bash
# Navigate to where you put the app
cd Downloads\fantasy-social-mvp

# Install Python dependencies
pip install -r requirements.txt

# Create test data
python create_test_data.py

# Run the app
streamlit run app.py
```

3. A browser window will open automatically!
4. If not, go to: http://localhost:8501

### For the Non-Coder (After Setup):

Once someone sets it up once, you just need to:
1. Open Terminal (Mac) or Command Prompt (Windows)
2. Type:
   ```bash
   cd fantasy-social-mvp
   streamlit run app.py
   ```
3. Press Enter
4. Your browser opens with the app!

---

## 📱 What Can You Do?

1. **Sign In**: Enter your Sleeper username
2. **Create Posts**:
   - Choose Public or Private
   - Share your lineup decisions
   - Attach your roster to ask "Who do I start?"
3. **View Feed**:
   - Toggle between Public and Private views
   - See posts from other fantasy players
4. **Follow Users**: Build your fantasy network
5. **Check League Details**: See standings, formats, etc.

---

## ❓ Troubleshooting

**"Python is not recognized" or "command not found"?**
- You need to install Python first: https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

**"pip is not recognized"?**
- Python didn't install correctly
- Try reinstalling Python and check the PATH option

**"Sleeper username not found"?**
- Make sure you typed your username correctly
- Or use a test username: `fantasy_guru`

**App won't start?**
- Make sure you're in the right folder: `cd fantasy-social-mvp`
- Try running `pip install -r requirements.txt` again

**Database is empty?**
- Run: `python create_test_data.py` (or `python3` on Mac)
- This creates 5 test users with sample posts

---

## 🆘 Still Stuck?

Ask whoever shared this with you! They can either:
1. Deploy it online (free) so you just click a link
2. Set it up on your computer in 5 minutes
3. Share their screen and walk you through it

---

## 🎮 Pro Tips

- **Test Users**: Log in as different test users to see how following works
- **Public vs Private**: Try both view modes to see the difference
- **Roster Sharing**: Perfect for "Who do I start?" questions
- **League Details**: Check standings without leaving the app
- **Delete Posts**: Made a mistake? Just click the 🗑️ button

Enjoy! 🏈
