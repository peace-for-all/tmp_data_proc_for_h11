## Data loader (with scheduler)

This module works like this:
Scheduler creates cron jobs and executes loader.py for each table.

### How to use
1. Write config.py defining conditions of data load (source, destination, data format, schedule)
2. Run scheduler.py; it creates crontab for a specified user with all tables from config
3. Scheduler.py runs loader.py for each table with params from config
4. TODO: Logging isn't yet implemented (so no way to monitor, scripts just raise exc for now)

### Notes
- crontab validity is checked in scheduler; script exits if time cond is wrong
- for now SQL expressions (DDL and inserts) are done with `df.to_sql()` (I don't like it, todo change later)

