# Quick Start Guide

Get your Fantasy Football Social MVP running in 3 minutes!

## Step 1: Install Dependencies (30 seconds)

```bash
cd fantasy-social-mvp
pip install -r requirements.txt
```

## Step 2: Add Test Data (Optional - 10 seconds)

This creates demo users and posts so you can see the app in action:

```bash
python create_test_data.py
```

## Step 3: Run the App (5 seconds)

```bash
streamlit run app.py
```

The app will open in your browser automatically!

## Step 4: Log In

### Option A: Use Your Sleeper Account
1. Click "Connect Sleeper"
2. Enter your Sleeper username
3. Your leagues and teams will be pulled automatically

### Option B: Use Test Data (if you ran Step 2)
Log in with any of these usernames:
- `fantasy_guru` - The veteran player
- `the_commish` - League commissioner
- `waiver_wire_king` - Streaming expert
- `taco_tuesday` - The fun one
- `analytics_andy` - Data driven player

## What to Try

### 1. Create a Post with Your Roster
1. Go to "Feed"
2. Click "Create a post"
3. Check "📋 Attach roster/players to this post"
4. Select a league and choose what to share
5. Write something like "Who do I start this week?"
6. Post it!
7. Your roster will appear as an **expandable section** that others can click to view

### 2. Discover and Follow Users
1. Click "Discover" in the sidebar
2. Browse other fantasy players
3. Click "Follow" on interesting users
4. Their posts will show up in your feed

### 3. View Your Teams
1. Expand "🏈 My Teams" in the sidebar
2. See your current lineup and record
3. Switch between leagues if you have multiple

### 4. Check Your Profile & League Details
1. Click "My Profile"
2. View all your leagues with W-L records
3. **Click "ℹ️ View League Details & Standings"** to see:
   - League format (PPR/Half-PPR/Standard)
   - Number of teams and playoff spots
   - Full standings with win %, points for/against
   - Top 3 teams get medal emojis 🥇🥈🥉
4. Edit your bio
5. See your post history

## Next Steps

- Invite your league mates to join
- Post about your latest trades
- Share lineup decisions
- Celebrate wins (or commiserate losses)
- Build your cross-league fantasy network!

## Troubleshooting

**No leagues showing up?**
- Make sure you entered your Sleeper username correctly
- Check that you have 2025 leagues (the app looks for 2025 season)
- If you only have 2024 leagues, you can manually change the year in `app.py` line 274

**Test data not showing?**
- Make sure you ran `python create_test_data.py` before starting the app
- Try restarting the Streamlit app

**App won't start?**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check that you're in the `fantasy-social-mvp` directory

## Have Fun!

This is an MVP - the foundation for a full fantasy football social platform. Enjoy exploring and feel free to customize it!
