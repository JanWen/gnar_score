# Create First Blood View
```sql create_first_tower_view
CREATE OR REPLACE VIEW lol.first_tower as
select min(gametime) as gametime, platformgameid, teamid
from lol.games
where eventtype = 'building_destroyed'
group by platformgameid, teamid
```

# Create Joined View
```sql create_first_tower_wins.sql
CREATE OR REPLACE VIEW lol.first_tower_wins as
SELECT
    lol.first_tower.platformgameid,
    gametime,
    teamid as ownerteamid,
    winningteam
    FROM "lol"."first_tower"
INNER JOIN lol.wins ON lol.wins.platformgameid=lol.first_tower.platformgameid
```


# First Tower by Team
```sql
SELECT
    team_id,
    name,
    count(*) as Games,
    sum(case when winningteam = side then 1 else 0 end) AS Wins,
    sum(case when ownerteamid != side then 1 else 0 end) as FirstTower,
    sum(case when ownerteamid != side and side = winningteam then 1 else 0 end) as FirstTowerWins
FROM "lol"."first_tower_wins"as fb, lol.team_games as tg, lol.teams as t
where 
    fb.platformgameid = tg.platformgameid
    and teamid = team_id
group by team_id, name
```