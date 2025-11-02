"""
Script to populate the database with test users and posts for demo purposes
"""
from utils.database import Database
from utils.sleeper_api import SleeperAPI
import random

def create_test_data():
    """Create test users and posts"""
    db = Database()

    # List of real Sleeper users for testing (public accounts)
    # These are example usernames - replace with real ones or use your own
    test_sleeper_usernames = [
        "testuser1",
        "testuser2",
        "testuser3"
    ]

    # Create test users without Sleeper integration
    test_users = [
        {
            'sleeper_username': 'fantasy_guru',
            'sleeper_user_id': 'test_user_1',
            'display_name': 'Fantasy Guru',
            'bio': 'Been playing fantasy for 10+ years. Always looking for that championship!',
            'avatar_url': None
        },
        {
            'sleeper_username': 'the_commish',
            'sleeper_user_id': 'test_user_2',
            'display_name': 'The Commissioner',
            'bio': 'Commissioner of 5 leagues. Ask me about league settings!',
            'avatar_url': None
        },
        {
            'sleeper_username': 'waiver_wire_king',
            'sleeper_user_id': 'test_user_3',
            'display_name': 'Waiver Wire King',
            'bio': 'Streaming D/ST and finding hidden gems since 2015',
            'avatar_url': None
        },
        {
            'sleeper_username': 'taco_tuesday',
            'sleeper_user_id': 'test_user_4',
            'display_name': 'Taco Tuesday',
            'bio': 'I drafted a kicker in round 3 and I\'m not sorry',
            'avatar_url': None
        },
        {
            'sleeper_username': 'analytics_andy',
            'sleeper_user_id': 'test_user_5',
            'display_name': 'Analytics Andy',
            'bio': 'Living and dying by the projections',
            'avatar_url': None
        }
    ]

    print("Creating test users...")
    user_ids = []
    for user_data in test_users:
        user_id = db.create_user(
            sleeper_username=user_data['sleeper_username'],
            sleeper_user_id=user_data['sleeper_user_id'],
            display_name=user_data['display_name'],
            bio=user_data['bio'],
            avatar_url=user_data['avatar_url']
        )

        if user_id:
            user_ids.append(user_id)
            print(f"✓ Created user: {user_data['display_name']} (ID: {user_id})")
        else:
            # User already exists, get their ID
            existing = db.get_user_by_sleeper_username(user_data['sleeper_username'])
            if existing:
                user_ids.append(existing['id'])
                print(f"  User already exists: {user_data['display_name']}")

    # Create some sample posts
    print("\nCreating test posts...")
    sample_posts = [
        {
            'user_idx': 0,  # fantasy_guru
            'content': "Just made the trade of the season! Gave up my RB2 for a potential league winner. Am I crazy or genius?",
            'post_type': 'trade_talk',
            'visibility': 'public'
        },
        {
            'user_idx': 1,  # the_commish
            'content': "PSA: Waiver claims process tonight at midnight. Good luck everyone!",
            'post_type': 'general',
            'visibility': 'public'
        },
        {
            'user_idx': 2,  # waiver_wire_king
            'content': "Picking up the Panthers D/ST for next week's matchup. They play the worst offense in the league!",
            'post_type': 'lineup_decision',
            'visibility': 'public'
        },
        {
            'user_idx': 0,  # fantasy_guru
            'content': "Three weeks in a row as the highest scorer. This is my year! 🏆",
            'post_type': 'victory_lap',
            'visibility': 'public'
        },
        {
            'user_idx': 3,  # taco_tuesday
            'content': "Started my RB1 on his bye week. AMA.",
            'post_type': 'trash_talk',
            'visibility': 'public'
        },
        {
            'user_idx': 4,  # analytics_andy
            'content': "The projections said this was a smash spot. The projections lied.",
            'post_type': 'general',
            'visibility': 'private'
        },
        {
            'user_idx': 2,  # waiver_wire_king
            'content': "Who do I start this week: Player A with tough matchup but high target share, or Player B with easier matchup but lower usage?",
            'post_type': 'lineup_decision',
            'visibility': 'private'
        },
        {
            'user_idx': 1,  # the_commish
            'content': "Considering switching to 0.5 PPR next season. Thoughts?",
            'post_type': 'general',
            'visibility': 'public'
        },
        {
            'user_idx': 0,  # fantasy_guru
            'content': "My opponent has 3 players on Monday night and I'm up by 15. Sweating bullets right now...",
            'post_type': 'general',
            'visibility': 'private'
        },
        {
            'user_idx': 3,  # taco_tuesday
            'content': "Just realized my 'sleeper pick' has been on IR since week 2. Maybe that's why they call it Sleeper?",
            'post_type': 'trash_talk',
            'visibility': 'public'
        }
    ]

    for post_data in sample_posts:
        if post_data['user_idx'] < len(user_ids):
            post_id = db.create_post(
                user_id=user_ids[post_data['user_idx']],
                content=post_data['content'],
                post_type=post_data['post_type'],
                visibility=post_data.get('visibility', 'public')
            )
            print(f"✓ Created post ID {post_id}")

    # Create some follow relationships
    print("\nCreating follow relationships...")
    if len(user_ids) >= 3:
        # User 1 follows users 2 and 3
        db.follow_user(user_ids[0], user_ids[1])
        db.follow_user(user_ids[0], user_ids[2])

        # User 2 follows user 1 and 3
        db.follow_user(user_ids[1], user_ids[0])
        db.follow_user(user_ids[1], user_ids[2])

        # User 3 follows everyone
        for i in range(len(user_ids)):
            if i != 2:
                db.follow_user(user_ids[2], user_ids[i])

        # Some random follows
        if len(user_ids) >= 5:
            db.follow_user(user_ids[3], user_ids[0])
            db.follow_user(user_ids[4], user_ids[0])
            db.follow_user(user_ids[4], user_ids[2])

        print("✓ Follow relationships created")

    # Add some likes to posts
    print("\nAdding likes to posts...")
    posts = db.get_posts(limit=100)
    for post in posts[:5]:  # Like first 5 posts
        for _ in range(random.randint(1, 8)):
            db.like_post(post['id'])
    print("✓ Likes added")

    # Add some comments
    print("\nAdding comments...")
    sample_comments = [
        "Great trade! I think you won that one.",
        "Not sure about that decision but good luck!",
        "This is wild! 😂",
        "I'm doing the same thing in my league",
        "Have you considered the matchup though?",
        "Terrible take lol",
        "This aged well",
        "Same boat, so stressful!",
    ]

    if len(posts) > 0 and len(user_ids) > 0:
        for i, post in enumerate(posts[:5]):
            # Add 1-3 comments to each of the first 5 posts
            num_comments = random.randint(1, 3)
            for _ in range(num_comments):
                commenter_id = random.choice(user_ids)
                comment_text = random.choice(sample_comments)
                db.add_comment(post['id'], commenter_id, comment_text)
        print("✓ Comments added")

    print("\n✅ Test data creation complete!")
    print(f"\nCreated:")
    print(f"  - {len(user_ids)} test users")
    print(f"  - {len(sample_posts)} test posts")
    print(f"  - Multiple follow relationships")
    print(f"  - Likes and comments")
    print(f"\nYou can now log in with any of these test usernames:")
    for user_data in test_users:
        print(f"  - {user_data['sleeper_username']}")

if __name__ == "__main__":
    create_test_data()
