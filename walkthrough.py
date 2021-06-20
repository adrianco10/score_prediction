import pandas as pd
import streamlit as st
from scipy.stats import poisson
from PIL import Image
import numpy as np
import text


# function to load la liga stats into csv, turn into df and sum up all home and away goals
# stats from https://fbref.com/en/comps/12/La-Liga-Stats
# function to read csv and sum home and away goals
def sum_of_home_away_goals():
    cols_list = ['Squad', 'GF', 'GA', 'GF_away', 'GA_away']
    df = pd.read_csv('goals_table.csv', usecols=cols_list)
    home_goals = df['GF'].sum()
    away_goals = df['GF_away'].sum()

    df2 = {'Squad': 'Total', 'GF': df['GF'].sum(), 'GF_away': df['GF_away'].sum()}
    df = df.append(df2, ignore_index=True)

    return home_goals, away_goals, df


# function to calculate average goals per match using sum of home and away goals as arguments
def average_goals_per_match(home_sum, away_sum):
    home_matches = 380
    away_matches = 380
    home_goals_per_match = home_sum / home_matches
    away_goals_per_match = away_sum / away_matches

    return home_goals_per_match, away_goals_per_match


# function to calculate the average number of goals scored by each team both at home and away
def team_goal_averages():
    cols_list = ['Squad', 'GF', 'GA', 'GF_away', 'GA_away']
    df = pd.read_csv('goals_table.csv', usecols=cols_list)
    home_goal_average = df['GF'] / 19
    away_goal_average = df['GF_away'] / 19
    avg_home_goals_conceded = df['GA'] / 19
    avg_away_goals_conceded = df['GA_away'] / 19
    df['home_goal_average'] = home_goal_average
    df['away_goal_average'] = away_goal_average
    df['avg_home_goals_conceded'] = avg_home_goals_conceded
    df['avg_away_goals_conceded'] = avg_away_goals_conceded

    return df


# function takes existing dataframe as argument and uses existing columns to calculate attack and defense ratings
def atk_def_strength(df):
    home_goal_avg = 1.3684
    away_goal_avg = 1.1395
    # calculate home atk strength
    atk_strength_home = df['home_goal_average'] / home_goal_avg
    df['home_atk_str'] = atk_strength_home
    # calculate home def strength
    def_str_home = df['avg_home_goals_conceded'] / away_goal_avg
    df['home_def_str'] = def_str_home
    # calculate away atk strength
    atk_strength_away = df['away_goal_average'] / away_goal_avg
    df['away_atk_str'] = atk_strength_away
    # calculate away def strength
    def_str_away = df['avg_away_goals_conceded'] / home_goal_avg
    df['away_def_str'] = def_str_away

    return df


# function that calculates goal expectancy for a home and away team using previously gathered data as arguments
def goal_expectancy(atk_home, defence_away, atk_away, def_home, homegoalavg, awaygoalavg):
    xg_home = atk_home * defence_away * homegoalavg
    xg_away = atk_away * def_home * awaygoalavg

    return xg_home, xg_away


# function that employs the Poisson formula from the Scipy library to calculate goal probability
def poisson_formula(xgoalhome, xgoalaway):
    home_team = []
    away_team = []
    for goal in range(0, 6):
        home_team_goal_prob = (poisson.pmf(goal, xgoalhome))
        home_team.append(home_team_goal_prob)
    for away_goal in range(0, 6):
        away_team_goal_prob = poisson.pmf(away_goal, xgoalaway)
        away_team.append(away_team_goal_prob)
    home_team = pd.DataFrame(home_team, columns=['Probability'])
    away_team = pd.DataFrame(away_team, columns=['Probability'])

    return home_team, away_team


# take two dataframes as arguments(which contain goal probabilities for home and away teams)
# and return list of the products of every row of 1st dataframe multiplied by
# every row of 2nd dataframe
def match_outcome(df1, df_2):
    scoreline = []
    for x in df1['Probability']:
        for y in df_2['Probability']:
            score_probability = round(x * y, 3)
            scoreline.append(score_probability)

    return scoreline


# generator function to separate list into chunks of n-size
def chunks(lst, n):
    for a in range(0, len(lst), n):
        yield lst[a:a + n]


# loops through generator items and appends them to empty list
def scorelist(gen_object):
    score_list = []
    for item in gen_object:
        score_list.append(item)

    return score_list


# function that takes goal probability dataframe as argument and extracts
# all the probabilities where the home teams wins using, then sums them together
# to give odds of home team winning
def team_odds(goal_dataframe):
    home_list = []
    away_list = []
    tie_list = []
    h = 1  # home
    a = 1  # away
    t = 0  # tie

    while h <= 5 and a <= 5:
        home_list.append(goal_dataframe.iloc[h, 0:h])
        h += 1
        away_list.append(goal_dataframe.iloc[0:a, a])
        a += 1
    while t <= 5:
        tie_list.append(goal_dataframe.iloc[t, t])
        t += 1

    home_list = np.hstack(home_list)
    home_odds = round(sum(home_list) * 100, 2)
    away_list = np.hstack(away_list)
    away_odds = round(sum(away_list) * 100, 2)
    tie_list = np.hstack(tie_list)
    tie_odds = round(sum(tie_list) * 100, 2)

    return home_odds, away_odds, tie_odds


def walkthrough():
    hgoals, agoals, dataFrame = sum_of_home_away_goals()
    avg_home_goals, avg_away_goals = average_goals_per_match(hgoals, agoals)
    team_averages_df = team_goal_averages()

    df2 = pd.DataFrame({'Average_home_goals/match': [avg_home_goals], 'Average_away_goals/match': [avg_away_goals]})
    df2.index = ['La Liga Teams']

    st.title('Predicting La Liga scores and results using Python')
    ligateams = Image.open('La-Liga-teams.jpg')
    st.image(ligateams)
    text.intro()
    text.goals_1st()
    st.dataframe(dataFrame)
    text.goals_2nd()
    st.dataframe(df2)
    text.so_average()
    st.dataframe(team_averages_df)
    pain = Image.open('disappointed.jpg')
    st.image(pain, caption='Pain')
    text.attack_n_defence()
    atk_def = atk_def_strength(team_averages_df)
    atk_def = atk_def.set_index('Squad')
    st.dataframe(atk_def)
    text.goal_expectancy()

    l_col, r_col = st.beta_columns(2)
    with st.form('Home and Away'):
        home = [l_col.selectbox('Home Team', atk_def.index)]  # use index of team names as selection options
        if team_averages_df['Squad'].isin(home).any():
            l_col.write(atk_def.loc[home, ['home_atk_str', 'home_def_str']])  # loc[row_label, column_label]
        away = [r_col.selectbox('Away team', (team_averages_df['Squad']))]
        if team_averages_df['Squad'].isin(away).any():
            r_col.write(atk_def.loc[away, ['away_atk_str', 'away_def_str']])
        submitted = st.form_submit_button("Calculate Goal Expectancy")
        if submitted:
            st.balloons()
            # stripping unwanted chars from string to be able to match in dataframe later
            home = str(home)
            away = str(away)
            chars = "[]'"
            for we in chars:
                home = home.replace(we, '')
                away = away.replace(we, '')
            # home team's atk strength and away team's defence strength
            homeattack = atk_def.at[
                home, 'home_atk_str']  # df.at[row_label, column_label] will return single value of cell
            awaydefence = atk_def.at[away, 'away_def_str']
            # away team's attack strength and home team's defence strength
            awayattack = atk_def.at[away, 'away_atk_str']
            homedefence = atk_def.at[home, 'home_def_str']
            # Extract League goal averages
            homegoalaverage = df2.at['La Liga Teams', 'Average_home_goals/match']
            awaygoalaverage = df2.at['La Liga Teams', 'Average_away_goals/match']
            # calling predefined function we created to calculate and return goal expectancy for both teams. Takes
            # attack and defensive strength for both teams as arguments and does the required calculations
            xgoals_home, xgoals_away = goal_expectancy(homeattack, awaydefence, awayattack, homedefence,
                                                       homegoalaverage, awaygoalaverage)
            xgoals_home = round(xgoals_home, 4)
            xgoals_away = round(xgoals_away, 4)
            l_col.info(f"{home}'s goal expectancy is **{xgoals_home}**")
            r_col.info(f"{away}'s goal expectancy is **{xgoals_away}**")
            text.poisson()

            try:
                left_col2, right_col2 = st.beta_columns(2)
                home_goal_probabilities, away_goal_probabilities = poisson_formula(xgoals_home, xgoals_away)
                left_col2.subheader(f"{home}'s goal probability playing {away} at home")
                left_col2.dataframe(home_goal_probabilities)
                right_col2.subheader(f"{away}'s goal probability playing {home} away")
                right_col2.dataframe(away_goal_probabilities)

                text.match_outcomes()

                scoreline_probs = match_outcome(home_goal_probabilities, away_goal_probabilities)
                score_chunks = chunks(scoreline_probs, 6)
                list_of_scores = scorelist(score_chunks)
                goal_prob_df = pd.DataFrame(list_of_scores, columns=['0', '1', '2', '3', '4', '5'],
                                            index=['0', '1', '2', '3', '4', '5'])
                goal_prob_df.index.name = f"{home}"
                st.dataframe(goal_prob_df)
                home_win, away_win, tie = team_odds(goal_prob_df)

                with st.beta_expander('View Code'):
                    st.code('''
        # take two dataframes as arguments(which contain goal probabilities for home and 
       # away teams and return list containing products of every row of 1st dataframe 
       # multiplied by every row of 2nd dataframe
       def match_outcome(df1, df_2):
           scoreline = []
           for x in df1['Probability']:
               for y in df_2['Probability']:
                   score_probability = round(x * y, 4)
                   scoreline.append(score_probability)

           return scoreline


       # generator function to separate list into chunks of n-size, where n is
       # determined by how many outcomes/goals we would like to calculate, which in
       # our case is up to 5 goals. So our chunks would be 6 items long because a score 
       # of 0-0 is still valid
       def chunks(lst, n):
           for a in range(0, len(lst), n):
               yield lst[a:a + n]


       # loops through generator items and appends them to empty list
       def scorelist(gen_object):
           score_list = []
           for item in gen_object:
               score_list.append(item)

           return score_list

       scoreline_probs = match_outcome(home_goal_probabilities, away_goal_probabilities)
       score_chunks = chunks(scoreline_probs, 6)
       list_of_scores = scorelist(score_chunks)
       goal_prob_df = pd.DataFrame(list_of_scores, columns=['0', '1', '2', '3', '4', '5'],
                                                   index=['0', '1', '2', '3', '4', '5'])''')

                text.tell_me_odds()
                my_string4 = f"For the teams you chose above these should be the estimated probabilities for each outcome:\n" \
                             f"\n1. Chance that {home} (home) wins = **{home_win}%**\n" \
                             f"\n2. Chance that {away} (away) wins = **{away_win}%**" \
                             f"\n3. Chance of a tie = **{tie}%**"
                st.markdown(my_string4)
                with st.beta_expander("View Code"):
                    st.code('''# function that takes goal probability dataframe as argument and extracts
       # all the probabilities where the home teams wins then sums them together
       # to give probability of home win, away win and tie
       def team_odds(goal_dataframe):
           home_list = []
           away_list = []
           tie_list = []
           h = 1  # home
           a = 1  # away
           t = 0  # tie

           while h <= 5 and a <= 5:
               home_list.append(goal_dataframe.iloc[h, 0:h])
               h += 1
               away_list.append(goal_dataframe.iloc[0:a, a])
               a += 1
           while t <= 5:
               tie_list.append(goal_dataframe.iloc[t, t])
               t += 1

           home_list = np.hstack(home_list)
           home_odds = round(sum(home_list) * 100, 2)
           away_list = np.hstack(away_list)
           away_odds = round(sum(away_list) * 100, 2)
           tie_list = np.hstack(tie_list)
           tie_odds = round(sum(tie_list) * 100, 2)

           return home_odds, away_odds, tie_odds''')
                text.conclusion()
                st.markdown("-Adrian Cortes")

            except NameError as name:
                st.info(
                    "To proceed choose two teams above and click **'Calculate Goal Expectancy'** to see their goal expectancy."
                    " You should then also see their respective goal probability tables here.")
