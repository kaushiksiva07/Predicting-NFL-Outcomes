import pandas as pd
import nfl_data_py as nfl
import numpy as np
from .models import GameStats

def import_pbp_data(seasons):
    """
    Imports play-by-play data for the given NFL seasons.
    """
    pbp_data = pd.concat([nfl.import_pbp_data([season], downcast=True) for season in seasons])
    return pbp_data

def calculate_epa(pbp_data):
    """
    Calculates the EPA for rushing and passing for each team, season, and week.
    """
    rush_off_epa = pbp_data.loc[pbp_data['rush_attempt'] == 1].groupby(['posteam', 'season', 'week'], as_index=False)['epa'].mean()
    rush_def_epa = pbp_data.loc[pbp_data['rush_attempt'] == 1].groupby(['defteam', 'season', 'week'], as_index=False)['epa'].mean()
    pass_off_epa = pbp_data.loc[pbp_data['pass_attempt'] == 1].groupby(['posteam', 'season', 'week'], as_index=False)['epa'].mean()
    pass_def_epa = pbp_data.loc[pbp_data['pass_attempt'] == 1].groupby(['defteam', 'season', 'week'], as_index=False)['epa'].mean()

    # Shift epa values by one game to predict next one
    rush_off_epa['epa_shifted'] = rush_off_epa['epa'].shift()
    pass_off_epa['epa_shifted'] = pass_off_epa['epa'].shift()
    rush_def_epa['epa_shifted'] = rush_def_epa['epa'].shift()
    pass_def_epa['epa_shifted'] = pass_def_epa['epa'].shift()

    # Exponentially weighted EPA's
    rush_off_epa['ewma'] = rush_off_epa['epa_shifted'].ewm(min_periods=1, span=10).mean()
    pass_off_epa['ewma'] = pass_off_epa['epa_shifted'].ewm(min_periods=1, span=10).mean()
    rush_def_epa['ewma'] = rush_def_epa['epa_shifted'].ewm(min_periods=1, span=10).mean()
    pass_def_epa['ewma'] = pass_def_epa['epa_shifted'].ewm(min_periods=1, span=10).mean()

    return rush_off_epa, rush_def_epa, pass_off_epa, pass_def_epa

def dynamic_window(epa_data):
    """
    Defines a dynamically shifting window for EPA calculations.
    """
    values = np.zeros(len(epa_data))
    for i, (index, row) in enumerate(epa_data.iterrows()):
        epa = epa_data.epa_shifted.iloc[:i+1]
        if row.week > 10:
            values[i] = epa.ewm(min_periods=1, span=row.week).mean().values[-1]
        else:
            values[i] = epa.ewm(min_periods=1, span=10).mean().values[-1]

    return pd.Series(values, index=epa_data.index)

def final_stats(pbp_data, rush_off_epa, rush_def_epa, pass_off_epa, pass_def_epa):
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

    # Compute average EPA by week and add to epa dataframe
    means = epa.groupby(['season', 'week'], as_index=False)[[column for column in epa.columns if 'dynamic' in column]].mean()
    means['avg_epa'] = means[[column for column in epa.columns if 'dynamic' in column]].mean(axis=1)
    means = means[['season', 'week', 'avg_epa']]
    epa = epa.merge(means, on = ['season', 'week'])

    # Drop first week of data
    epa = epa.loc[epa['season'] != epa['season'].unique()[0], :]
    epa = epa.reset_index(drop=True)
    
    return epa

def get_schedule(week):
    sched = nfl.import_schedules([2023])
    sched[['away_team', 'home_team']] = sched[['away_team', 'home_team']].astype(str)
    wk = sched.loc[sched['week'] == week][['season', 'week', 'home_team', 'away_team', 'result']]
    return wk

def main_function():
    GameStats.objects.all().delete()
    seasons = range(2013, 2024)
    pbp_data = import_pbp_data(seasons)
    rush_off_epa, rush_def_epa, pass_off_epa, pass_def_epa = calculate_epa(pbp_data)
    stats = final_stats(pbp_data, rush_off_epa, rush_def_epa, pass_off_epa, pass_def_epa)
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


# Main execution
if __name__ == "__main__":
    main_function()
