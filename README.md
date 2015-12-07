# dalton-schedules
API wrapper for retrieving student and teacher schedules at the Dalton School.

For many of the tests in `schedules.py`, a user and password from the Dalton system is necessary. Create a `credentials.py` file and declare two variables, `username` and `password`, whose values are your username and password. This is in the gitignore, and should not leave one's computer.

Install dependencies with `pip install -r requirements.txt`

## API

All `POST` method API endpoints require a JSON object as the request body. This object should contain `username` and `password` fields. 

- `POST` `/info/<id>`
  - Get information about a user. Returns their grade, full name, and whether they're a student or a teacher.

- `POST` `/schedule/my`
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
- `POST` `/faculty`
    - Returns an array of all faculty members. Example element:
    ```
    {
      "firstname": "Jim", 
      "fullname": "Jim Zulakis", 
      "id": "ZULJ", 
      "lastname": "Zulakis"
    }
    ```
- `POST` `/schedule/faculty/<_id>`
    - Retrieve the week's schedule for the faculty member whose ID is in the URL. Same format as a student's ID.

- `POST` `/schedule/compare/<person1>/<person2>`
    - Returns the free times that these two people share this week.
    - The two parameters are faculty IDs. If either of the parameters is `me` instead of an ID, then the current student's ID will be used.
