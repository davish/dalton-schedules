# dalton-schedules
API wrapper for retrieving student and teacher schedules at the Dalton School.

For many of the tests in `schedules.py`, a user and password from the Dalton system is necessary. Create a `credentials.py` file and declare two variables, `username` and `password`, whose values are your username and password. This is in the gitignore, and should not leave one's computer.

Install dependencies with `pip install -r requirements.txt`

Currently implemented API endpoints:
- `/schedule`  | `POST` | body: `username`, `password`
    - Get this week's schedule for the user whose credentials are passed in. Returns data in a JSON array of "event" objects of this general format:
    ```
{
    "date": "2015-11-24",
    "start": "2015-11-24 13:40:00", 
    "end": "2015-11-24 14:25:00", 
    "location": "612", 
    "course": {
        "course_name": "Math Class", 
        "instructor": {
          "id": "XXXX", 
          "name": "Mr. Schneebly"
        }, 
    "section_id": "1010-01"
    }
}
    ```