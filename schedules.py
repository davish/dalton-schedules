import requests
import datetime

from bs4 import BeautifulSoup

from utils import *

roux_url = 'https://schedules.dalton.org/roux/index.php'

SCHOOL_YEAR = '2016'

def send_request(req):
    r = requests.post(roux_url, data={'rouxRequest': req})
    soup = BeautifulSoup(r.text, 'xml')
    return soup, int(soup.result.get('status'))

def build_schedule(res):
    """
    Take in a schedule in XML and spit it out as a Python object.
    """
    schedule = []
    soup = res
    for period in soup.find_all('period'):
        d = datetime.datetime.strptime(period.date.text, '%m-%d-%Y').date()
        p = {
            'date': str(d),
            'start': str(
                datetime.datetime.strptime(period.start.text, '%Y-%m-%d %H:%M:%S'
                    ).replace(year=d.year,month=d.month,day=d.day)),
            'end': str(
                datetime.datetime.strptime(period.end.text, '%Y-%m-%d %H:%M:%S'
                    ).replace(year=d.year,month=d.month,day=d.day)),
            'location': period.location.text,
            'course': {
                'id': period.section.get('id'),
                'title': period.section.find('name').text,
                'instructor': {
                    'id': period.instructor.get('id'),
                    'name': period.instructor.find('name').text
                }
            }  
        }
        schedule.append(p)

    return schedule

def select_faculty_calendar(faculty_id, key, m=None):
    """
    Given a faculty ID and a valid session key, 
    get a faculty member's schedule for the current week.
    """
    if m is None:
        m = get_monday(datetime.datetime.now().date())
    req = """
    <request>
    <key>%s</key>
    <action>selectFacultyCalendar</action>
    <ID>%s</ID>
    <academicyear>%s</academicyear>
    <start>%s</start>
    <end>%s</end>
    </request>
    """ % (key, 
        faculty_id, 
        SCHOOL_YEAR,
        date_string(m), 
        date_string(m + datetime.timedelta(days=4)))
    soup, status = send_request(req)
    if status == 200:
        return build_schedule(soup.result)

def get_teacher_list(key):
    """
    Get a list of all teachers, given a session key.
    """
    soup, status = send_request(
        """
        <request>
        <key>%s</key>
        <action>selectFacultyProfiles</action>
        </request>
        """ % (key))
    
    if status == 200:
        f = []
        for faculty in soup.result.find_all('faculty'):
            f.append({
                'id': faculty.get('id'),
                'fullname': faculty.find('name').text,
                'firstname': faculty.find('firstname').text,
                'lastname': faculty.find('lastname').text
                })
        return f
    else:
        return None


def select_student_calendar(key, _id, m=None):
    """
    Given a session key and a student ID, get a student's schedule and return
    the relevant XML in string form.
    """
    if m is None:
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
        """ % (key, 
               _id, 
               SCHOOL_YEAR, 
               date_string(m), 
               date_string(m + datetime.timedelta(days=4)))
    soup, status = send_request(sched_req)
    if status == 200:
        return build_schedule(soup.result)

def select_student_schedule(key, _id):
    soup, status = send_request(
        """
        <request>
        <key>%s</key>
        <action>selectStudentSchedule</action>
        <ID>%s</ID>
        <academicyear>%s</academicyear>
        </request>
        """ % (key, _id, SCHOOL_YEAR))
    if status == 200:
        return soup

def select_user(key, _id):
    soup, status = send_request(
        """
        <request>
        <key>%s</key>
        <action>selectUser</action>
        <ID>%s</ID>
        </request>
        """ % (key, _id))
    if status == 200:
        u = soup.result.user
        return {'fullname': u.find('name').text,
                'grade': u.grade.text,
                'type': u.get('type'),
                }


def get_key(username, pswd):
    """
    Get a schedules access key given a username and password.
    """
    soup, status = send_request(
        """
        <request>
        <key></key>
        <action>authenticate</action>
        <credentials>
        <username>%s</username><password type="plaintext">%s</password>
        </credentials>
        </request>""" % (username, pswd))
    if status == 200:
        return soup.result.key.text, soup.result.key.get('owner')
    else:
        return None, None

if __name__ == '__main__':
    import credentials
    key, _id = get_key(credentials.username, credentials.password)
    print select_student_calendar(key, _id)[0]
    