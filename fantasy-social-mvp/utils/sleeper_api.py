import requests
from typing import Optional, List, Dict
import streamlit as st

class SleeperAPI:
    """Wrapper for Sleeper Fantasy Football API"""
    BASE_URL = "https://api.sleeper.app/v1"

    @staticmethod
    @st.cache_data(ttl=300)
    def get_user(username: str) -> Optional[Dict]:
        """Get user info by username"""
        try:
            response = requests.get(f"{SleeperAPI.BASE_URL}/user/{username}")
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            st.error(f"Error fetching user: {e}")
            return None

    @staticmethod
    @st.cache_data(ttl=300)
    def get_user_leagues(user_id: str, sport: str = "nfl", season: str = "2025") -> List[Dict]:
        """Get all leagues for a user"""
        try:
            response = requests.get(f"{SleeperAPI.BASE_URL}/user/{user_id}/leagues/{sport}/{season}")
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            st.error(f"Error fetching leagues: {e}")
            return []

    @staticmethod
    @st.cache_data(ttl=300)
    def get_league_rosters(league_id: str) -> List[Dict]:
        """Get all rosters in a league"""
        try:
            response = requests.get(f"{SleeperAPI.BASE_URL}/league/{league_id}/rosters")
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            st.error(f"Error fetching rosters: {e}")
            return []

    @staticmethod
    @st.cache_data(ttl=300)
    def get_league_users(league_id: str) -> List[Dict]:
        """Get all users in a league"""
        try:
            response = requests.get(f"{SleeperAPI.BASE_URL}/league/{league_id}/users")
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            st.error(f"Error fetching league users: {e}")
            return []

    @staticmethod
    @st.cache_data(ttl=300)
    def get_league(league_id: str) -> Optional[Dict]:
        """Get league details"""
        try:
            response = requests.get(f"{SleeperAPI.BASE_URL}/league/{league_id}")
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            st.error(f"Error fetching league: {e}")
            return None

    @staticmethod
    def get_user_roster_in_league(user_id: str, league_id: str) -> Optional[Dict]:
        """Get a specific user's roster in a league"""
        rosters = SleeperAPI.get_league_rosters(league_id)
        for roster in rosters:
            if roster.get('owner_id') == user_id:
                return roster
        return None

    @staticmethod
    @st.cache_data(ttl=3600)
    def get_all_players() -> Dict:
        """Get all NFL players data (cached for 1 hour)"""
        try:
            response = requests.get(f"{SleeperAPI.BASE_URL}/players/nfl")
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            st.error(f"Error fetching players: {e}")
            return {}

    @staticmethod
    def get_player_name(player_id: str, all_players: Dict = None) -> str:
        """Get player name from player ID"""
        if all_players is None:
            all_players = SleeperAPI.get_all_players()

        player = all_players.get(player_id, {})
        if player:
            first = player.get('first_name', '')
            last = player.get('last_name', '')
            position = player.get('position', '')
            team = player.get('team', '')
            return f"{first} {last} ({position} - {team})" if first and last else player_id
        return player_id

    @staticmethod
    def get_roster_with_names(roster: Dict, all_players: Dict = None) -> Dict:
        """Get roster with player names instead of IDs"""
        if all_players is None:
            all_players = SleeperAPI.get_all_players()

        roster_copy = roster.copy()

        if 'players' in roster_copy and roster_copy['players']:
            roster_copy['player_details'] = []
            for player_id in roster_copy['players']:
                player = all_players.get(player_id, {})
                if player:
                    roster_copy['player_details'].append({
                        'id': player_id,
                        'name': f"{player.get('first_name', '')} {player.get('last_name', '')}".strip(),
                        'position': player.get('position', 'N/A'),
                        'team': player.get('team', 'N/A'),
                        'status': player.get('injury_status', 'Active')
                    })

        if 'starters' in roster_copy and roster_copy['starters']:
            roster_copy['starter_details'] = []
            for player_id in roster_copy['starters']:
                player = all_players.get(player_id, {})
                if player:
                    roster_copy['starter_details'].append({
                        'id': player_id,
                        'name': f"{player.get('first_name', '')} {player.get('last_name', '')}".strip(),
                        'position': player.get('position', 'N/A'),
                        'team': player.get('team', 'N/A'),
                        'status': player.get('injury_status', 'Active')
                    })

        return roster_copy
