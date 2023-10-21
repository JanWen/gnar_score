Team that will get controll over the first four waves has strong advantage.

Check lvl and cs lead for team per game and compare to wr

end time at around 3:30
5 min = 300000
1 min = 60000
210000 gametime


Get the Level and cs for each team and join with the win for that team
```sql
select 
    eventtime,
    g.platformgameid,
    gametime,
    w.winningteam,
    participants[1].level +  participants[2].level + participants[3].level + participants[4].level + participants[5].level as blue_level,
    participants[6].level +  participants[7].level + participants[8].level + participants[9].level + participants[10].level  as red_level,
    participants[1].stats[1].value +  participants[2].stats[1].value + participants[3].stats[1].value + participants[4].stats[1].value + participants[5].stats[1].value as blue_cs,
    participants[6].stats[1].value +  participants[7].stats[1].value + participants[8].stats[1].value + participants[9].stats[1].value + participants[10].stats[1].value  as red_cs
from lol.games as g, lol.wins as w
where
    g.platformgameid = w.platformgameid
    and eventtype = 'stats_update'
    and gametime >= 210000 and gametime <= 211000
    and CARDINALITY(participants) = 10
```


```sql
select 
    eventtime,
    g.platformgameid,
    gametime,
    w.winningteam,
    participants[1].level as level_1,
    participants[1].stats[1].value as cs_1,
    participants[2].level as level_2,
    participants[2].stats[1].value as cs_2,
    participants[3].level as level_3,
    participants[3].stats[1].value as cs_3,
    participants[4].level as level_4,
    participants[4].stats[1].value as cs_4,
    participants[5].level as level_5,
    participants[5].stats[1].value as cs_5,
    participants[6].level as level_6,
    participants[6].stats[1].value as cs_6,
    participants[7].level as level_7,
    participants[7].stats[1].value as cs_7,
    participants[8].level as level_8,
    participants[8].stats[1].value as cs_8,
    participants[9].level as level_9,
    participants[9].stats[1].value as cs_9,
    participants[10].level as level_10,
    participants[10].stats[1].value as cs_10
from lol.games as g, lol.wins as w
where
    g.platformgameid = w.platformgameid
    and eventtype = 'stats_update'
    and gametime >= 210000 and gametime <= 211000
    and CARDINALITY(participants) = 10
```