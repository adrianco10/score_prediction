# this script simply contains all the streamlit text that makes up the page

import streamlit as st
from PIL import Image

def intro():
    st.markdown(
        "I set out to create a soccer score and result prediction program using Poisson distribution and Python. "
        "The Poisson Formula is a probablity theory that can be used alongside historical sports data to predict outcomes of sporting"
        " events. ")
    st.markdown(
        "This can be done by other means of course and there are websites and calculators already out there "
        "but since I have been learning Python for a couple of years"
        " now and I wanted to challenge myself with a custom project."
        " Specifically the challenge was to use Python to program a tool to dynamically calculate the"
        " probability of any scoreline for any given matchup between teams in the Spanish top flight (La Liga) and"
        " then use those stats to also predict the result of the game (home win, away win, and tie).")

    st.markdown(
        "To be able to use the Poisson formula however we first need to gather quite a bit of data. What follows"
        " is an account of how I went about creating the tool including the code for each major section. So without "
        "wasting any more time I'm just jumping right into it!\n\n To make sure I was doing everything right I used "
        "this page as a guide:https://www.thepunterspage.com/poisson-distribution-betting/.")

    st.info("To reiterate: This page walks through the process and steps that I took to create the tool. If you "
            "just want to check out the tool itself without all the numbers click on the selection box in the top left.")


def goals_1st():
    st.subheader(':soccer:Goals, Goals, and More Goals:soccer:')
    goals = Image.open('goalphoto.jpg')
    st.image(goals, caption='Photo from:https://www.pri.org/stories/2014-07-01/when-did-simple-goal-become-goooooooooooooal')
    st.markdown("To start we first need some preliminary stats like the average goal expectancy for home and "
                "away games for all teams and also the attack and defence strength for every team in the league. "
                "To find these we also need three other pieces of data first which will basically build the foundation"
                " for all our future calculations: ")
    st.markdown('1. Total **home goals** scored by all teams')
    st.markdown('2. Total **away goals** scored by all teams')
    st.markdown('3. **Average** number of **home goals and away goals per match** for the whole league')

    st.markdown(
        "To do this I relied on the home/away league table stats from https://fbref.com/en/comps/12/La-Liga-Stats."
        " I downloaded the data as a CSV file and then converted that into a pandas dataframe*. From here I found"
        " the sum of the home goals column [GF] and away goals column [GF_away] using the code below:")
    st.info("*Pandas is a Python language"
            " software library that is very helpful for tasks that have to do with data manipulation and analysis.")

    with st.beta_expander('View code'):
        code = "cols_list = ['Squad', 'GF', 'GA', 'GF_away', 'GA_away'] \ndf = pd.read_csv('goals_table.csv', usecols=cols_list)\n" \
               "home_goals = df['GF'].sum() \naway_goals = df['GF_away'].sum()"
        st.code(code, language='python')


def goals_2nd():
    st.markdown(
        "With the first two stats we can calculate the average number of home goals and away goals per match "
        "for the whole league. Each team plays a total of 19 games at home and "
        "19 away. So with 20 teams in the league and knowing the total home and away goals from the previous step we "
        "can calculate the average home "
        " and away goals per match :")

    st.latex(r'''\tag*{home and away matches} 20 * 19 = 380''')
    st.latex(r'''\tag*{Avg. home goals per match}520 / 380 = 1.368''')
    st.latex(r'''\tag*{Avg. away goals per match}433 / 380 = 1.139''')
    st.markdown('We can now take these averages and plug them into a new table for use later on:')


def so_average():
    st.subheader("Averages")
    my_string = "This is where things start to get tricky; If we want a tool that can calculate the odds of any given scoreline " \
                "for any given match-up of La Liga teams then we also need to calculate the following for each team before" \
                " moving on:\n " \
                "\n1. Home goal average" \
                "\n2. Average goals conceded per home match" \
                "\n3. Away goal average" \
                "\n4. Average goals conceded per away match"

    st.write(my_string)
    st.markdown(
        "Thankfully everything builds on top of each other and we already have some of the stats needed to "
        "calculate these figures. We could of course do this manually for each team but my aim is to use python "
        "all throughout this project and make it dynamic so I can just pick a matchup between two teams and immediately "
        "see the corresponding score probabilities. We can use the dataframe from above to calculate the new stats we need and add these"
        " as new columns in the same dataframe. Both the updated dataframe and code used are below:")

    with st.beta_expander('View code'):
        st.code('''def team_goal_averages():
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

                   return df''')




def attack_n_defence():
    st.subheader('Attack and Defence Strength')
    st.markdown(
        "Now we're getting somewhere! With most of the preliminary stats in hand we can now begin to calculate both the attack"
        " and defensive strength of each individual team. For this step we will again be relying on the new iteration of"
        " the dataframe above and adding new columns to represent each team's attack and defence strength, for both "
        " home and away matches.")

    left_col, right_col = st.beta_columns(2)
    left_col.info(
        "**Attack strength is a team’s avg. number of goals scored, divided by the league’s average number of "
        "goals scored**.")
    right_col.info(
        "**Defence strength is team's avg. number of goals conceded divided by league average number of "
        "goals conceded**")
    st.markdown(
        "We know each team's average number of goals scored and conceded, both at home and away, and if you remember, the"
        " equivalent stats for the league was also one of the first things we calculated. So knowing we have this data in hand"
        " in our updated dataframe I created a function that took said dataframe (which again has all the info we need) "
        "and uses the data already present to calculate the following for each team: "
        "")
    my_string2 = "1. Attack strength when playing at home\n" \
                 " 2. Defensive strength when playing at home\n" \
                 " 3. Attack strength when playing away\n" \
                 " 4. Defensive strength when playing away"
    st.write(my_string2)
    st.markdown("Once again if you're interested in the code used for this you can click below to expand it:")
    with st.beta_expander('View Code'):
        st.code('''# function takes existing dataframe as argument and uses existing columns to calculate 
               # attack and defense ratings
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

               return df''')

    st.markdown("And here is the updated dataframe! :sunglasses:")


def goal_expectancy():
    st.subheader('Goal Expectancy')
    st.markdown(
        "There is one last metric we need before we can begin to plug in values into the Poisson Formula and that"
        " is goal expectancy. We need to know the goal expectancy for both teams to be able to calculate the"
        " probability of each team's likely score. Because our dataframe now has all the info we need I've started "
        " to build out an interactive tool below so you can play around with the teams and results. You can select "
        "a home and away team and for each one you will see their respective attack and defence strengths. You "
        "can then click the button at the bottom to calculate their goal expectancy.")
    st.markdown("Code is below.")
    with st.beta_expander('View Code'):
        st.code('''l_col, r_col = st.beta_columns(2)
               with st.form('Home and Away'):
                   home = [l_col.selectbox('Home Team', atk_def.index)]
                   if team_averages_df['Squad'].isin(home).any():
                       l_col.write(atk_def.loc[home, ['home_atk_str', 'home_def_str']])  # loc[row_label, column_label]
                   away = [r_col.selectbox('Away team', (team_averages_df['Squad']))]
                   if team_averages_df['Squad'].isin(away).any():
                       r_col.write(atk_def.loc[away, ['away_atk_str', 'away_def_str']])
                   submitted = st.form_submit_button("Calculate Goal Expectancy")
                   if submitted:
                       # stripping unwanted chars from string to be able to match in dataframe later
                       home = str(home)
                       away = str(away)
                       chars = "[]'"
                       for we in chars:
                           home = home.replace(we, '')
                           away = away.replace(we, '')
                       # home team's atk strength and away team's defence strength
                       homeattack = atk_def.at[home, 'home_atk_str'] # df.at[row_label, column_label] will return single value of cell
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
                       r_col.info(f"{away}'s goal expectancy is **{xgoals_away}**")''')


def poisson():
    st.subheader("The Poisson Formula")
    st.success("Everything we need is finally in place to use the Poisson formula!")
    st.markdown(
        "This will allow us to calculate"
        " the likelihood of each possible score that we may be intrerested in. Here is a breakdown of that"
        " formula (don't ask me to explain it, I'm just plugging numbers in :sweat_smile:):")
    st.latex(r'''
                       P = \cfrac{(\lambda^ke^{-\lambda})}{k!}
                       ''')
    st.markdown("Where: ")
    my_string3 = "1. P is the probability we are trying to solve for \
                                    \n2. k is the number of goals (I'm limiting this to max of 5)\
                                    \n3. λ is the expected number of goals\
                                    \n4. e is the constant known as Euler's number(2.71828)\
                                    \n5. k! is the factorial of k(number of goals)"
    st.markdown(my_string3)
    st.markdown("We are going to do the calculations assuming a maximum of 5 goals per game, per team."
                " Perhaps in the future I will expand it but for now it's a good enough start since the "
                "possibility of a 5+ goal game by any individual team is usually pretty low even in ideal conditions.")
    st.markdown(
        "As an example: even for the team with the highest scoring average at home (Barcelona) against a "
        "team with the highest average of goals conceded away (Granada) there is only about a 4.1% "
        "chance that Barcelona score 7 goals. If you were keen on placing a very risky (A.K.A unwise) bet of Barcelona "
        "scoring 7 goals in a game, you would have the best chances of winning that bet when Barcelona plays "
        "Granada at home, but good luck, last time Barcelona put 7 past a team was September 2nd,"
        " 2018 against Huesca and nowadays, as much as it hurts to say we're more likely"
        " to concede 8 than score them...")
    image = Image.open('barca_8_goals.png')
    st.image(image, caption='PAIN')

    st.markdown(" Anyway! I figured this to be a small enough probability that we can safely omit "
                "it (probably violating some sacred rule of statistics but :shrug:)")
    st.markdown("Below you should see the goal probabilities for the teams that you chose above, again "
                "up to 5 goals each.")


def match_outcomes():
    st.subheader("Predicting match outcome using goal probabilites!")
    st.markdown(
        "Now that we can calculate the goal probability for any given matchup we can use these probabilities"
        " to create a table representing which score line has the highest chance of "
        "occurring. To find the chances of any given score line we just have to multiply the possibility"
        " of each possible score by each team, by the possibility of each possible score by the other "
        "team. For me this was a bit troublesome to code at first but I managed to find a way to get it"
        " working.")

    st.markdown("For some reason I wasn't able to get titles in the table below but just know that the "
                "left-most column represents the home team score and the top-most row represents the away "
                "team score. So if you want to know the likelihood of a 2-0 scoreline for the home team just "
                "look for the 2 on the left column and line it up with the 0 on the top row. Conversely, if "
                "you want to find the probability of a 0-2 score for the away team first find the 2 in the "
                "top row, then line it up with the 0 on the left-most column. Of course you can multiply by"
                " 100 if you want the percentages.")


def tell_me_odds():
    st.subheader("Never Tell Me The Odds")
    st.markdown(
        "So with the table above we can determine what the most likely outcome for any given matchup"
        " is. We can take this a step futher though and also use the table to find the estimated chance of "
        "a home win, an away win, or a tie!  ")
    st.markdown(
        "To find the probability of a home win we just have to add all the probabilities in the table where"
        " the home team wins i.e. 1-0, 2-0, 2-1, 3-0, 3-1 etc. all the way up to 5-4. Same thing"
        " goes for the away team. Since I know where these values are located on this dataframe/ "
        " two-dimensional array I can use some code to extract the values at these positions "
        " and sum them up.")


def conclusion():
    st.subheader("That's a wrap!")
    st.success(
        "**If you've made it this far, thank you for reading!**\n\n This was a challenging project for me and I'm"
        " proud to be able to share it with you. I'll be using this tool in the upcoming season and recording"
        " actual results to these estimated ones to determine the accuracy so I'll probaly report on"
        " that at various intervals as the season progresses.\n\n I might also decide to add other major European "
        "leagues over time.")
