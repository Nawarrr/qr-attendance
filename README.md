#  ![Badge](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) QR Attendance

QR Attendance is a web app that helps you take the attendance with just a quick qr scan from the students

# THIS IS NO LONGER WORKING as Heroku removed free plans, will be fixed ASAP

## How to use it ? 
1. Visit https://qr-attendance-deployed.herokuapp.com/
2. Enter your name (Instuctor) and the course name and click create session
3. Student can use the QR code (you can also send them the link shown) to open a page
4. Student should enter their name and ID and submit
5. Click Submit when all the students are done
6. Click Download to Download the csv file with attendance

## User Stories
- Instructor can enter his name and the session name
- Student can scan a QR code to show their attendance
- Instructor can download the attendance or leave it in the DB


## Features
- Functional Creation of Session
- Fucntional Attendance for students


## Future Features
- Authentication for students to assure integrity in the Attendance Taking
- Better styled website
- Starting a course and keep track for every session in that course 


## Technologies Used
- FastAPI
- SQLite
