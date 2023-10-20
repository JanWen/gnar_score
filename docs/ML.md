Want and array
time team event kills_avg deths_avg wins_avg loss_avg rolling last 20 games


We create a view with the kills and deaths per team per game
```sql
create or replace view lol.games_ks as
SELECT
    g.platformgameid,
    side,
    tg.teamid,
    min(g.eventtime) as eventtime,
    max(case when w.winningteam = side then 1 else 0 end) as win,
    sum(case when killerteamid = side then 1 else 0 end) AS kills,
    sum(case when killerteamid != side then 1 else 0 end) AS deaths
FROM "lol"."games" as g, team_games as tg, lol.wins as w
where
    g.platformgameid = tg.platformgameid
    and g.platformgameid = w.platformgameid
    and eventtype = 'champion_kill'
group by g.platformgameid, side, tg.teamid
order by platformgameid
```

Then we calc thge rolling avg of kills and deaths based on the view
```sql
SELECT
platformgameid,
side,
teamid,
AVG(kills)
    OVER(ORDER BY eventtime ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
    AS avg_kills,
AVG(deaths)
    OVER(ORDER BY eventtime ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
    AS avg_deaths,
AVG(win)
    OVER(ORDER BY eventtime ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
    AS avg_win
FROM lol.games_ks;
```