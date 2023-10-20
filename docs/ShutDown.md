Question:
How does a teams ability to hold onto their shutdown relate to winrate and performance?

Thesis: Shutdowns are generate through advantages and controlling is on of the main mechanics from preventing swings and comebacks. Thus a team that is able to consistently generate and hold onto shutdown will have high quality, dominating play.

This additionally avoids the issues of having to analyse the circumsntaces in which a kill happens to decide whether it is good or not, since large shutdown are almost alwas bad and kills with shutdowns are in a way events already wieghted with importance according to the games internal systems.



Checking for effect of shutdown control on wr in the same game probably not diff from 

time for how long a shutdown gets held? (not worried rn)


# Create Views

1. Create view of the maximum shutdown teams held in each game
```sql
CREATE OR REPLACE VIEW lol.shutdown_max as
select 
    platformgameid,
    max(participants[1].shutdownvalue + participants[2].shutdownvalue + participants[3].shutdownvalue + participants[4].shutdownvalue + participants[5].shutdownvalue )as BlueTeamShutdown,
    max(participants[6].shutdownvalue + participants[7].shutdownvalue + participants[8].shutdownvalue + participants[9].shutdownvalue + participants[10].shutdownvalue) as RedTeamShutdown
from lol.games
where
    eventtype = 'stats_update' and 
    participants[1].shutdownvalue > 0
group by platformgameid
```

2. create view of shutdown collected each game
```sql
CREATE OR REPLACE VIEW lol.shutdown_collected as
select
    g.platformgameid,
    tg.teamid,
    side,
    sum(shutdownbounty) as shutdownbounty
from lol.games as g, lol.team_games as tg
where
    eventtype = 'champion_kill'
    and killerteamid = side
    and g.platformgameid = tg.platformgameid
group by g.platformgameid, tg.teamid, side
```

3. Join the views

```sql create_gold_diff_wins.sql
CREATE OR REPLACE VIEW lol.shutdowns as
SELECT 
    *
FROM "lol"."shutdown_max"
INNER JOIN "lol"."shutdown_collected" ON lol.shutdown_max.platformgameid=lol.shutdown_collected.platformgameid
```
