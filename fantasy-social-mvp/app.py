import streamlit as st
from utils.database import Database
from utils.sleeper_api import SleeperAPI

# Page configuration
st.set_page_config(
    page_title="Fantasy Football Social",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
if 'db' not in st.session_state:
    st.session_state.db = Database()

# Initialize session state
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1F4788;
        margin-bottom: 0.5rem;
    }
    .subheader {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .stat-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .stat-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1F4788;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #666;
    }
    .post-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    .post-header {
        display: flex;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    .post-author {
        font-weight: bold;
        color: #1F4788;
    }
    .post-time {
        color: #999;
        font-size: 0.85rem;
    }
    .post-content {
        color: #000000;
        font-size: 1rem;
        line-height: 1.5;
    }
    .player-card {
        background-color: #f8f9fa;
        padding: 0.5rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .player-name {
        color: #000000;
        font-weight: bold;
    }
    .player-info {
        color: #333333;
        font-size: 0.85rem;
    }
    .league-badge {
        background-color: #1F4788;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.85rem;
        display: inline-block;
        margin: 0.25rem;
    }
    .platform-card {
        text-align: center;
        padding: 2rem;
        border: 2px solid #1F4788;
        border-radius: 1rem;
        background-color: #f8f9fa;
        cursor: pointer;
        transition: all 0.3s;
    }
    .platform-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    .platform-card-disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }
    .platform-title {
        color: #000000;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    .platform-subtitle {
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

def login_page():
    """Login/Signup page with platform selection"""
    st.markdown('<p class="main-header">🏈 Fantasy Football Social</p>', unsafe_allow_html=True)
    st.markdown('<p class="subheader">Connect with fantasy players across all your leagues</p>', unsafe_allow_html=True)

    # Initialize platform selection state
    if 'selected_platform' not in st.session_state:
        st.session_state.selected_platform = None

    if st.session_state.selected_platform is None:
        # Platform selection landing page
        st.markdown("### Choose Your Platform")
        st.markdown("Connect your fantasy football account to get started")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown('<div class="platform-card">', unsafe_allow_html=True)
            # Try to load Sleeper logo, fall back to emoji if not found
            try:
                st.image("assets/sleeper-logo.png", width=100)
            except:
                st.markdown("### 💤")
            st.markdown('<p class="platform-title">Sleeper</p>', unsafe_allow_html=True)
            st.markdown('<p class="platform-subtitle">Best API support</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            if st.button("Connect Sleeper", type="primary", use_container_width=True):
                st.session_state.selected_platform = "sleeper"
                st.rerun()

        with col2:
            st.markdown('<div class="platform-card platform-card-disabled">', unsafe_allow_html=True)
            st.markdown("### 📺")
            st.markdown('<p class="platform-title">ESPN</p>', unsafe_allow_html=True)
            st.markdown('<p class="platform-subtitle">Coming Soon</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.button("Connect ESPN", use_container_width=True, disabled=True)

        with col3:
            st.markdown('<div class="platform-card platform-card-disabled">', unsafe_allow_html=True)
            st.markdown("### 🟣")
            st.markdown('<p class="platform-title">Yahoo</p>', unsafe_allow_html=True)
            st.markdown('<p class="platform-subtitle">Coming Soon</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.button("Connect Yahoo", use_container_width=True, disabled=True)

        st.markdown("---")
        st.markdown("""
        **Why Fantasy Football Social?**
        - 📊 Showcase your teams across multiple leagues and platforms
        - 🗣️ Connect with fantasy players beyond your league
        - 🏆 Compare stats and celebrate wins
        - 💬 Share lineup decisions and get feedback from the community
        - 🎯 Ask "Who do I start?" with full roster context
        """)

    else:
        # Sleeper login form
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            if st.button("← Back to platform selection"):
                st.session_state.selected_platform = None
                st.rerun()

            st.markdown("### Connect Sleeper Account")
            st.markdown("Enter your Sleeper username to get started")

            sleeper_username = st.text_input("Sleeper Username", placeholder="your_sleeper_username")

            if st.button("Continue", type="primary", use_container_width=True):
                if sleeper_username:
                    with st.spinner("Connecting to Sleeper..."):
                        # Fetch user from Sleeper
                        sleeper_user = SleeperAPI.get_user(sleeper_username)

                        if sleeper_user:
                            # Check if user exists in our database
                            db_user = st.session_state.db.get_user_by_sleeper_username(sleeper_username)

                            if not db_user:
                                # Create new user
                                user_id = st.session_state.db.create_user(
                                    sleeper_username=sleeper_username,
                                    sleeper_user_id=sleeper_user['user_id'],
                                    display_name=sleeper_user.get('display_name', sleeper_username),
                                    avatar_url=sleeper_user.get('avatar')
                                )
                                db_user = st.session_state.db.get_user_by_id(user_id)
                                st.success("Account created! Welcome to Fantasy Football Social!")
                            else:
                                st.success(f"Welcome back, {db_user['display_name']}!")

                            st.session_state.current_user = db_user
                            st.session_state.selected_platform = None  # Reset for next login
                            st.rerun()
                        else:
                            st.error("Sleeper username not found. Please check and try again.")
                else:
                    st.warning("Please enter your Sleeper username")

def main_app():
    """Main application with navigation"""
    # Sidebar navigation
    with st.sidebar:
        st.markdown(f"### Welcome, {st.session_state.current_user['display_name']}!")

        # User stats
        stats = st.session_state.db.get_user_stats(st.session_state.current_user['id'])
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Posts", stats['posts'])
        with col2:
            st.metric("Following", stats['following'])
        with col3:
            st.metric("Followers", stats['followers'])

        st.markdown("---")

        # Navigation
        page = st.radio(
            "Navigate",
            ["Feed", "My Profile", "Discover", "Leaderboards"],
            label_visibility="collapsed"
        )

        st.markdown("---")

        # Quick roster viewer
        with st.expander("🏈 My Teams"):
            user = st.session_state.current_user
            leagues = SleeperAPI.get_user_leagues(user['sleeper_user_id'], "nfl", "2025")

            if leagues and len(leagues) > 0:
                # Select league
                if len(leagues) == 1:
                    selected_league = leagues[0]
                else:
                    league_names = [f"{league['name']}" for league in leagues]
                    selected_idx = st.selectbox("League:", range(len(league_names)), format_func=lambda x: league_names[x], key="sidebar_league_select")
                    selected_league = leagues[selected_idx]

                # Get and display roster
                roster = SleeperAPI.get_user_roster_in_league(user['sleeper_user_id'], selected_league['league_id'])
                if roster:
                    all_players = SleeperAPI.get_all_players()
                    roster_with_names = SleeperAPI.get_roster_with_names(roster, all_players)

                    # Show record
                    wins = roster.get('settings', {}).get('wins', 0)
                    losses = roster.get('settings', {}).get('losses', 0)
                    st.caption(f"Record: {wins}-{losses}")

                    # Show starters
                    if 'starter_details' in roster_with_names and roster_with_names['starter_details']:
                        st.markdown("**Starters:**")
                        for player in roster_with_names['starter_details'][:5]:  # Show first 5
                            st.caption(f"• {player['name']} ({player['position']})")
                        if len(roster_with_names['starter_details']) > 5:
                            st.caption(f"... and {len(roster_with_names['starter_details']) - 5} more")
            else:
                st.caption("No leagues found for 2025")

        st.markdown("---")

        if st.button("Logout", use_container_width=True):
            st.session_state.current_user = None
            st.rerun()

    # Main content area
    if page == "Feed":
        show_feed()
    elif page == "My Profile":
        show_profile()
    elif page == "Discover":
        show_discover()
    elif page == "Leaderboards":
        show_leaderboards()

def show_feed():
    """Show social feed"""
    st.markdown('<p class="main-header">Feed</p>', unsafe_allow_html=True)

    # View mode toggle
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**Feed View:**")
    with col2:
        view_mode = st.radio(
            "View Mode",
            ["Public", "Private"],
            horizontal=True,
            label_visibility="collapsed",
            help="Public: See all public posts + private posts from followers | Private: See only posts from people you follow"
        )

    st.markdown("---")

    # Create post section
    with st.expander("Create a post", expanded=False):
        post_content = st.text_area("What's on your mind?", placeholder="Share your latest trade, lineup decision, or trash talk...")

        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            post_type = st.selectbox("Post type", ["General", "Lineup Decision", "Trade Talk", "Victory Lap", "Trash Talk"])
        with col2:
            post_visibility = st.radio("Visibility", ["Public", "Private"], horizontal=True, help="Public: Anyone can see | Private: Only followers can see")

        # Option to attach roster/players
        attach_roster = st.checkbox("📋 Attach roster/players to this post")

        post_metadata = None
        selected_league_id = None

        if attach_roster:
            st.markdown("**Select a league to share from:**")
            user = st.session_state.current_user
            leagues = SleeperAPI.get_user_leagues(user['sleeper_user_id'], "nfl", "2025")

            if leagues:
                league_options = {f"{league['name']}": league['league_id'] for league in leagues}
                selected_league_name = st.selectbox("Choose league", list(league_options.keys()))
                selected_league_id = league_options[selected_league_name]

                # Get roster for this league
                roster = SleeperAPI.get_user_roster_in_league(user['sleeper_user_id'], selected_league_id)

                if roster:
                    # Load player data
                    all_players = SleeperAPI.get_all_players()
                    roster_with_names = SleeperAPI.get_roster_with_names(roster, all_players)

                    share_option = st.radio("What to share:", ["Full Roster", "Starters Only", "Select Specific Players"])

                    if share_option == "Full Roster" and 'player_details' in roster_with_names:
                        post_metadata = {
                            'league_id': selected_league_id,
                            'league_name': selected_league_name,
                            'share_type': 'full_roster',
                            'players': roster_with_names['player_details']
                        }
                        st.caption(f"📋 Will share all {len(roster_with_names['player_details'])} players")

                    elif share_option == "Starters Only" and 'starter_details' in roster_with_names:
                        post_metadata = {
                            'league_id': selected_league_id,
                            'league_name': selected_league_name,
                            'share_type': 'starters',
                            'players': roster_with_names['starter_details']
                        }
                        st.caption(f"🏈 Will share {len(roster_with_names['starter_details'])} starters")

                    elif share_option == "Select Specific Players" and 'player_details' in roster_with_names:
                        player_names = [f"{p['name']} ({p['position']} - {p['team']})" for p in roster_with_names['player_details']]
                        selected_players_names = st.multiselect("Choose players:", player_names)

                        if selected_players_names:
                            selected_players = [
                                roster_with_names['player_details'][player_names.index(name)]
                                for name in selected_players_names
                            ]
                            post_metadata = {
                                'league_id': selected_league_id,
                                'league_name': selected_league_name,
                                'share_type': 'selected',
                                'players': selected_players
                            }
                            st.caption(f"👥 Will share {len(selected_players)} selected players")
            else:
                st.info("No leagues found for 2025. Join a league on Sleeper first!")

        with col3:
            if st.button("Post", type="primary", use_container_width=True):
                if post_content:
                    st.session_state.db.create_post(
                        user_id=st.session_state.current_user['id'],
                        content=post_content,
                        post_type=post_type.lower().replace(" ", "_"),
                        league_id=selected_league_id,
                        metadata=post_metadata,
                        visibility=post_visibility.lower()
                    )
                    st.success("Posted!")
                    st.rerun()
                else:
                    st.warning("Please enter some content")

    st.markdown("---")

    # Show feed
    feed = st.session_state.db.get_feed_for_user(
        st.session_state.current_user['id'],
        view_mode=view_mode.lower()
    )

    if not feed:
        if view_mode == "Private":
            st.info("Your private feed is empty! Follow some users to see their posts, or switch to Public view.")
        else:
            st.info("The feed is empty! Be the first to post something, or check out the Discover page.")
    else:
        for post in feed:
            show_post(post)

def show_league_details(league_id: str):
    """Display detailed league information including format and standings"""
    league = SleeperAPI.get_league(league_id)
    if not league:
        st.error("Could not load league details")
        return

    # League format details
    st.markdown("**League Format:**")
    col1, col2, col3 = st.columns(3)

    with col1:
        scoring = league.get('scoring_settings', {})
        if scoring.get('rec') == 1:
            format_type = "PPR"
        elif scoring.get('rec') == 0.5:
            format_type = "Half PPR"
        else:
            format_type = "Standard"
        st.metric("Scoring", format_type)

    with col2:
        num_teams = league.get('total_rosters', 'N/A')
        st.metric("Teams", num_teams)

    with col3:
        playoff_teams = league.get('settings', {}).get('playoff_teams', 'N/A')
        st.metric("Playoff Teams", playoff_teams)

    # League settings
    st.markdown("**Settings:**")
    settings_col1, settings_col2 = st.columns(2)

    with settings_col1:
        st.caption(f"🔄 Waiver Type: {league.get('settings', {}).get('waiver_type', 'N/A')}")
        st.caption(f"📅 Trade Deadline: Week {league.get('settings', {}).get('trade_deadline', 'N/A')}")

    with settings_col2:
        roster_positions = league.get('roster_positions', [])
        if roster_positions:
            st.caption(f"📋 Roster Size: {len(roster_positions)} positions")

    # Standings
    st.markdown("---")
    st.markdown("**Standings:**")

    rosters = SleeperAPI.get_league_rosters(league_id)
    users = SleeperAPI.get_league_users(league_id)

    if rosters and users:
        # Create user lookup
        user_lookup = {user['user_id']: user for user in users}

        # Build standings list
        standings = []
        for roster in rosters:
            owner_id = roster.get('owner_id')
            user = user_lookup.get(owner_id, {})

            standings.append({
                'team': user.get('display_name', 'Unknown'),
                'wins': roster.get('settings', {}).get('wins', 0),
                'losses': roster.get('settings', {}).get('losses', 0),
                'ties': roster.get('settings', {}).get('ties', 0),
                'points_for': roster.get('settings', {}).get('fpts', 0) + roster.get('settings', {}).get('fpts_decimal', 0) / 100,
                'points_against': roster.get('settings', {}).get('fpts_against', 0) + roster.get('settings', {}).get('fpts_against_decimal', 0) / 100
            })

        # Sort by wins (descending), then by points_for
        standings.sort(key=lambda x: (x['wins'], x['points_for']), reverse=True)

        # Display standings
        for idx, team in enumerate(standings, 1):
            win_pct = team['wins'] / (team['wins'] + team['losses']) if (team['wins'] + team['losses']) > 0 else 0

            # Medal emoji for top 3
            medal = ""
            if idx == 1:
                medal = "🥇 "
            elif idx == 2:
                medal = "🥈 "
            elif idx == 3:
                medal = "🥉 "

            st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 0.75rem; border-radius: 0.5rem; margin-bottom: 0.5rem;">
                <span style="color: #000000; font-weight: bold;">{medal}#{idx} {team['team']}</span><br>
                <span style="color: #333333; font-size: 0.9rem;">
                    {team['wins']}-{team['losses']}{f"-{team['ties']}" if team['ties'] > 0 else ""}
                    ({win_pct:.1%}) |
                    PF: {team['points_for']:.1f} |
                    PA: {team['points_against']:.1f}
                </span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Standings not available")

def show_post(post):
    """Display a single post"""
    import json

    st.markdown(f"""
    <div class="post-card">
        <div class="post-header">
            <span class="post-author">@{post['sleeper_username']}</span>
            <span style="margin-left: auto;" class="post-time">{post['created_at']}</span>
        </div>
        <p class="post-content">{post['content']}</p>
        <div style="margin-top: 1rem;">
            <span style="background-color: #f0f2f6; padding: 0.25rem 0.5rem; border-radius: 0.25rem; font-size: 0.85rem; color: #333;">
                {post['post_type'].replace('_', ' ').title()}
            </span>
            <span style="background-color: {'#e3f2fd' if post.get('visibility') == 'public' else '#fff3e0'}; color: {'#1976d2' if post.get('visibility') == 'public' else '#f57c00'}; padding: 0.25rem 0.5rem; border-radius: 0.25rem; font-size: 0.85rem; margin-left: 0.5rem;">
                {'🌍 Public' if post.get('visibility') == 'public' else '🔒 Private'}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Show attached roster/players and league details if metadata exists
    if post.get('metadata'):
        try:
            metadata = json.loads(post['metadata']) if isinstance(post['metadata'], str) else post['metadata']

            if metadata and 'players' in metadata:
                players = metadata['players']
                player_count = len(players) if players else 0

                with st.expander(f"📋 View {metadata.get('share_type', 'roster').replace('_', ' ').title()} ({player_count} players) - {metadata.get('league_name', 'League')}"):
                    # Display players in a nice table format
                    if players:
                        cols_per_row = 2
                        for i in range(0, len(players), cols_per_row):
                            cols = st.columns(cols_per_row)
                            for j, col in enumerate(cols):
                                if i + j < len(players):
                                    player = players[i + j]
                                    with col:
                                        status_emoji = "🟢" if player.get('status') == 'Active' else "🔴"
                                        st.markdown(f"""
                                        <div class="player-card">
                                            {status_emoji} <span class="player-name">{player['name']}</span><br>
                                            <span class="player-info">{player['position']} - {player['team']}</span>
                                        </div>
                                        """, unsafe_allow_html=True)

            # Show league details if league_id is present
            if metadata and metadata.get('league_id'):
                with st.expander(f"ℹ️ League Details - {metadata.get('league_name', 'League')}"):
                    show_league_details(metadata['league_id'])

        except (json.JSONDecodeError, KeyError, TypeError):
            pass  # Ignore if metadata is malformed
    elif post.get('league_id'):
        # Show league details even if no roster is attached
        league = SleeperAPI.get_league(post['league_id'])
        if league:
            with st.expander(f"ℹ️ League Details - {league.get('name', 'League')}"):
                show_league_details(post['league_id'])

    # Like, comment, and delete actions
    # Check if post belongs to current user
    is_own_post = post.get('user_id') == st.session_state.current_user['id']

    if is_own_post:
        col1, col2, col3, col4 = st.columns([1, 1, 1, 7])
    else:
        col1, col2, col4 = st.columns([1, 1, 8])
        col3 = None

    with col1:
        if st.button(f"👍 {post['likes']}", key=f"like_{post['id']}"):
            st.session_state.db.like_post(post['id'])
            st.rerun()
    with col2:
        comments = st.session_state.db.get_comments(post['id'])
        st.button(f"💬 {len(comments)}", key=f"comment_btn_{post['id']}")

    # Show delete button only for user's own posts
    if is_own_post and col3:
        with col3:
            if st.button("🗑️ Delete", key=f"delete_{post['id']}", type="secondary"):
                if st.session_state.db.delete_post(post['id'], st.session_state.current_user['id']):
                    st.success("Post deleted!")
                    st.rerun()
                else:
                    st.error("Failed to delete post")

def show_profile():
    """Show user profile with Sleeper leagues"""
    st.markdown('<p class="main-header">My Profile</p>', unsafe_allow_html=True)

    user = st.session_state.current_user

    # Profile header
    col1, col2 = st.columns([1, 3])
    with col1:
        if user['avatar_url']:
            st.image(f"https://sleepercdn.com/avatars/thumbs/{user['avatar_url']}", width=150)
    with col2:
        st.markdown(f"### {user['display_name']}")
        st.markdown(f"@{user['sleeper_username']}")

        stats = st.session_state.db.get_user_stats(user['id'])
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown(f'<div class="stat-box"><div class="stat-value">{stats["posts"]}</div><div class="stat-label">Posts</div></div>', unsafe_allow_html=True)
        with col_b:
            st.markdown(f'<div class="stat-box"><div class="stat-value">{stats["following"]}</div><div class="stat-label">Following</div></div>', unsafe_allow_html=True)
        with col_c:
            st.markdown(f'<div class="stat-box"><div class="stat-value">{stats["followers"]}</div><div class="stat-label">Followers</div></div>', unsafe_allow_html=True)

    # Edit bio
    with st.expander("Edit Profile"):
        new_bio = st.text_area("Bio", value=user.get('bio', ''), placeholder="Tell us about your fantasy football journey...")
        if st.button("Save"):
            st.session_state.db.update_user(user['id'], bio=new_bio)
            st.success("Profile updated!")
            st.rerun()

    st.markdown("---")

    # Show Sleeper leagues
    st.markdown("### My Leagues (2025)")

    leagues = SleeperAPI.get_user_leagues(user['sleeper_user_id'], "nfl", "2025")

    if leagues:
        for league in leagues:
            with st.container():
                st.markdown(f"#### {league['name']}")

                # Get user's roster in this league
                roster = SleeperAPI.get_user_roster_in_league(user['sleeper_user_id'], league['league_id'])

                if roster:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Wins", roster.get('settings', {}).get('wins', 0))
                    with col2:
                        st.metric("Losses", roster.get('settings', {}).get('losses', 0))
                    with col3:
                        st.metric("Points For", f"{roster.get('settings', {}).get('fpts', 0):.1f}")

                # Add league details expander
                with st.expander("ℹ️ View League Details & Standings"):
                    show_league_details(league['league_id'])

                st.markdown("---")
    else:
        st.info("No leagues found for 2024 season. Join some leagues on Sleeper!")

    st.markdown("---")

    # Show user's posts
    st.markdown("### My Posts")
    user_posts = st.session_state.db.get_posts(user_id=user['id'])

    if user_posts:
        for post in user_posts:
            show_post(post)
    else:
        st.info("You haven't posted anything yet!")

def show_discover():
    """Show user discovery page"""
    st.markdown('<p class="main-header">Discover Players</p>', unsafe_allow_html=True)

    st.markdown("Find and follow other fantasy football players")

    # Get all users
    all_users = st.session_state.db.get_all_users()
    current_user_id = st.session_state.current_user['id']

    # Filter out current user
    other_users = [u for u in all_users if u['id'] != current_user_id]

    if other_users:
        for user in other_users:
            with st.container():
                col1, col2, col3 = st.columns([2, 4, 2])

                with col1:
                    if user['avatar_url']:
                        st.image(f"https://sleepercdn.com/avatars/thumbs/{user['avatar_url']}", width=80)

                with col2:
                    st.markdown(f"**{user['display_name']}**")
                    st.markdown(f"@{user['sleeper_username']}")
                    if user.get('bio'):
                        st.markdown(f"_{user['bio']}_")

                    # Show user stats
                    stats = st.session_state.db.get_user_stats(user['id'])
                    st.caption(f"{stats['posts']} posts • {stats['followers']} followers")

                with col3:
                    is_following = st.session_state.db.is_following(current_user_id, user['id'])

                    if is_following:
                        if st.button("Unfollow", key=f"unfollow_{user['id']}", use_container_width=True):
                            st.session_state.db.unfollow_user(current_user_id, user['id'])
                            st.rerun()
                    else:
                        if st.button("Follow", key=f"follow_{user['id']}", type="primary", use_container_width=True):
                            st.session_state.db.follow_user(current_user_id, user['id'])
                            st.rerun()

                st.markdown("---")
    else:
        st.info("No other users yet. Invite your league mates!")

def show_leaderboards():
    """Show cross-league leaderboards"""
    st.markdown('<p class="main-header">Leaderboards</p>', unsafe_allow_html=True)

    st.markdown("### Coming Soon!")
    st.info("""
    Cross-league leaderboards will show:
    - Top performers across all connected leagues
    - Best win percentages
    - Highest scoring teams
    - Most active users on the platform

    For now, check out individual profiles to see their league stats!
    """)

    # Show most active users
    st.markdown("### Most Active Users")

    all_users = st.session_state.db.get_all_users()
    user_activity = []

    for user in all_users:
        stats = st.session_state.db.get_user_stats(user['id'])
        user_activity.append({
            'user': user,
            'total_activity': stats['posts'] + stats['followers']
        })

    # Sort by activity
    user_activity.sort(key=lambda x: x['total_activity'], reverse=True)

    for idx, item in enumerate(user_activity[:10], 1):
        user = item['user']
        st.markdown(f"**#{idx}** @{user['sleeper_username']} - {item['total_activity']} activity points")

# Main app logic
if st.session_state.current_user is None:
    login_page()
else:
    main_app()
