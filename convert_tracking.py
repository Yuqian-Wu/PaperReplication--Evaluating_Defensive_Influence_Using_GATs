"""
Football Tracking Data Processor - 2022 World Cup Edition
===============================================

This module processes raw football tracking data from compressed JSONL files
and converts it into structured pandas DataFrames for analysis.

Features:
- Loads and parses bz2-compressed JSONL tracking data
- Extracts player positions, ball positions, and game events
- Calculates velocities and accelerations for players and ball
- Handles coordinate transformations and data cleaning
- Manages team rosters and metadata
- Adapted for 2022 FIFA World Cup dataset from Gradient Sports
"""

import pandas as pd
import bz2
import json
import numpy as np
import os

# =============================================================================
# CONFIGURATION AND SETUP
# =============================================================================

# Data paths configuration for 2022 World Cup dataset
BASE_DATA_PATH = r'E:\JerryWu\Master\SoccerAnalytics\OpenData\TrackingData\Gradient Sports  Enhanced 2022 World Cup Dataset'
TRACKING_DATA_PATH = os.path.join(BASE_DATA_PATH, 'Tracking Data')
METADATA_PATH = os.path.join(BASE_DATA_PATH, 'Metadata')
ROSTERS_PATH = os.path.join(BASE_DATA_PATH, 'Rosters')
OUTPUT_PATH = 'Data'  # Local output directory

# Create output directory if it doesn't exist
if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

# =============================================================================
# DATA LOADING FUNCTIONS
# =============================================================================

def load_tracking_data(filepath):
    """
    Load and parse tracking data from a bz2-compressed JSONL file.
    
    Args:
        filepath (str): Path to the bz2 file containing JSONL data
        
    Returns:
        list: List of dictionaries containing parsed JSON data
    """
    data = []
    with bz2.open(filepath, 'rt') as f:
        for line in f:
            data.append(json.loads(line))
    return data

# =============================================================================
# MAIN PROCESSING FUNCTION
# =============================================================================

def process_tracking_data(data, roster_game_home_name_dict, roster_game_home_team_name_dict,
                         roster_game_home_pos_dict, roster_game_away_name_dict, 
                         roster_game_away_team_name_dict, roster_game_away_pos_dict,
                         home_team_start_left, pitch_x_adjustment, pitch_y_adjustment):
    """
    Transform raw tracking data into structured DataFrames.
    
    Args:
        data (list): Raw tracking data from load_tracking_data()
        roster_game_home_name_dict (dict): Home team jersey number to player name mapping
        roster_game_home_team_name_dict (dict): Home team jersey number to team name mapping
        roster_game_home_pos_dict (dict): Home team jersey number to position mapping
        roster_game_away_name_dict (dict): Away team jersey number to player name mapping
        roster_game_away_team_name_dict (dict): Away team jersey number to team name mapping
        roster_game_away_pos_dict (dict): Away team jersey number to position mapping
        home_team_start_left (bool): Whether home team starts on the left side
        pitch_x_adjustment (float): X-coordinate adjustment for pitch normalization
        pitch_y_adjustment (float): Y-coordinate adjustment for pitch normalization
        
    Returns:
        tuple: (balls_df, events_df, players_df) - Three processed DataFrames
    """
    # Initialize data containers
    home_players_data = []
    away_players_data = []
    balls_data = []
    events_data = []

    # Process each frame of tracking data
    for frame in data:
        if frame['homePlayersSmoothed'] is None:
            continue
            
        # Extract player data
        _extract_home_players(frame, home_players_data, roster_game_home_name_dict,
                             roster_game_home_team_name_dict, roster_game_home_pos_dict)
        _extract_away_players(frame, away_players_data, roster_game_away_name_dict,
                             roster_game_away_team_name_dict, roster_game_away_pos_dict)
        
        # Extract ball and event data
        _extract_ball_data(frame, balls_data)
        _extract_event_data(frame, events_data)

    # Convert to DataFrames and process
    balls_df, events_df, players_df = _create_dataframes(
        home_players_data, away_players_data, balls_data, events_data, home_team_start_left
    )
    
    # Clean and enhance data
    players_df = _clean_player_data(players_df)
    balls_df = _clean_ball_data(balls_df, players_df)
    events_df = _process_events_data(events_df, balls_df)
    
    # Apply coordinate transformations
    players_df, balls_df = _apply_coordinate_transformations(
        players_df, balls_df, pitch_x_adjustment, pitch_y_adjustment
    )
    
    # Calculate velocities and accelerations
    players_df = get_players_df_velocities(players_df)
    balls_df = calculate_ball_velocities(balls_df)
    
    return balls_df, events_df, players_df

# =============================================================================
# DATA EXTRACTION HELPER FUNCTIONS
# =============================================================================

def _extract_home_players(frame, home_players_data, name_dict, team_name_dict, pos_dict):
    """Extract home team player data from a frame."""
    for player in frame['homePlayersSmoothed']:
        jersey_num = int(player.get('jerseyNum'))
        
        # Skip players not in roster (substitutes or tracking errors)
        if jersey_num not in name_dict:
            continue
            
        home_players_data.append({
            'frameNum': int(frame['frameNum']),
            'period': int(frame['period']),
            'periodElapsedTime': float(frame['periodElapsedTime']),
            'playerName': name_dict[jersey_num],
            'playerPos': pos_dict[jersey_num],
            'jerseyNum': jersey_num,
            'x': float(player.get('x')),
            'y': float(player.get('y')),
            'confidence': player.get('confidence'),
            'visibility': player.get('visibility'),
            'is_home': True,
            'teamName': team_name_dict[jersey_num]
        })

def _extract_away_players(frame, away_players_data, name_dict, team_name_dict, pos_dict):
    """Extract away team player data from a frame."""
    for player in frame['awayPlayersSmoothed']:
        jersey_num = int(player.get('jerseyNum'))
        
        # Skip players not in roster (substitutes or tracking errors)
        if jersey_num not in name_dict:
            continue
            
        away_players_data.append({
            'frameNum': int(frame['frameNum']),
            'period': int(frame['period']),
            'periodElapsedTime': float(frame['periodElapsedTime']),
            'playerName': name_dict[jersey_num],
            'playerPos': pos_dict[jersey_num],
            'jerseyNum': jersey_num,
            'x': player.get('x'),
            'y': player.get('y'),
            'confidence': player.get('confidence'),
            'visibility': player.get('visibility'),
            'is_home': False,
            'teamName': team_name_dict[jersey_num]
        })

def _extract_ball_data(frame, balls_data):
    """Extract ball position data from a frame."""
    ball_data = {
        'frameNum': int(frame['frameNum']),
        'period': int(frame['period']),
        'periodElapsedTime': float(frame['periodElapsedTime']),
        'x': None,
        'y': None,
        'z': None,
        'visibility': None,
    }
    
    if frame['ballsSmoothed'] is not None:
        ball = frame['ballsSmoothed']
        ball_data.update({
            'x': ball.get('x'),
            'y': ball.get('y'),
            'z': ball.get('z'),
            'visibility': ball.get('visibility'),
        })
    
    balls_data.append(ball_data)

def _extract_event_data(frame, events_data):
    """Extract game event data from a frame."""
    if (frame['game_event'] is not None) and (frame['possession_event'] is not None):
        poss_event = frame['possession_event'].get('possession_event_type')
        events_data.append({
            'frameNum': int(frame['frameNum']),
            'period': int(frame['period']),
            'periodElapsedTime': float(frame['periodElapsedTime']),
            'eventType': frame['game_event'].get('game_event_type'),
            'player_name': frame['game_event'].get('player_name'),
            'team_name': frame['game_event'].get('team_name'),
            'possessionEventType': poss_event,
            'start_frame': frame['game_event'].get('start_frame'),
            'end_frame': frame['game_event'].get('end_frame'),
            'start_time': frame['game_event'].get('start_time'),
            'end_time': frame['game_event'].get('end_time'),
        })

# =============================================================================
# DATAFRAME CREATION AND PROCESSING
# =============================================================================

def _create_dataframes(home_players_data, away_players_data, balls_data, events_data, home_team_start_left):
    """Create initial DataFrames from extracted data."""
    home_players_df = pd.DataFrame(home_players_data)
    away_players_df = pd.DataFrame(away_players_data)
    balls_df = pd.DataFrame(balls_data)
    events_df = pd.DataFrame(events_data)
    
    # Add team direction information
    if len(balls_df) > 0:
        balls_df['homeTeamLeft'] = np.where(balls_df['period'] == 1, home_team_start_left, ~home_team_start_left)
    if len(events_df) > 0:
        events_df['homeTeamLeft'] = np.where(events_df['period'] == 1, home_team_start_left, ~home_team_start_left)

    # Combine player dataframes
    players_df = pd.concat([home_players_df, away_players_df], axis=0, ignore_index=True)
    
    return balls_df, events_df, players_df

def _clean_player_data(players_df):
    """Clean player data by removing frames with incorrect player counts."""
    if len(players_df) == 0:
        return players_df
    
    frame_counts = players_df['frameNum'].value_counts()
    valid_frames = frame_counts[frame_counts <= 22].index
    players_df = players_df[players_df['frameNum'].isin(valid_frames)]
    return players_df.sort_values('frameNum').reset_index(drop=True)

def _clean_ball_data(balls_df, players_df):
    """Clean ball data to match valid player frames."""
    if len(players_df) == 0 or len(balls_df) == 0:
        return balls_df
    return balls_df[balls_df['frameNum'].isin(players_df['frameNum'].unique())]

def _process_events_data(events_df, balls_df):
    """Process events data and add possession sequences."""
    if len(events_df) == 0:
        return events_df
    
    # Remove duplicate events and merge with ball position
    events_df = events_df.drop_duplicates('frameNum').reset_index(drop=True)
    events_df = events_df.merge(balls_df[['frameNum', 'x', 'y', 'z']], on=['frameNum'], how='left')
    
    # Add possession sequences
    events_df['is_new_sequence'] = (
        (events_df['team_name'] != events_df['team_name'].shift()) &
        (events_df['team_name'] == events_df['team_name'].shift(-1))
    )
    events_df['possession_sequence'] = events_df['is_new_sequence'].cumsum() - 1
    events_df.drop(columns=['is_new_sequence'], inplace=True)
    
    return events_df

def _apply_coordinate_transformations(players_df, balls_df, pitch_x_adjustment, pitch_y_adjustment):
    """Apply coordinate transformations to normalize pitch coordinates."""
    # Transform to standard pitch coordinates
    if len(players_df) > 0 and 'x' in players_df.columns:
        players_df['x'] = players_df['x'] + pitch_x_adjustment
        players_df['y'] = players_df['y'] + pitch_y_adjustment
    
    if len(balls_df) > 0 and 'x' in balls_df.columns:
        balls_df['x'] = balls_df['x'] + pitch_x_adjustment
        balls_df['y'] = balls_df['y'] + pitch_y_adjustment
    
    return players_df, balls_df

# =============================================================================
# VELOCITY AND ACCELERATION CALCULATIONS
# =============================================================================

def get_players_df_velocities(players_df):
    """
    Calculate velocities and accelerations for all players.
    
    Args:
        players_df (pd.DataFrame): Player tracking data
        
    Returns:
        pd.DataFrame: Enhanced DataFrame with velocity and acceleration data
    """
    # Sort the dataframe for proper time-series calculations
    players_df_sorted = players_df.sort_values(['playerName', 'period', 'periodElapsedTime'])

    # Calculate time and position differences
    players_df_sorted = _calculate_time_differences(players_df_sorted)
    players_df_sorted = _calculate_position_differences(players_df_sorted)
    
    # Calculate velocities and accelerations
    players_df_sorted = _calculate_velocities(players_df_sorted)
    players_df_sorted = _calculate_accelerations(players_df_sorted)
    
    # Clean and smooth the data
    players_df_sorted = _clean_velocity_data(players_df_sorted)
    players_df_sorted = _apply_smoothing(players_df_sorted)
    
    # Return final cleaned dataset
    return _finalize_player_dataframe(players_df_sorted)

def _calculate_time_differences(df):
    """Calculate time differences between consecutive frames for each player."""
    df['dt'] = df.groupby('playerName')['periodElapsedTime'].diff()
    return df

def _calculate_position_differences(df):
    """Calculate position differences between consecutive frames for each player."""
    df['dx'] = df.groupby('playerName')['x'].diff()
    df['dy'] = df.groupby('playerName')['y'].diff()
    return df

def _calculate_velocities(df):
    """Calculate velocity components and magnitude."""
    df['velocity_x'] = df['dx'] / df['dt']
    df['velocity_y'] = df['dy'] / df['dt']
    df['velocity_magnitude'] = np.sqrt(df['velocity_x']**2 + df['velocity_y']**2)
    return df

def _calculate_accelerations(df):
    """Calculate acceleration components and magnitude."""
    df['acceleration_x'] = df.groupby('playerName')['velocity_x'].diff() / df['dt']
    df['acceleration_y'] = df.groupby('playerName')['velocity_y'].diff() / df['dt']
    df['acceleration_magnitude'] = np.sqrt(df['acceleration_x']**2 + df['acceleration_y']**2)
    return df

def _clean_velocity_data(df):
    """Remove infinite values and replace with zeros."""
    return df.replace([np.inf, -np.inf], 0)

def _apply_smoothing(df, window_size=5):
    """Apply rolling average smoothing to velocity and acceleration data."""
    df['velocity_magnitude'] = df.groupby('playerName', group_keys=False).apply(
        lambda x: x['velocity_magnitude'].rolling(window=window_size, center=True, min_periods=1).mean()
    )

    df['acceleration_magnitude'] = df.groupby('playerName', group_keys=False).apply(
        lambda x: x['acceleration_magnitude'].rolling(window=window_size, center=True, min_periods=1).mean()
    )
    
    return df

def _finalize_player_dataframe(df):
    """Finalize the player dataframe with proper column selection and sorting."""
    final_columns = [
        'frameNum', 'period', 'periodElapsedTime', 'playerName', 'playerPos',
        'jerseyNum', 'x', 'y', 'confidence', 'visibility', 'is_home',
        'teamName', 'velocity_x', 'velocity_y', 'velocity_magnitude', 
        'acceleration_x', 'acceleration_y', 'acceleration_magnitude'
    ]
    
    return (df.fillna(0)
              .sort_values(['frameNum', 'period'])
              [final_columns]
              .reset_index(drop=True))

def calculate_ball_velocities(balls_df):
    """
    Calculate velocities and accelerations for the ball.
    
    Args:
        balls_df (pd.DataFrame): Ball tracking data
        
    Returns:
        pd.DataFrame: Enhanced DataFrame with ball velocity and acceleration data
    """
    # Create a copy to avoid modifying the original
    df = balls_df.copy().sort_values('frameNum')

    # Calculate time and position differences
    df = _calculate_ball_time_differences(df)
    df = _calculate_ball_position_differences(df)
    
    # Calculate velocities and accelerations
    df = _calculate_ball_velocities(df)
    df = _calculate_ball_accelerations(df)
    
    # Clean the data
    df = _clean_ball_velocity_data(df)
    
    # Return final cleaned dataset
    return _finalize_ball_dataframe(df)

def _calculate_ball_time_differences(df):
    """Calculate time differences between consecutive frames for ball."""
    df['dt'] = df['periodElapsedTime'].diff()
    return df

def _calculate_ball_position_differences(df):
    """Calculate position differences between consecutive frames for ball."""
    df['dx'] = df['x'].diff()
    df['dy'] = df['y'].diff()
    return df

def _calculate_ball_velocities(df):
    """Calculate ball velocity components and magnitude."""
    df['velocity_x'] = df['dx'] / df['dt']
    df['velocity_y'] = df['dy'] / df['dt']
    df['velocity_magnitude'] = np.sqrt(df['velocity_x']**2 + df['velocity_y']**2)
    return df

def _calculate_ball_accelerations(df):
    """Calculate ball acceleration components and magnitude."""
    df['dvx'] = df['velocity_x'].diff()
    df['dvy'] = df['velocity_y'].diff()
    df['acceleration_x'] = df['dvx'] / df['dt']
    df['acceleration_y'] = df['dvy'] / df['dt']
    df['acceleration_magnitude'] = np.sqrt(df['acceleration_x']**2 + df['acceleration_y']**2)
    return df

def _clean_ball_velocity_data(df):
    """Clean ball velocity data by handling NaN values."""
    velocity_columns = [
        'velocity_x', 'velocity_y', 'velocity_magnitude', 
        'acceleration_x', 'acceleration_y', 'acceleration_magnitude'
    ]
    
    for col in velocity_columns:
        df[col] = df[col].fillna(method='ffill').fillna(method='bfill')
    
    return df

def _finalize_ball_dataframe(df):
    """Finalize the ball dataframe with proper column selection and sorting."""
    final_columns = [
        'frameNum', 'period', 'periodElapsedTime', 'x', 'y', 'z', 'visibility', 
        'homeTeamLeft', 'velocity_x', 'velocity_y', 'velocity_magnitude', 
        'acceleration_x', 'acceleration_y', 'acceleration_magnitude'
    ]
    
    return (df.sort_values(['frameNum', 'period'])
              [final_columns]
              .reset_index(drop=True))

# =============================================================================
# METADATA AND ROSTER MANAGEMENT
# =============================================================================

def load_game_metadata(game_id):
    """
    Load metadata for a specific game from JSON file.
    
    Args:
        game_id (str or int): Unique identifier for the game
        
    Returns:
        dict: Game metadata dictionary
    """
    metadata_file = os.path.join(METADATA_PATH, f'{game_id}.json')
    
    if not os.path.exists(metadata_file):
        raise FileNotFoundError(f"Metadata file not found: {metadata_file}")
    
    with open(metadata_file, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    # Return the first element if it's a list
    if isinstance(metadata, list) and len(metadata) > 0:
        return metadata[0]
    return metadata

def load_game_roster(game_id):
    """
    Load roster for a specific game from JSON file.
    
    Args:
        game_id (str or int): Unique identifier for the game
        
    Returns:
        list: List of player dictionaries
    """
    roster_file = os.path.join(ROSTERS_PATH, f'{game_id}.json')
    
    if not os.path.exists(roster_file):
        raise FileNotFoundError(f"Roster file not found: {roster_file}")
    
    with open(roster_file, 'r', encoding='utf-8') as f:
        roster = json.load(f)
    
    return roster

def get_metadata(game_id):
    """
    Extract game metadata and roster information for a specific game.
    Adapted for 2022 World Cup JSON format.
    
    Args:
        game_id (str or int): Unique identifier for the game
        
    Returns:
        tuple: Comprehensive game metadata including team information and roster dictionaries
    """
    # Load metadata and roster from JSON files
    game_metadata = load_game_metadata(game_id)
    roster_data = load_game_roster(game_id)
    
    # Extract basic game information
    game_info = _extract_game_info_from_json(game_metadata)
    
    # Split rosters by team
    home_roster, away_roster = _split_rosters_by_team_json(roster_data, game_info)
    
    # Create roster dictionaries
    roster_dicts = _create_roster_dictionaries_json(home_roster, away_roster)
    
    # Set pitch adjustments
    pitch_adjustments = _get_pitch_adjustments()
    
    return (*game_info, home_roster, away_roster, *roster_dicts, *pitch_adjustments)

def _extract_game_info_from_json(game_metadata):
    """Extract basic game information from JSON metadata."""
    home_team_id = game_metadata['homeTeam']['id']
    away_team_id = game_metadata['awayTeam']['id']
    home_team_name = game_metadata['homeTeam']['name']
    away_team_name = game_metadata['awayTeam']['name']
    home_team_start_left = game_metadata['homeTeamStartLeft']
    
    return home_team_id, away_team_id, home_team_name, away_team_name, home_team_start_left

def _split_rosters_by_team_json(roster_data, game_info):
    """Split roster data by home and away teams from JSON format."""
    home_team_id, away_team_id = game_info[0], game_info[1]
    
    home_roster = []
    away_roster = []
    
    for player_entry in roster_data:
        team_id = player_entry['team']['id']
        if team_id == home_team_id:
            home_roster.append(player_entry)
        elif team_id == away_team_id:
            away_roster.append(player_entry)
    
    return home_roster, away_roster

def _create_roster_dictionaries_json(home_roster, away_roster):
    """Create dictionaries mapping jersey numbers to player information from JSON format."""
    # Home team dictionaries
    roster_game_home_name_dict = {}
    roster_game_home_team_name_dict = {}
    roster_game_home_pos_dict = {}
    
    for player in home_roster:
        # Convert jersey number to int for consistency with tracking data
        jersey_num = int(player['shirtNumber'])
        roster_game_home_name_dict[jersey_num] = player['player']['nickname']
        roster_game_home_team_name_dict[jersey_num] = player['team']['name']
        roster_game_home_pos_dict[jersey_num] = player['positionGroupType']
    
    # Away team dictionaries
    roster_game_away_name_dict = {}
    roster_game_away_team_name_dict = {}
    roster_game_away_pos_dict = {}
    
    for player in away_roster:
        # Convert jersey number to int for consistency with tracking data
        jersey_num = int(player['shirtNumber'])
        roster_game_away_name_dict[jersey_num] = player['player']['nickname']
        roster_game_away_team_name_dict[jersey_num] = player['team']['name']
        roster_game_away_pos_dict[jersey_num] = player['positionGroupType']
    
    return (roster_game_home_name_dict, roster_game_home_team_name_dict, roster_game_home_pos_dict,
            roster_game_away_name_dict, roster_game_away_team_name_dict, roster_game_away_pos_dict)

def _get_pitch_adjustments():
    """Get standard pitch coordinate adjustments."""
    pitch_x_adjustment = 52.5
    pitch_y_adjustment = 34
    return pitch_x_adjustment, pitch_y_adjustment

# =============================================================================
# FILE DOWNLOAD UTILITIES
# =============================================================================

def download_all_files():
    """
    Download all files from S3 bucket to local directory.
    
    Note: This function requires AWS S3 configuration and proper credentials.
    The variables 's3', 'bucket_name', and 'local_directory' need to be defined
    in the calling context.
    """
    # Create local directory if it doesn't exist
    if not os.path.exists(local_directory):
        try:
            os.makedirs(local_directory)
        except PermissionError:
            print(f"Error: No permission to create directory {local_directory}")
            return
        except Exception as e:
            print(f"Error creating directory: {str(e)}")
            return

    # Initialize download process
    paginator = s3.get_paginator('list_objects_v2')
    total_files = 0
    downloaded_files = 0

    try:
        # Count total files
        total_files = _count_total_files(paginator)
        print(f"Found {total_files} files in the bucket")

        # Download all files
        downloaded_files = _download_files(paginator, total_files)
        print(f"\nDownload complete! Downloaded {downloaded_files} files to {local_directory}/")

    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

def _count_total_files(paginator):
    """Count total number of files in the S3 bucket."""
    total_files = 0
    for page in paginator.paginate(Bucket=bucket_name):
        if 'Contents' in page:
            total_files += len(page['Contents'])
    return total_files

def _download_files(paginator, total_files):
    """Download all files from S3 bucket."""
    downloaded_files = 0
    
    for page in paginator.paginate(Bucket=bucket_name):
        if 'Contents' in page:
            for obj in page['Contents']:
                success = _download_single_file(obj, downloaded_files + 1, total_files)
                if success:
                    downloaded_files += 1
    
    return downloaded_files

def _download_single_file(obj, current_count, total_count):
    """Download a single file from S3."""
    s3_file = obj['Key']
    safe_filename = s3_file.replace('/', '_')  # Make filename Windows-safe
    local_file = os.path.join(local_directory, safe_filename)

    try:
        print(f"Downloading {s3_file}... ", end='', flush=True)
        s3.download_file(bucket_name, s3_file, local_file)
        print(f"Done! ({current_count}/{total_count})")
        return True
    except Exception as e:
        print(f"Error downloading {s3_file}: {str(e)}")
        return False

# =============================================================================
# MAIN PROCESSING FUNCTION FOR 2022 WORLD CUP DATA
# =============================================================================

def process_game(game_id, save_output=True):
    """
    Process a complete game from the 2022 World Cup dataset.
    
    Args:
        game_id (str or int): Game identifier (e.g., '3812')
        save_output (bool): Whether to save the processed dataframes to CSV
        
    Returns:
        tuple: (balls_df, events_df, players_df) - Three processed DataFrames
    """
    print(f"Processing game {game_id}...")
    
    # Load tracking data
    tracking_file = os.path.join(TRACKING_DATA_PATH, f'{game_id}.jsonl.bz2')
    if not os.path.exists(tracking_file):
        raise FileNotFoundError(f"Tracking data file not found: {tracking_file}")
    
    print(f"Loading tracking data from {tracking_file}...")
    tracking_data = load_tracking_data(tracking_file)
    print(f"Loaded {len(tracking_data)} frames")
    
    # Get metadata and roster information
    print("Loading metadata and rosters...")
    (home_team_id, away_team_id, home_team_name, away_team_name, home_team_start_left,
     home_roster, away_roster,
     roster_game_home_name_dict, roster_game_home_team_name_dict, roster_game_home_pos_dict,
     roster_game_away_name_dict, roster_game_away_team_name_dict, roster_game_away_pos_dict,
     pitch_x_adjustment, pitch_y_adjustment) = get_metadata(game_id)
    
    print(f"Game: {home_team_name} vs {away_team_name}")
    print(f"Home team starts left: {home_team_start_left}")
    
    # Process tracking data
    print("Processing tracking data...")
    balls_df, events_df, players_df = process_tracking_data(
        tracking_data,
        roster_game_home_name_dict, roster_game_home_team_name_dict, roster_game_home_pos_dict,
        roster_game_away_name_dict, roster_game_away_team_name_dict, roster_game_away_pos_dict,
        home_team_start_left, pitch_x_adjustment, pitch_y_adjustment
    )
    
    print(f"Processed {len(balls_df)} ball frames, {len(events_df)} events, {len(players_df)} player records")
    
    # Save output if requested
    if save_output:
        output_dir = os.path.join(OUTPUT_PATH, str(game_id))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        balls_file = os.path.join(output_dir, f'balls_{game_id}.csv')
        events_file = os.path.join(output_dir, f'events_{game_id}.csv')
        players_file = os.path.join(output_dir, f'players_{game_id}.csv')
        
        print(f"Saving dataframes to {output_dir}...")
        balls_df.to_csv(balls_file, index=False)
        events_df.to_csv(events_file, index=False)
        players_df.to_csv(players_file, index=False)
        print("Saved successfully!")
    
    return balls_df, events_df, players_df

def get_available_games():
    """
    Get list of available game IDs from the tracking data directory.
    
    Returns:
        list: List of game IDs (as strings)
    """
    if not os.path.exists(TRACKING_DATA_PATH):
        raise FileNotFoundError(f"Tracking data directory not found: {TRACKING_DATA_PATH}")
    
    game_ids = []
    for filename in os.listdir(TRACKING_DATA_PATH):
        if filename.endswith('.jsonl.bz2'):
            game_id = filename.replace('.jsonl.bz2', '')
            game_ids.append(game_id)
    
    return sorted(game_ids)

# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    # Example: Process a single game
    print("=" * 80)
    print("2022 FIFA World Cup Tracking Data Processor")
    print("=" * 80)
    
    # Get available games
    available_games = get_available_games()
    print(f"\nFound {len(available_games)} games in the dataset")
    print(f"First 5 games: {available_games[:5]}")
    
    # Process the first game as an example
    if available_games:
        example_game_id = available_games[0]
        print(f"\nProcessing example game: {example_game_id}")
        print("-" * 80)
        
        try:
            balls_df, events_df, players_df = process_game(example_game_id, save_output=True)
            
            print("\n" + "=" * 80)
            print("Processing completed successfully!")
            print("=" * 80)
            print(f"\nDataFrame shapes:")
            print(f"  Balls:   {balls_df.shape}")
            print(f"  Events:  {events_df.shape}")
            print(f"  Players: {players_df.shape}")
            
        except Exception as e:
            print(f"\nError processing game: {str(e)}")
            import traceback
            traceback.print_exc()
    else:
        print("\nNo games found in the tracking data directory!")
        