# GLOBAL POWER RANKINGS HACKATHON
https://lolglobalpowerrankings.devpost.com/
https://docs.google.com/document/d/1wFRehKMJkkRR5zyjEZyaVL9H3ZbhP7_wP0FBE5ID40c/edit#heading=h.2xoljw88prx

# 


ELO system enrichen by findings from machine learning models.

# HOW TO TEST AN ELO SYSTEM

## Predictability
- elo system is not a predictive model, it is not supposed to predict failures or upsets, it is supposed to reflact them
-  consider
- predictive power can still be used to verify basic functionality of an elo system
Out of the 2488 matches included in the dataset, with this elo system 50% of matches have an elo difference of less then 103. In all these matches, blue side has a wr of 55%. 
In all matches with an elo diff greater then 103, blue side has a wr of 75%.
In all red side favoured matches with an elo diff greater then 103, the blue side win rate is 31%.
total games 2488
half_match_cutoff 103

EVEN MATCHES WR 0.55 1248
bluefav_matches WR 0.75 667
redfav_matches WR 0.31 569

These win rates / elo difference are consitent with what is observed in other rating systems used by FIDE USCF.


### Match Based Elo




IDEA: Update elo not per game but per match with increasing importance acording to games in a match
win bo5 
boX are good numerical indicator of match importance since it's unlikely you'd want important titles decided by a small nr of matches
how do we make this so the code isnt shit :thinking_face:


RESERACH:

Assing k factor to different leagues not as effective since teams dont usually move between league except for msi and worlds. so teams in major region both win and lose more elo

COMPARING RANKING SYSTEMS:
There are many ways to compare two power ranking systems. Here are a few common methods:

    Direct comparison: This is the simplest method, and it simply involves comparing the rankings of each system for each team. The system with the higher rankings for the most teams is generally considered to be the better system.
    Predictive accuracy: This method compares the ability of the two systems to predict the outcomes of future matches. This can be done by using a historical dataset of match results and comparing the predictions of the two systems to the actual outcomes.
    Sensitivity to recent results: This method compares how sensitive the two systems are to recent results. A system that is more sensitive to recent results will tend to change rankings more quickly in response to changes in team performance.
    Complexity: This method compares the complexity of the two systems. A more complex system may be more accurate, but it may also be more difficult to understand and use.
    Robustness: This method compares how robust the two systems are to changes in the data. A more robust system will be less likely to produce inaccurate rankings if the data is noisy or incomplete.


Elo rating system, the Glicko rating system, and the Sagarin rating system.

https://wismuth.com/elo/calculator.html#best_of=5&score=0-0&system=tennis-men&e_score=0.6


CHANGELOG:

13/09/2023:
Implemented a basic elo system  based on games wins
14/09/2023
Save report and images to daily folder