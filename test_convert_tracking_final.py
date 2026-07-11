"""
Test script: Process 2022 World Cup Final match data
Argentina vs France
"""

import sys
import os

# Ensure convert_tracking can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from convert_tracking import process_game, get_available_games, load_game_metadata

def main():
    print("=" * 80)
    print("2022 FIFA World Cup Final - Data Processing Test")
    print("=" * 80)
    
    # Get all available games
    print("\nStep 1: Getting all available games...")
    try:
        games = get_available_games()
        print(f"[OK] Found {len(games)} games")
        print(f"  Game IDs: {games}")
    except Exception as e:
        print(f"[ERROR] {e}")
        return
    
    # Find final match ID (10517 - Argentina vs France)
    final_game_id = '10517'
    
    if final_game_id not in games:
        print(f"\n[ERROR] Final match ID {final_game_id} not found")
        print(f"  Available games: {games}")
        return
    
    # Load final match metadata
    print(f"\nStep 2: Loading final match metadata (ID: {final_game_id})...")
    try:
        metadata = load_game_metadata(final_game_id)
        print(f"[OK] Metadata loaded successfully")
        print(f"  Home Team: {metadata['homeTeam']['name']}")
        print(f"  Away Team: {metadata['awayTeam']['name']}")
        print(f"  Date: {metadata['date']}")
        print(f"  Stadium: {metadata['stadium']['name']}")
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Process final match data
    print(f"\nStep 3: Processing final match tracking data...")
    print("  Note: This may take several minutes...")
    
    try:
        balls_df, events_df, players_df = process_game(final_game_id, save_output=True)
        
        print(f"\n[OK] Final match data processed successfully!")
        print("\n" + "=" * 80)
        print("Data Statistics")
        print("=" * 80)
        
        # Ball data statistics
        print(f"\n[Ball Data]")
        print(f"  Total frames: {len(balls_df)}")
        print(f"  Time range: {balls_df['periodElapsedTime'].min():.2f}s - {balls_df['periodElapsedTime'].max():.2f}s")
        print(f"  Periods: {balls_df['period'].unique()}")
        print(f"\n  First 5 rows:")
        print(balls_df.head().to_string())
        
        # Event data statistics
        print(f"\n[Event Data]")
        print(f"  Total events: {len(events_df)}")
        if len(events_df) > 0:
            print(f"  Event types: {events_df['eventType'].unique()}")
            print(f"  Teams involved: {events_df['team_name'].unique()}")
            print(f"\n  First 5 events:")
            print(events_df[['periodElapsedTime', 'eventType', 'player_name', 'team_name']].head().to_string())
        
        # Player data statistics
        print(f"\n[Player Data]")
        print(f"  Total records: {len(players_df)}")
        print(f"  Number of players: {players_df['playerName'].nunique()}")
        print(f"  Teams: {players_df['teamName'].unique()}")
        
        # Statistics by team
        for team in players_df['teamName'].unique():
            team_players = players_df[players_df['teamName'] == team]['playerName'].unique()
            print(f"\n  {team} ({len(team_players)} players):")
            for i, player in enumerate(sorted(team_players)[:11], 1):
                pos = players_df[players_df['playerName'] == player]['playerPos'].iloc[0]
                jersey = players_df[players_df['playerName'] == player]['jerseyNum'].iloc[0]
                try:
                    print(f"    {i:2d}. #{jersey:2d} {player:20s} ({pos})")
                except UnicodeEncodeError:
                    # Handle special characters in player names
                    player_safe = player.encode('ascii', 'replace').decode('ascii')
                    print(f"    {i:2d}. #{jersey:2d} {player_safe:20s} ({pos})")
        
        # Output file locations
        print(f"\n" + "=" * 80)
        print("Output Files")
        print("=" * 80)
        output_dir = f"Data/{final_game_id}"
        print(f"  Directory: {output_dir}/")
        print(f"  - balls_{final_game_id}.csv")
        print(f"  - events_{final_game_id}.csv")
        print(f"  - players_{final_game_id}.csv")
        
        print(f"\n" + "=" * 80)
        print("[OK] Test completed! Final match data successfully processed and saved.")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n[ERROR] Processing failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()