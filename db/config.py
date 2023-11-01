config = {
    'skills_daily': {
        'source_data_dir': 'source_data',
        'file_format': 'csv',
        'load_time': 'daily 9am'
    },
    'skills_weekly': {
        'source_data_dir': 'source_data',
        'file_format': 'csv',
        'load_time': 'weekly Monday'  # todo implement in loader.py! it's a bug now, will load yday only
    }
}
