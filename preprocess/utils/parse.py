from datetime import datetime


# Get data from filenames
def get_filename_data(filename):
    # format: Vision_Field_Application_Engineer_2023-11-01_12-39-43.tmp
    tokens = filename.rstrip('.tmp').split('_')

    # date and time are in the last two tokens
    date_str = tokens[-2]
    time_str = tokens[-1]

    # if the token -3 is not "developer" or "engineer", then it is the company name
    # todo low prio backlog - remove hardcode for dev / engineer
    # print(f"{tokens[-3].lower()} <--- this token decides if company name is present")
    if tokens[-3].lower() not in ['developer', 'engineer']:     # hacky
        company = tokens[-3]
        job_title = '_'.join(tokens[:-3])
    else:
        company = ''
        job_title = '_'.join(tokens[:-2])

    # datetime_str = f"{date_str} {time_str}"
    # date_obj = datetime.strptime(datetime_str, "%Y%m%d %H%M")
    # date_str = date_obj.strftime("%Y-%m-%d")
    # time_str = date_obj.strftime("%H:%M")

    return job_title, company, date_str, time_str


# if __name__ == '__main__':
#     partial_filename = 'Vision_Field_Application_Engineer_2023-11-01_12-39-43.tmp'
#     full_filename = 'DevOps_Engineer_GCP_2023-10-30_13-58-44.tmp'
#
#     get_filename_data(partial_filename)
#     get_filename_data(full_filename)
