import datetime
def get_monday(d):
    return datetime.date(d.year, d.month, d.day - (d.isoweekday()-1))

def date_string(d):
    return "%s%02d%02d" % (d.year, d.month, d.day)