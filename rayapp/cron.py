from django_cron import CronJobBase, Schedule


class DownloadNewsFromApiCron(CronJobBase):
    RUN_EVERY_MINS = 60

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'rayapp.download_news_from_api_job'

    def do(self):
        from news.management.commands.run_news_parsing_service_command import Command
        command = Command()
        command.handle()


class BackupDatabaseCronJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    # RUN_AT_TIMES = ['03:00']
    # schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'rayapp.backup_database_cron_job'

    def do(self):
        from news.management.commands.backup_db_command import Command
        cmd = Command()
        cmd.handle()
