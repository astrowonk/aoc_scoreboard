
## Advent of Code Scoreboard

This class will parse a JSON file from the API listed on an [Advent of Code](https://adventofcode.com) private scoreboard into pandas dataframes. Very much a work in progress, I hope to make setup.py file soon, and then maybe on to pypi.

Usage:

```
from AOCScoreboard import AOCScoreboard
scores = AOCScoreboard('myfile.json')

## one row per name, time, day, star, points, and running total points
scores.df

## axis name, columns points by day
scores.make_daily_leaderboard()

```


### Screenshots from Jupyter
![image](https://user-images.githubusercontent.com/13702392/145860760-25edf63f-47cd-452e-830e-0ddad1d2528f.png)

![Screen Shot 2021-12-13 at 12 35 57 PM](https://user-images.githubusercontent.com/13702392/145860893-08c0833a-75cd-49a2-9eca-9d3b0490d9e3.png)
