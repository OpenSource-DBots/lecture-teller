from datetime import datetime


"""
Summary:
    Log some message to the log file
"""
def log(message: str):
    with open(f'logs/{log_file_name()}.txt', 'a') as f:
        f.write(f'[{get_current_time()}] {message}\n')


"""
Summary:
    Write the log file name as 'logs_year-month-day'
Returns:
    Log file name
"""
def log_file_name():
    current_time = datetime.now()
    return current_time.strftime('logs_%m-%d-%Y')


"""
Summary:
    Get the current time and format it to H:M:S
Returns:
    The time formatted in H:M:S
"""
def get_current_time():
    current_time = datetime.now()
    return current_time.strftime('%H:%M:%S')
