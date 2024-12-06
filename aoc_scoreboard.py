import pandas as pd
import re
import json
import datetime
import random

__VERSION__ = '0.1.1'


def make_new_file_name(file_name, suffix='csv'):
    """Make a new file name based on the old file name using the suffix"""
    suffix = '.' + suffix
    if file_name.endswith('json'):
        return file_name.replace('.json', suffix)
    return file_name + suffix


class AOCScoreboard:
    json_file_name = None

    def __init__(self, json_file=None, json_dict=None, randomize_user_names=False) -> None:
        """Either process a json file or a load a dict already created"""
        self.randomize_user_names = randomize_user_names

        if json_file:
            self.process_json_file(json_file)
        else:
            self.json_data = json_dict
            self.create_completion_day_dict()
            self.make_df()

    @staticmethod
    def compute_points_star(x, n):
        x = [y for y in x if y[0] is not None]
        x.sort(key=lambda x: x[0])
        sorted_name = [x[1] for x in x]
        # return point dictionary
        return {key: val for key, val in zip(x, range(n, 0, -1))}

    def compute_points_day(self, x, leaderboard_size, day):
        star1 = self.compute_points_star(x['star1'], leaderboard_size)
        star2 = self.compute_points_star(x['star2'], leaderboard_size)
        return [
            {
                'Day': day,
                'Star': 1,
                'Points': val,
                'Name': key[1],
                'Date': datetime.datetime.fromtimestamp(key[0]),
            }
            for key, val in star1.items()
        ] + [
            {
                'Day': day,
                'Star': 2,
                'Points': val,
                'Name': key[1],
                'Date': datetime.datetime.fromtimestamp(key[0]),
            }
            for key, val in star2.items()
        ]

    def make_df(self):
        final_res = []
        for day, res in self.completion_day_dict.items():
            out = self.compute_points_day(res, self.leaderboard_size, day)
            final_res.extend(out)
        self.df = pd.DataFrame(final_res)
        self.df['Day'] = self.df['Day'].astype(int)
        self.df = self.df.sort_values(
            ['Date', 'Day', 'Star'],
        ).reset_index(drop=True)
        self.df['Total Points'] = self.df.groupby(['Name'])['Points'].cumsum()
        if self.randomize_user_names:
            unique_names = self.df['Name'].unique()
            random_index = list(range(0, len(unique_names)))
            random.shuffle(random_index)
            name_map = {name: f'User {random_index[i]}' for i, name in enumerate(unique_names)}
            self.df['Name'] = self.df['Name'].map(name_map)
        return

    def make_daily_leaderboard(self, show_possibles=True):
        """make a dataframe with point totals by day"""
        df = self.df.pivot_table(
            index='Name',
            columns=['Day'],
            values='Points',
            aggfunc=sum,
        )
        df = df[sorted(df.columns, key=lambda x: int(x))]

        df['Total'] = df.T.sum()
        df.sort_values('Total', ascending=False, inplace=True)
        # hypotheticals
        df.drop(
            columns=['Total', 'Lowest Possible Total', 'Highest Possible Total'],
            inplace=True,
            errors='ignore',
        )

        # there must be a better way...
        best_possible_one_star = df.copy()
        worst_possible_one_star = df.copy()

        # count stars check for only 1 star
        df2 = self.df.pivot_table(
            index='Name',
            columns=['Day'],
            values='Star',
            aggfunc='count',
        )

        # double any one star rows

        best_possible_one_star[df2 == 1] = best_possible_one_star[df2 == 1].add(
            (best_possible_one_star[df2 == 1].min(axis=0))
        )

        # but could get the second star last
        worst_possible_one_star[df2 == 1] = worst_possible_one_star[df2 == 1] + 2
        highest = best_possible_one_star.fillna((best_possible_one_star.min() - 2)).T.sum()
        lowest = worst_possible_one_star.fillna(2).T.sum()

        df['Total'] = df.T.sum()
        df['Highest Possible Total'] = highest
        df['Lowest Possible Total'] = lowest
        if show_possibles:
            return df
        else:
            return df.drop(
                columns=['Lowest Possible Total', 'Highest Possible Total'], errors='ignore'
            )

    def create_completion_day_dict(self):
        completion_day_dict = {}
        for member_name, member_dict in self.json_data['members'].items():
            for day, val in member_dict['completion_day_level'].items():
                completion_day_dict.setdefault(day, {}).setdefault('star1', []).append(
                    (val.get('1', {}).get('get_star_ts'), member_dict['name'] or member_name)
                )
                completion_day_dict.setdefault(day, {}).setdefault('star2', []).append(
                    (val.get('2', {}).get('get_star_ts'), member_dict['name'] or member_name)
                )
        self.completion_day_dict = completion_day_dict
        self.leaderboard_size = len(self.json_data['members'])

    def line_graph(self):
        try:
            return self.df.plot.line(
                x='Date', y='Total Points', color='Name', backend='plotly'
            )
        except ValueError:
            print('Line plot requires plotly backend')

    def process_json_file(self, json_file):
        self.json_file_name = json_file
        with open(json_file) as f:
            self.json_data = json.load(f)
        self.create_completion_day_dict()
        self.make_df()

    def export_csv(self):
        """export the base level dataframe to a csv file"""
        self.df.to_csv(make_new_file_name(self.json_file_name, 'csv'))

    def minutes_between_stars(self):
        res = (
            self.df.groupby(['Day', 'Name'])['Date']
            .agg(['max', 'min'])
            .assign(minutes_between_stars=lambda x: (x['max'] - x['min']))
        )
        res['minutes_between_stars'] = res['minutes_between_stars'].apply(
            lambda x: x.total_seconds() / 60
        )

        return res.reset_index().pivot_table(
            index='Name', columns='Day', values='minutes_between_stars', aggfunc='max'
        )


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('json_file', type=str)
    args = parser.parse_args()

    AOCScoreboard(args.json_file).export_csv()
