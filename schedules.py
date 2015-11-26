import requests
import datetime

from bs4 import BeautifulSoup

from utils import *
import credentials

roux_url = 'https://schedules.dalton.org/roux/index.php'

def build_schedule(res):
    """
    Take in a schedule in XML and spit it out as a Python object.
    """
    schedule = []
    soup = BeautifulSoup(res, 'xml')
    for period in soup.find_all('period'):
        d = datetime.datetime.strptime(period.date.text, '%m-%d-%Y').date()
        p = {
            'date': d,
            'start': datetime.datetime.strptime(period.start.text, '%Y-%m-%d %H:%M:%S').replace(year=d.year,month=d.month,day=d.day),
            'end': datetime.datetime.strptime(period.end.text, '%Y-%m-%d %H:%M:%S').replace(year=d.year,month=d.month,day=d.day),
            'location': period.location.text,
            'section_id': period.section.get('id'),
            'course_name': period.section.find('name').text
        }
        schedule.append(p)

    return schedule


def get_student_schedule(username, pswd):
    """
    Given a username and password, get a student's schedule and return
    the relevant XML in string form.
    """
    info = get_key(username, pswd)
    key = info[0]
    id_ = info[1]
    m = get_monday(datetime.datetime.now().date())
    sched_req = """
    <request>
    <key>%s</key>
    <action>selectStudentCalendar</action>
    <ID>%s</ID>
    <academicyear>%s</academicyear>
    <start>%s</start>
    <end>%s</end>
    </request>
    """ % (key, id_, '2016', date_string(m), date_string(m + datetime.timedelta(days=4)))
    r = requests.post(roux_url, data={'rouxRequest': sched_req})
    soup = BeautifulSoup(r.text, 'xml')
    return str(soup.result)


def get_key(username, pswd):
    """
    Get a schedules access key given a username and password.
    """
    token_req = """
    <request>
    <key></key>
    <action>authenticate</action>
    <credentials>
    <username>%s</username><password type="plaintext">%s</password>
    </credentials>
    </request>
    """ % (username, pswd)
    r = requests.post(roux_url, data={'rouxRequest': token_req})
    soup = BeautifulSoup(r.text, 'xml')
    return soup.result.key.text, soup.result.key.get('owner')

def spoof_schedule():
    """
    Return string in the same format as get_student_schedule, 
    but from a file instead of from the schedules API.
    """
    with open('res.xml', 'r') as f:
        return str(BeautifulSoup(f.read(), 'xml').result)

def build_spoof():
    with open('res.xml', 'w') as f:
        f.write(get_student_schedule(credentials.username, credentials.password))

if __name__ == '__main__':
    sched = build_schedule(spoof_schedule())
    print sched[0]
    