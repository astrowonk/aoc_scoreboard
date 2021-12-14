
## Advent of Code Scoreboard

This class will parse a JSON file from the API listed on an [Advent of Code](https://adventofcode.com) private scoreboard into pandas dataframes.

This module powers the [AOC Dashboard](https://github.com/astrowonk/aoc_dashboard) which is a [Plotly Dash](https://dash.plotly.com) web app that renders charts and tables based on user-uploaded .json file from the AoC site. [The web app is running live on my web site](https://marcoshuerta.com/dash/aoc/), if you want to check it out.

Usage:

```
from AOCScoreboard import AOCScoreboard
scores = AOCScoreboard('myfile.json')

## one row per name, time, day, star, points, and running total points
scores.df

## axis name, columns points by day
scores.make_daily_leaderboard()

## Minutes between stars by day for each user
scores.minutes_between_stars()

```


### Screenshots from Jupyter


![Screen Shot 2021-12-13 at 12 35 57 PM](https://user-images.githubusercontent.com/13702392/145860893-08c0833a-75cd-49a2-9eca-9d3b0490d9e3.png)
