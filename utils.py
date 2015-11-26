import datetime
def get_monday(d):
    return datetime.date(d.year, d.month, d.day - (d.isoweekday()-1))

def date_string(d):
    return "%s%s%s" % (d.year, d.month, d.day)