# Fantasy Football Social - MVP

A social media platform for fantasy football players built with Streamlit and Sleeper API integration.

## Features

### Core Features
- **Multi-Platform Support**: Landing page for Sleeper, ESPN, Yahoo (only Sleeper functional in MVP)
- **Sleeper Integration**: Connect your Sleeper account and view all your 2025 leagues
- **Social Feed**: Post updates, share lineup decisions, and engage with other fantasy players
- **Roster Sharing**: Attach your full roster, starters, or specific players to posts
- **User Profiles**: Showcase your fantasy teams across multiple leagues
- **Cross-League Discovery**: Find and follow fantasy players beyond your immediate leagues
- **Activity Leaderboards**: See the most active users on the platform
- **Quick Team Viewer**: Sidebar widget to quickly reference your teams while browsing

### Post Types
- General discussion
- Lineup decisions
- Trade talk
- Victory laps
- Trash talk

### Privacy Controls
- **Post Visibility**: Choose between Public or Private when creating posts
  - **Public**: Anyone can see in public view mode
  - **Private**: Only followers can see (in both view modes)
- **View Modes**: Toggle between Public and Private feed views
  - **Public View**: See all public posts + private posts from people you follow
  - **Private View**: See only posts from people you follow (both public and private)
- **Visual Indicators**: Posts display 🌍 Public or 🔒 Private badges
- **Delete Posts**: Delete your own posts with the 🗑️ button

### Roster Features
- Share full roster with posts (expandable, not shown by default)
- Share only starters
- Select specific players to highlight
- Visual player cards with position and team info
- Injury status indicators

### League Details
- **League Format**: See scoring type (PPR/Half-PPR/Standard), team count, playoff teams
- **League Settings**: Waiver type, trade deadline, roster size
- **Live Standings**: Full league standings with win-loss records, win %, points for/against
- **Medals**: Top 3 teams get 🥇🥈🥉 medals
- Available in posts (when roster is shared) and on profile page

## Installation

1. Clone or download this project

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Demo with Test Data

To populate the app with test users and sample posts for demo purposes:

```bash
python create_test_data.py
```

This will create:
- 5 test users with different personas
- Sample posts of various types
- Follow relationships between users
- Likes and comments

You can then log in with any of these test usernames:
- `fantasy_guru`
- `the_commish`
- `waiver_wire_king`
- `taco_tuesday`
- `analytics_andy`

## How to Use

1. **Choose Platform**: Select Sleeper on the landing page (ESPN/Yahoo coming soon)

2. **Sign In**: Enter your Sleeper username
   - If you're new, an account will be automatically created
   - Your Sleeper leagues and stats will be pulled in automatically
   - Or use a test username if you ran `create_test_data.py`

3. **Explore Your Profile**:
   - View all your 2025 fantasy leagues
   - See your team records and points
   - **View League Details**: Click the expander to see:
     - League format (PPR/Half-PPR/Standard)
     - League settings (waiver type, trade deadline, etc.)
     - Full standings with medals for top 3 teams
   - Edit your bio
   - View your post history

4. **Set Your Feed View**:
   - Toggle between **Public** and **Private** view modes at the top of the feed
   - **Public**: See all public posts from anyone + private posts from your followers
   - **Private**: See only posts from people you follow

5. **Create Posts**:
   - Share your thoughts, lineup decisions, trades, or trash talk
   - **Choose Visibility**: Select Public (anyone can see) or Private (only followers)
   - **Attach roster/players**: Check the box to attach your team
     - Select which league
     - Choose full roster, starters only, or specific players
     - Roster appears as an **expandable section** in the post (click to view)
     - Players display with position, team, and injury status
   - Great for "Who do I start?" questions!
   - **Delete your posts**: Use the 🗑️ button on your own posts

6. **View Posts with Context**:
   - Posts display 🌍 Public or 🔒 Private badges
   - Posts with attached rosters have an expandable "📋 View Roster" section
   - Posts with league context have an expandable "ℹ️ League Details" section
   - See full standings and league format without leaving the feed

7. **Quick Team Reference**:
   - Expand "🏈 My Teams" in the sidebar
   - View your current lineup for any league
   - See your record and starters

8. **Discover Users**:
   - Find other fantasy players on the platform
   - Follow users to see their posts in your feed
   - View their bios and stats

9. **Engage**:
   - Like posts from other users
   - View comments (commenting feature ready in database)
   - Build your fantasy football social network

## Technical Details

### Stack
- **Frontend**: Streamlit
- **Database**: SQLite (local file-based)
- **API**: Sleeper Fantasy Football API
- **Language**: Python 3.8+

### Project Structure
```
fantasy-social-mvp/
├── app.py                 # Main Streamlit application
├── utils/
│   ├── database.py       # SQLite database operations
│   └── sleeper_api.py    # Sleeper API wrapper
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

### Database Schema
- **users**: User profiles linked to Sleeper accounts
- **posts**: Social media posts with type categorization
- **follows**: User follow relationships
- **comments**: Post comments (foundation for future enhancement)

## Future Enhancements

### Short Term
- Enhanced leaderboards with actual fantasy stats
- Comment functionality on posts
- Image/GIF uploads
- Trade proposal sharing
- Live scoring updates

### Medium Term
- Multi-season history
- League comparison tools
- Matchup predictions
- Trade analyzer integration
- Push notifications

### Long Term
- Mobile app (React Native)
- Direct messaging
- League creation within the platform
- Integration with other fantasy platforms (ESPN, Yahoo)
- Premium analytics features

## Development Notes

This is an MVP built to demonstrate the core concept. For production use, consider:

- User authentication (OAuth, JWT)
- Database migration to PostgreSQL
- API rate limiting and caching strategies
- Responsive mobile design
- Content moderation tools
- Performance optimization for larger user bases

## Sleeper API Resources

- [Sleeper API Documentation](https://docs.sleeper.app/)
- All Sleeper data is publicly accessible
- No API key required for public endpoints

## Support

For issues or questions about Sleeper integration, refer to the [Sleeper API docs](https://docs.sleeper.app/).

For app-specific issues, check the code comments or modify the source directly.

---

Built with Streamlit | Powered by Sleeper API
