# Power Rankings Hackathon: GNAR-Score
<img src="images/gentleman_gnar.webp" alt="Gentleman Gnar" width="400"/>

This is an entry for the [DevPost Power Ranking Hackathon](https://lolglobalpowerrankings.devpost.com/).

https://docs.google.com/document/d/1wFRehKMJkkRR5zyjEZyaVL9H3ZbhP7_wP0FBE5ID40c
The PDF Version can be found [here](mf-pdf-linlk.com).  
The video showcase of this entry can be be found here.
# Introduction

This is an entry to the Devpost Power Rankings Hackathon 2023. I am a Software Engineer based in Berlin, Germany and have been a long time player of League of Legends and follower of it's esports scene.  
League of legends offers a lot of variations in micro decision and skill expression through fast, reactive gameplay and cool combos, and also big picture, strategic thinking and organized team work which make it a fascinating environment to analyze.

The GNAR(Gaussian Naive Adjusted Ranking)-Score is based on a Elo formula, whose predictive properties have been 
improved using the output of a Gaussian Naive Bayes classifier trained on historical data.

# Entry
My Entry into this hackathon is in the form of an API. This API is available under 
https://usm38g8rwj.execute-api.eu-central-1.amazonaws.com/api where all the required endpoints are available. 
The first 20 teams of the global rankings system can be fetched with the following curl command:
here is a curl command for each endpoitn
```bash
# get the global rankind (first 20 teams)
curl 'https://usm38g8rwj.execute-api.eu-central-1.amazonaws.com/api/global_rankings?number_of_teams=20'

# get rankings for a list of team_ids
curl 'https://usm38g8rwj.execute-api.eu-central-1.amazonaws.com/api/team_rankings?team_ids=98767991926151025,107563714667537640,98767991853197861,100205573495116443'

# get the rankings for teams in a tournament by tournament_id
curl 'https://usm38g8rwj.execute-api.eu-central-1.amazonaws.com/api/tournament_rankings/110733838935136200'
```
<div class="page"/>

# Tech Stack
- The API is written in Python with the Chalice framework from AWS
- AWS Lambda and ApiGateway for hosting the API
- S3 for accessing hackathon data and hosting data for the API
- Athena for exploring and exporting data
- Terraform to configure required infrastructure and permission


Python was chosen because my familiarity with the language and because it's ecosystem offers good libraries for both api development and data science tasks.
Chalice is a Python library that allows us to easily deploy out code to AWS with lambda and API Gateway, using syntax that is similar to other common python api frameworks like flask and fast-api.
The Data from S3 was used to create tables in Athena as per the guide.

## Basic Statistical Indicators

To begin building a predictive model we can start by looking at some basic statistics indicators. A few somewhat obvious choices
are first blood, first tower and first inhibitor.
Out of the 25255 games in the dataset, Blue won 13350 games and red 11903. Therefore the blue side has a 64% winrate after getting first blood,
while the red side has 0.59.
The following table also includes the winrates per for first tower and first inhibitor.

| Side | Total Game | Wins  | First Blood WR | First Tower WR | First Inhib WR |
|------|------------|-------|----------------|----------------|----------------|
| Blue | 25255      | 13352 |    0.63953     | 0.69689        | 0.94578        |
| Red  | 25255      | 11903 |    0.58693     | 0.67633        | 0.94511        |

These stats might be interesting, but are only use for predicting the outcome of the game live as it is being played out. And event like the first inhibitor only happen  quite late into the game, ideally we would like to make predictions earlier, even before the games starts

## Historic Performance through rolling averages
When trying to predict the outcome of a game we want to use data about past performance to predict to outcome
of the next game. We can combine the stats of past games by averaging them together.
For example, if in the last last 3 games, Team A has gotten 21, 15 and 30 kills. Its kill average would be 22.
WE can also average out information about the stats above by for example count ting the the past games where a team got first blood as 1 and games where it didnt as 0. A team that has gotten first blood in 2/3 last games would have a average first blood ratio of 0.66.
In addtion to the datapoint above i have also collected data on kills and deaths eachgame, and data about cs and level lead in the early game.
The process of preparing this data is detail in the preprocessing jupyter notebook.

We calculate the rolling avareg over the last 6 games for all of our data points, and can use the resulting data as input in a Gaussian Naive Bayes classifier, included in the scikit-learn python library.



# Elo System

The rating system is implemented using an Elo system. The reason for this is the process directness and simplicity. While the specific formulas or parameters can differ between elo system, the most important part is that their purely result based systems. It makes no assumptions about which strategies, mid term goals or game play patters are preferable or desirable.  
The attribution of points depends only on a teams ability to win, and nothing else. This approach is a convenient way to cut through all the complexity and variance of a competitive game like league and easily derive and objective rating the accurate reflects relative strength base on past performance.  
No doubt this is the reason these kinds of system are across many competitive games and sports such as chess, tennis and football.

K_Factor = 32
K_Factor_Scaling = 
expected_score_blue = 1/(1+10**((red_elo-blue_elo)/480))
Elo = Old_elo + (K_FACTOR*(1-expected_score_blue)*blue_game_wins)

# K-Factor Scaling
- account for importance of different kinds of matches
- scaling based on bo5 nr
