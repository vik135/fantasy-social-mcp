import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import json

class Database:
    """Simple SQLite database for social features"""

    def __init__(self, db_path: str = "fantasy_social.db"):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sleeper_username TEXT UNIQUE NOT NULL,
                sleeper_user_id TEXT UNIQUE NOT NULL,
                display_name TEXT,
                bio TEXT,
                avatar_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Posts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                post_type TEXT DEFAULT 'general',
                league_id TEXT,
                metadata TEXT,
                likes INTEGER DEFAULT 0,
                visibility TEXT DEFAULT 'public',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        # Add visibility column if it doesn't exist (for existing databases)
        try:
            cursor.execute("SELECT visibility FROM posts LIMIT 1")
        except sqlite3.OperationalError:
            cursor.execute("ALTER TABLE posts ADD COLUMN visibility TEXT DEFAULT 'public'")
            conn.commit()

        # Follows table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS follows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                follower_id INTEGER NOT NULL,
                following_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (follower_id) REFERENCES users (id),
                FOREIGN KEY (following_id) REFERENCES users (id),
                UNIQUE(follower_id, following_id)
            )
        ''')

        # Comments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (post_id) REFERENCES posts (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        conn.commit()
        conn.close()

    # User operations
    def create_user(self, sleeper_username: str, sleeper_user_id: str,
                   display_name: str = None, bio: str = None, avatar_url: str = None) -> Optional[int]:
        """Create a new user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (sleeper_username, sleeper_user_id, display_name, bio, avatar_url)
                VALUES (?, ?, ?, ?, ?)
            ''', (sleeper_username, sleeper_user_id, display_name or sleeper_username, bio, avatar_url))
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            conn.close()
            return None

    def get_user_by_sleeper_username(self, sleeper_username: str) -> Optional[Dict]:
        """Get user by Sleeper username"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE sleeper_username = ?', (sleeper_username,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def update_user(self, user_id: int, display_name: str = None, bio: str = None):
        """Update user profile"""
        conn = self.get_connection()
        cursor = conn.cursor()
        if display_name:
            cursor.execute('UPDATE users SET display_name = ? WHERE id = ?', (display_name, user_id))
        if bio:
            cursor.execute('UPDATE users SET bio = ? WHERE id = ?', (bio, user_id))
        conn.commit()
        conn.close()

    # Post operations
    def create_post(self, user_id: int, content: str, post_type: str = 'general',
                   league_id: str = None, metadata: Dict = None, visibility: str = 'public') -> int:
        """Create a new post"""
        conn = self.get_connection()
        cursor = conn.cursor()
        metadata_json = json.dumps(metadata) if metadata else None
        cursor.execute('''
            INSERT INTO posts (user_id, content, post_type, league_id, metadata, visibility)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, content, post_type, league_id, metadata_json, visibility))
        conn.commit()
        post_id = cursor.lastrowid
        conn.close()
        return post_id

    def get_posts(self, limit: int = 50, user_id: int = None) -> List[Dict]:
        """Get posts (optionally filtered by user)"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if user_id:
            cursor.execute('''
                SELECT p.*, u.display_name, u.sleeper_username, u.avatar_url
                FROM posts p
                JOIN users u ON p.user_id = u.id
                WHERE p.user_id = ?
                ORDER BY p.created_at DESC
                LIMIT ?
            ''', (user_id, limit))
        else:
            cursor.execute('''
                SELECT p.*, u.display_name, u.sleeper_username, u.avatar_url
                FROM posts p
                JOIN users u ON p.user_id = u.id
                ORDER BY p.created_at DESC
                LIMIT ?
            ''', (limit,))

        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_feed_for_user(self, user_id: int, limit: int = 50, view_mode: str = 'public') -> List[Dict]:
        """
        Get feed for a user based on view mode

        Public mode: All public posts + private posts from people you follow
        Private mode: Only posts from people you follow (public + private) + your own posts
        """
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if view_mode == 'public':
            # Public mode: All public posts + private posts from people you follow
            cursor.execute('''
                SELECT p.*, u.display_name, u.sleeper_username, u.avatar_url
                FROM posts p
                JOIN users u ON p.user_id = u.id
                WHERE (
                    p.visibility = 'public'
                    OR (
                        p.visibility = 'private' AND (
                            p.user_id = ? OR p.user_id IN (
                                SELECT following_id FROM follows WHERE follower_id = ?
                            )
                        )
                    )
                )
                ORDER BY p.created_at DESC
                LIMIT ?
            ''', (user_id, user_id, limit))
        else:
            # Private mode: Only posts from people you follow + your own posts
            cursor.execute('''
                SELECT p.*, u.display_name, u.sleeper_username, u.avatar_url
                FROM posts p
                JOIN users u ON p.user_id = u.id
                WHERE p.user_id = ? OR p.user_id IN (
                    SELECT following_id FROM follows WHERE follower_id = ?
                )
                ORDER BY p.created_at DESC
                LIMIT ?
            ''', (user_id, user_id, limit))

        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def like_post(self, post_id: int):
        """Increment likes on a post"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE posts SET likes = likes + 1 WHERE id = ?', (post_id,))
        conn.commit()
        conn.close()

    def delete_post(self, post_id: int, user_id: int) -> bool:
        """Delete a post (only if it belongs to the user)"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # First check if the post belongs to the user
        cursor.execute('SELECT user_id FROM posts WHERE id = ?', (post_id,))
        result = cursor.fetchone()

        if result and result[0] == user_id:
            # Delete associated comments first
            cursor.execute('DELETE FROM comments WHERE post_id = ?', (post_id,))
            # Then delete the post
            cursor.execute('DELETE FROM posts WHERE id = ?', (post_id,))
            conn.commit()
            conn.close()
            return True
        else:
            conn.close()
            return False

    # Follow operations
    def follow_user(self, follower_id: int, following_id: int) -> bool:
        """Follow a user"""
        if follower_id == following_id:
            return False
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO follows (follower_id, following_id)
                VALUES (?, ?)
            ''', (follower_id, following_id))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False

    def unfollow_user(self, follower_id: int, following_id: int):
        """Unfollow a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM follows
            WHERE follower_id = ? AND following_id = ?
        ''', (follower_id, following_id))
        conn.commit()
        conn.close()

    def is_following(self, follower_id: int, following_id: int) -> bool:
        """Check if user is following another user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM follows
            WHERE follower_id = ? AND following_id = ?
        ''', (follower_id, following_id))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0

    def get_followers(self, user_id: int) -> List[Dict]:
        """Get followers of a user"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT u.* FROM users u
            JOIN follows f ON u.id = f.follower_id
            WHERE f.following_id = ?
        ''', (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_following(self, user_id: int) -> List[Dict]:
        """Get users that a user is following"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT u.* FROM users u
            JOIN follows f ON u.id = f.following_id
            WHERE f.follower_id = ?
        ''', (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_user_stats(self, user_id: int) -> Dict:
        """Get user statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM posts WHERE user_id = ?', (user_id,))
        post_count = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM follows WHERE follower_id = ?', (user_id,))
        following_count = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM follows WHERE following_id = ?', (user_id,))
        followers_count = cursor.fetchone()[0]

        conn.close()

        return {
            'posts': post_count,
            'following': following_count,
            'followers': followers_count
        }

    def get_all_users(self, limit: int = 100) -> List[Dict]:
        """Get all users for discovery"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users ORDER BY created_at DESC LIMIT ?', (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    # Comment operations
    def add_comment(self, post_id: int, user_id: int, content: str) -> int:
        """Add a comment to a post"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO comments (post_id, user_id, content)
            VALUES (?, ?, ?)
        ''', (post_id, user_id, content))
        conn.commit()
        comment_id = cursor.lastrowid
        conn.close()
        return comment_id

    def get_comments(self, post_id: int) -> List[Dict]:
        """Get comments for a post"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.*, u.display_name, u.sleeper_username
            FROM comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.post_id = ?
            ORDER BY c.created_at ASC
        ''', (post_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
