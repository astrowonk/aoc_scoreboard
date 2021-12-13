
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
