## Inspiration
I am a long time player of League of Legends and follower of it's esports scene.  
The combination of micro decision and skill expression through fast, reactive game play and cool combos but and also big picture, strategic thinking and organized team work is what makes League of Legends a fascinating game to play and analyze.   
This way the League of Legends community provides a fun and interesting environment for me to expand my knowledge of statistic and data analytics.
## What it does
The project ranks League of Legends teams based on a Elo system. The expected outcomes based on elo difference are weighted with the predictions of a classification model, trained on past data with the Gaussian Naive Bayes technique to increase the predictive power of the elo system as a whole.
## How we built it
Developed locally with python and deployed on AWS with Chalice. Data was explored and exported using Athena.
## Challenges we ran into
- Large dataset with some missing data took a while to explore
- Low sample size for matches between teams of different regions
- Lots of moving parts made iterative tuning difficult
## Accomplishments that we're proud of
- Predictive model suprisingly good for realtively siumple features
- Succefully combined two different types of models for common goal
- Gained confinecd in my ability to wrangle and alayse data
## What we learned
- How to tune an elo system for predictive performance
- Predictive models are still usefull in highly random environments like league
- A lot of sql and pandas
