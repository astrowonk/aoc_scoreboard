import pandas as pd
import re
import json
import datetime


def make_new_file_name(file_name, suffix='csv'):
    """Make a new file name based on the old file name using the suffix"""
    suffix = '.' + suffix
    if file_name.endswith('json'):
        return file_name.replace('.json', suffix)
    return file_name + suffix


class AOCScoreboard():

    json_file_name = None

    def __init__(self, json_file) -> None:
        self.process_json_file(json_file)

    def get_df(self):
        return self.df

    @staticmethod
    def compute_points_star(x, n):
        x = [y for y in x if y[0] is not None]
        x.sort(key=lambda x: x[0])
        sorted_name = [x[1] for x in x]
        #return point dictionary
        return {key: val for key, val in zip(x, range(n, 0, -1))}

    def compute_points_day(self, x, leaderboard_size, day):
        star1 = self.compute_points_star(x['star1'], leaderboard_size)
        star2 = self.compute_points_star(x['star2'], leaderboard_size)
        return [{
            'day': day,
            'star': 1,
            'points': val,
            'name': key[1],
            'time': datetime.datetime.fromtimestamp(key[0])
        } for key, val in star1.items()
                ] + [{
                    'day': day,
                    'star': 2,
                    'points': val,
                    'name': key[1],
                    'time': datetime.datetime.fromtimestamp(key[0])
                } for key, val in star2.items()]

    def make_df(self):
        final_res = []
        for day, res in self.completion_day_dict.items():
            out = self.compute_points_day(res, self.leaderboard_size, day)
            final_res.extend(out)
        self.df = pd.DataFrame(final_res)
        self.df.sort_values(['day', 'star'], inplace=True)
        self.df['running_total_points'] = self.df.groupby(
            ['name'])['points'].cumsum()
        return

    def make_daily_leaderboard(self, show_possibles=True):
        """make a dataframe with point totals by day"""
        df = self.df.pivot_table(
            index='name',
            columns=['day'],
            values='points',
            aggfunc=sum,
        )
        df = df[sorted(df.columns, key=lambda x: int(x))]

        df['total'] = df.T.sum()
        df.sort_values('total', ascending=False, inplace=True)
        #hypotheticals
        df.drop(
            columns=['total', 'Worst Possible Total', 'Best Possible Total'],
            inplace=True,
            errors='ignore')
        df['Best Possible Total'] = df.fillna((df.min() - 2).to_dict()).T.sum()
        df['Worst Possible Total'] = df.drop(
            columns=['Best Possible Total']).fillna(2).T.sum()
        df['total'] = df.T.drop(
            ['Worst Possible Total', 'Best Possible Total']).sum()
        if show_possibles:
            return df
        else:
            return df.drop(
                columns=['Worst Possible Total', 'Best Possible Total'],
                errors='ignore')

    def create_completion_day_dict(self):
        completion_day_dict = {}
        for member_name, member_dict in self.json_data['members'].items():
            for day, val in member_dict['completion_day_level'].items():
                completion_day_dict.setdefault(day, {}).setdefault(
                    'star1', []).append(
                        (val.get('1',
                                 {}).get('get_star_ts'), member_dict['name']
                         or member_name))
                completion_day_dict.setdefault(day, {}).setdefault(
                    'star2', []).append(
                        (val.get('2',
                                 {}).get('get_star_ts'), member_dict['name']
                         or member_name))
        self.completion_day_dict = completion_day_dict
        self.leaderboard_size = len(self.json_data['members'])

    def plot_line(self):
        return self.df.plot.line(x='time',
                                 y='running_total_points',
                                 color='name')

    def process_json_file(self, json_file):
        self.json_file_name = json_file
        with open(json_file) as f:
            self.json_data = json.load(f)
        self.create_completion_day_dict()
        self.make_df()

    def export_csv(self):
        """export the base level dataframe to a csv file"""
        self.df.to_csv(make_new_file_name(self.json_file_name, 'csv'))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('json_file', type=str)
    args = parser.parse_args()

    AOCScoreboard(args.json_file).export_csv()
