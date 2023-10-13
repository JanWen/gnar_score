
# Create First Blood View
```sql
CREATE OR REPLACE VIEW lol.first_blood as

select min(gametime) as gametime, platformgameid, killerteamid, winningteam
from lol.games
where eventtype = 'champion_kill'
group by platformgameid, killerteamid, winningteam
```

# Create Win View
```sql
CREATE OR REPLACE VIEW lol.wins as
select platformgameid, winningteam
from lol.games
where eventtype = 'game_end'
```

# Create Joined View
```sql create_first_blood_wins.sql
CREATE OR REPLACE VIEW lol.first_blood_wins as
SELECT * FROM "lol"."first_blood"
INNER JOIN lol.wins ON lol.wins.platformgameid=lol.first_blood.platformgameid
limit 10;
```

# Red/Blue WR Stats
```sql
SELECT count(*) AS total,
    sum(case when killerteamid = 100 then 1 else 0 end) AS BlueFB,
    sum(case when winningteam = 100 then 1 else 0 end) AS BlueWins,
    sum(case when killerteamid = 100 and winningteam = 100 then 1 else 0 end) AS BlueWinsFB,
    sum(case when killerteamid = 200 then 1 else 0 end) AS RedFB,
    sum(case when winningteam = 200 then 1 else 0 end) AS RedWins,
    sum(case when killerteamid = 200 and winningteam = 200 then 1 else 0 end) AS RedWinsFB
FROM lol.first_blood_wins
```
```
#	total	BlueFB	BlueWins	BlueWinsFB	RedFB	RedWins	RedWinsFB
1	50475	25162	26671	    13350	    25133	23804	11903
```

blue_winrate = 0.5284001981178801 \
blue_first_blood = 25162 \
blue_wins_with_fb = 13350 \
blue_winrate_with_fb_ = 0.5305619585088626 


red_winrate = 0.4715998018821199 \
RedFB = 25133 \
RedWinsFB = 11903 \
RedFbWr = 0.4736004456292524

# First Blood by Team
```sql
select name, avg(gametime) as avg_baron_kill, count(*) as games_no, min(gametime) as min_baron_kill_time
from lol.first_blood as g, lol.team_games as tg, lol.teams as t
where g.platformgameid = tg.platformgameid
  and killerteamid = side
  and teamid = team_id
group by name
-- having count(*) > 10
order by 2 asc
```