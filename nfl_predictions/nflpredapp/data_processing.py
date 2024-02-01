import pandas as pd
import nfl_data_py as nfl
import numpy as np
from .models import GameStats

def import_pbp_data(seasons):
    """
    Imports play-by-play data for the given NFL seasons.
    """
    cols = ['season', 'week', 'posteam', 'defteam', 'home_team', 'away_team', 'home_score', 'away_score', 'rush_attempt', 'pass_attempt', 'epa']
    pbp_data = nfl.import_pbp_data(seasons, cols, downcast=True)

    return pbp_data

def calculate_epa(pbp_data):
    """
    Function to calculate the EPA for rushing and passing for each team, season, and week.
    """
    # Pre-filter data for rush and pass attempts to avoid repetitive computations
    rush_attempts = pbp_data[pbp_data['rush_attempt'] == 1]
    pass_attempts = pbp_data[pbp_data['pass_attempt'] == 1]

    # Function to compute grouped mean and shifted ewma
    def compute_epa(data, group_fields):
        grouped_data = data.groupby(group_fields, as_index=False)['epa'].mean()
        return grouped_data

    # Apply the compute_epa function for each scenario
    rush_off_epa = compute_epa(rush_attempts, ['posteam', 'season', 'week'])
    rush_def_epa = compute_epa(rush_attempts, ['defteam', 'season', 'week'])
    pass_off_epa = compute_epa(pass_attempts, ['posteam', 'season', 'week'])
    pass_def_epa = compute_epa(pass_attempts, ['defteam', 'season', 'week'])

    return rush_off_epa, rush_def_epa, pass_off_epa, pass_def_epa

def dynamic_window(epa_data):
    # Use numpy to create an array of the same shape as epa_data
    values = np.zeros(epa_data.shape[0])

    # Determine the span for each row
    span = np.where(epa_data['week'] > 10, epa_data['week'], 10)

    # Vectorized operation to calculate exponentially weighted mean
    for i in range(len(values)):
        values[i] = epa_data['epa_shifted'].iloc[:i+1].ewm(min_periods=1, span=span[i]).mean().iloc[-1]

    return pd.Series(values, index=epa_data.index)

def dynamic_window(epa_data):
    # Use numpy to create an array of the same shape as epa_data
    values = np.zeros(epa_data.shape[0])

    # Determine the span for each row
    span = np.where(epa_data['week'] > 10, epa_data['week'], 10)

    # Vectorized operation to calculate exponentially weighted mean
    for i in range(len(values)):
        values[i] = epa_data['epa'].iloc[:i+1].ewm(min_periods=1, span=span[i]).mean().iloc[-1]

    return pd.Series(values, index=epa_data.index)

def final_stats(rush_off_epa, rush_def_epa, pass_off_epa, pass_def_epa):
    # Compute dynamically shifted EPA's
    rush_off_epa['ewma_dynamic'] = rush_off_epa.groupby('posteam').apply(dynamic_window).values
    pass_off_epa['ewma_dynamic'] = pass_off_epa.groupby('posteam').apply(dynamic_window).values
    rush_def_epa['ewma_dynamic'] = rush_def_epa.groupby('defteam').apply(dynamic_window).values
    pass_def_epa['ewma_dynamic'] = pass_def_epa.groupby('defteam').apply(dynamic_window).values

    # Combine EPA into offense and defense
    off_epa = rush_off_epa.merge(pass_off_epa, on=['posteam', 'season', 'week'], suffixes=['_rush', '_pass']).rename(columns={'posteam': 'team'})
    def_epa = rush_def_epa.merge(pass_def_epa, on=['defteam', 'season', 'week'], suffixes=['_rush', '_pass']).rename(columns={'defteam': 'team'})

    # Combine offense and defense into one table
    epa = off_epa.merge(def_epa, on=['team', 'season', 'week'], suffixes=['_off', '_def'])

    # # Drop first week of data
    epa = epa.loc[~((epa['season'] == 2013) & (epa['week'] == 1))]
    epa = epa.reset_index(drop=True)

    return epa

def get_schedule(week):
    sched = nfl.import_schedules([2023])
    sched[['away_team', 'home_team']] = sched[['away_team', 'home_team']].astype(str)
    wk = sched.loc[sched['week'] == week][['season', 'week', 'home_team', 'away_team', 'result']]
    return wk

def main_function():
    GameStats.objects.all().delete()
    seasons = list(range(2013, 2024))
    pbp_data = import_pbp_data(seasons)
    rush_off_epa, rush_def_epa, pass_off_epa, pass_def_epa = calculate_epa(pbp_data)
    stats = final_stats(rush_off_epa, rush_def_epa, pass_off_epa, pass_def_epa)
    for week in range(1, 19):
        if week > 1:
            prev_stats = stats.loc[(stats['week'] == (week - 1)) & (stats['season'] == 2023)]
        else:
            prev_stats = stats.loc[(stats['week'] == (17)) & (stats['season'] == 2022)]


        # Import Week's Schedule
        wk = get_schedule(week)
        home_pred = wk.merge(prev_stats.rename(columns={'team': 'home_team'}), on=['home_team'])
        away_pred = wk.merge(prev_stats.rename(columns={'team': 'away_team'}), on=['away_team'])
        final_pred = home_pred.merge(away_pred, on=['season_x', 'week_x', 'home_team', 'away_team'], suffixes=('_home', '_away'))

        for index, row in final_pred.iterrows():
            game = GameStats(
                week=week,
                home_team=row['home_team'],
                away_team=row['away_team'],
                ewma_dynamic_rush_off_home=row['ewma_dynamic_rush_off_home'], 
                ewma_dynamic_pass_off_home=row['ewma_dynamic_pass_off_home'],
                ewma_dynamic_rush_def_home=row['ewma_dynamic_rush_def_home'],
                ewma_dynamic_pass_def_home=row['ewma_dynamic_pass_def_home'],
                ewma_dynamic_rush_off_away=row['ewma_dynamic_rush_off_away'],
                ewma_dynamic_pass_off_away=row['ewma_dynamic_pass_off_away'],
                ewma_dynamic_rush_def_away=row['ewma_dynamic_rush_def_away'],
                ewma_dynamic_pass_def_away=row['ewma_dynamic_pass_def_away'],
            )
            game.save()

    
def data_already_exists():
    if GameStats.objects.exists():
        return True
    else:
        return False


# Main execution
if __name__ == "__main__":
    if not data_already_exists():
        main_function()
