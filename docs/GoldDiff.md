# Crate Team Gold View
```sql
CREATE OR REPLACE VIEW lol.team_gold as
select
    platformgameid,
    min(gametime) as gametime,
    min(teams[1].totalgold) as blue_gold,
    min(teams[2].totalgold) as red_gold
from lol.games
where eventtype = 'stats_update' and gametime > 900000
group by platformgameid
```

# Create Joined View
```sql create_gold_diff_wins.sql
CREATE OR REPLACE VIEW lol.gold_diff as
SELECT 
    team_gold.platformgameid,
    gametime,
    blue_gold,
    red_gold,
    blue_gold-red_gold as gold_diff,
    winningteam
FROM "lol"."team_gold"
INNER JOIN lol.wins ON lol.wins.platformgameid=lol.team_gold.platformgameid
```

```sql
SELECT
    team_id,
    name,
    count(*) as Games,
    sum(case when winningteam = side then 1 else 0 end) AS Wins,
    sum(case when side = 100 and gold_diff > 150 then 1 else 0 end) AS BlueGoldAdv,
    sum(case when side = 100 and gold_diff > 150 and winningteam = side  then 1 else 0 end) AS WinsBlueGoldAdv,
    sum(case when side = 200 and gold_diff > -150 then 1 else 0 end) AS RedGoldAdv,
    sum(case when side = 200 and gold_diff > -150 and winningteam = side  then 1 else 0 end) AS WinsRedGoldAdv
FROM "lol"."gold_diff"as fb, lol.team_games as tg, lol.teams as t
where 
    fb.platformgameid = tg.platformgameid
    and teamid = team_id
group by team_id, name
```
