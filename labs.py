import datetime

def invert_schedule(s):
    x = 0
    i = []
    start = to_date(s[0]['start']).replace(hour=8, minute=0)
    for period in s:
        time_with_buffer = to_date(period['start']) - datetime.timedelta(minutes=5)
        if time_with_buffer > start:
            i.append({
                'start': str(start),
                'end': str(time_with_buffer),
                'name': 'free'
                })
        start = to_date(period['end']) + datetime.timedelta(minutes=5)
    return i

def intersect_schedules(s1, s2):
    x = 0
    y = 0
    s = []
    s1 = invert_schedule(s1)
    s2 = invert_schedule(s2)
    while x < len(s1) and y < len(s2):
        start1 = to_date(s1[x]['start'])
        start2 = to_date(s2[y]['start'])
        end1 = to_date(s1[x]['end'])
        end2 = to_date(s2[y]['end'])
        if start1 < end2 and start2 < end1:
            s.append({
                'start': str(max(start1, start2)),
                'end': str(min(end1, end2))
                })
            if end1 < end2:
                x += 1
            else:
                y += 1
        elif end1 < start2:
            x += 1
        elif end2 < start1:
            y += 1
    return s

def to_date(s):
    return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    import test_schedules
    print intersect_schedules(test_schedules.c17dh, test_schedules.HYAM)