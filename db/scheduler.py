import datetime
import os
import subprocess

from config import config
from croniter import croniter


class Scheduler:
    def __init__(self):
        self.config = config
        self.cron_config = {}

    def human_to_cron(self, human_readable):
        parts = human_readable.split()
        if parts[0] == 'daily':
            if 'am' in parts[1]:
                hour = parts[1].strip('am')
            if 'pm' in parts[1]:
                hour = int(parts[1].strip('pm')) + 12

            cron_expr = f"0 {hour} * * *"
        elif parts[0] == 'weekly':
            days = {'Monday': '1', 'Tuesday': '2', 'Wednesday': '3', 'Thursday': '4', 'Friday': '5',
                    'Saturday': '6', 'Sunday': '7'}
            day_of_week = days.get(parts[1])

            if parts[1] not in days.keys():
                raise ValueError(f"{parts[1]} is not a valid day of the week")  # todo log not raise

            cron_expr = f"0 9 * * {day_of_week}"
        else:
            raise ValueError("Invalid human-readable time format")

        try:
            croniter(cron_expr)
        except Exception as e:
            raise  # todo log not raise

        return cron_expr

    def schedule_jobs(self):
        cron_jobs = []
        for table_name, table_config in self.config.items():
            human_readable = table_config['load_time']
            cron_expression = self.human_to_cron(human_readable)

            # todo fix yesterday - gotta be for a run
            # todo timezone?
            yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

            # Construct command
            f_loader = 'loader.py'
            cwd = os.path.dirname(os.path.realpath(__file__))
            loader_path = os.path.join(cwd, f_loader)
            command = f'python3 {loader_path} --table-name="{table_name}" --date="{yesterday}"'

            # create cron job
            cron_job = f'{cron_expression} {command}'
            cron_jobs.append(cron_job)

        cron_jobs = '\n'.join(cron_jobs) + '\n'

        try:
            crontab_user = 'wx' # todo move to separate config
            subprocess.run(['crontab', '-u', crontab_user, '-'], input=cron_jobs, text=True, check=True)
            print("Cron jobs rewritten.")
        except subprocess.CalledProcessError as e:
            print("Failed to update crontab:", str(e))

        return


if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.schedule_jobs()
