import datetime

def get_today_date():
    today = datetime.datetime.today().strftime('%Y%m%d')
    return today


if __name__ == '__main__':
    print(get_today_date())