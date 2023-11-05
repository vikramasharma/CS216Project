import pandas as pd

# Load the datasets
player_totals_df = pd.read_csv('data/Player Totals.csv')
player_shooting_df = pd.read_csv('data/Player Shooting.csv')
player_play_by_play_df = pd.read_csv('data/Player Play by Play.csv')
player_career_info_df = pd.read_csv('data/Player Career Info.csv')


player_career_info_df = player_career_info_df.merge(
    player_totals_df[['player_id', 'pos']].drop_duplicates(),
    on='player_id',
    how='left'
)

# we may need to address NA's differently in the main analysis depending on what statistic we are looking at using fillna()
#For simplicity's sake, we will drop all Na's in this example
player_totals_df.dropna(inplace=True)
player_shooting_df.dropna(inplace=True)
player_play_by_play_df.dropna(inplace=True)
player_career_info_df.dropna(inplace=True)

avg_years_by_position = player_career_info_df.groupby('pos')['num_seasons'].mean()
players_by_position = player_totals_df.groupby('pos')['player'].nunique()


player_totals_df = player_totals_df.sort_values(by=['player_id', 'season'])

player_totals_df['pts_diff'] = player_totals_df.groupby('player_id')['pts'].diff()

avg_improvement_by_position = player_totals_df.dropna(subset=['pts_diff']).groupby('pos')['pts_diff'].mean()

# Display the results
print("Average number of years played by position:")
print(avg_years_by_position)

print("\nNumber of players by position")
print(players_by_position)

print("\nAverage improvement in points scored by position:")
print(avg_improvement_by_position)

combined_positions = player_totals_df[player_totals_df['pos'].isin(['SF-SG', 'SG-PF'])]
print(combined_positions[['player', 'season', 'pts', 'pts_diff']])

# Calculate median improvement in points scored by position
median_improvement_by_position = player_totals_df.dropna(subset=['pts_diff']).groupby('pos')['pts_diff'].median()

min_games = 20
player_totals_df_filtered = player_totals_df[player_totals_df['g'] >= min_games]
median_improvement_filtered = player_totals_df_filtered.dropna(subset=['pts_diff']).groupby('pos')['pts_diff'].median()

print("\nMedian improvement in points scored by position:")
print(median_improvement_by_position)

print("\nMedian improvement in points scored by position with at least 20 games played:")
print(median_improvement_filtered)