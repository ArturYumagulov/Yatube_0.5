import datetime as dt


def year(request):
    clean_year = dt.datetime.now().year
    return {'year': clean_year}