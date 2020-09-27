#  MIT Research and Consultancy web portal
MIT Art Design and Technology University (MIT ADT University) is a place
where creativity and innovation coexist. The PhD course in MIT ADT University
is one amongst the enhanced courses in MIT. The Work Flow in this course is
totally based on paper work and is time consuming. The Aim of this project
is to bring Digital Transformation in this PhD Course and seize redundant free
management, digital process control and optimization, collecting and distributing
knowledge and information, and optimal coordination with existing systems for
efficient process management. This project will provide all the users a broad array
of information on a specific domain, arranged in a way that is most convenient
to access. It will increase communication and knowledge sharing. It will create
a generalized portal for all domains. The project aims to provide a rich space to
share and search information.

## Problem Statement

To develop a System that will provide an interactive platform for the Research
Scholars, research Supervisors, Research Co-Supervisors and reduce a lot of time,
efforts and paperwork, and also provide a forum for doubt solving. More specif-
ically, to allow a user to manage and communicate with other users and pub-
lish/assess articles. To facilitate submissions by making them online and avoiding
the manual paperwork submission. The system also contains a relational database
containing a list of Research Scholars, Research Supervisors and Research Co-
Supervisors, and Articles/Publishing’s.

## Objectives

* To create a user-friendly platform for Research Scholars, Research Supervisors, research Co-Supervisors
* To increase the speed and efficiency.
* To reduce paperwork and store/manage data/records efficiently.
* To make communication and progress tracking easier.

## Features

* Registration and Login with live validation and security
* An interactive forum for the researchers to communicate
* Submissions and Approvals of any resource.
* E-Library to access books, papers, videos, audios, links
* PhD Progress Status to keep a record of milestones completed
* User profile to display personal and professional details
* Admin Panel to approve, block, unblock, view users

## Technology
### Front End
* HTML5
* CSS3
* Bootstrap 4
* JavaScript
* JQuery
* Ajax
### Back End
* Python 3
* Flask
### Database
* Django

## Pages Included

### Portal
1. Research Scholar Registration
2. Login (Research Scholar, Research Supervisor/Co-Supervisor)
3. Home Page
4. Forum
5. View/Contact Batch Researchers
6. E-Library
7. Progress Page
8. Supervisor's Panel : Upload/Evaluate Assignments
9. Supervisor's Panel : Verify E-Resources
10. Profile Page : User Info
11. Profile Page : Submissions
12. Profile Page : Upload E-Resources
13. Profile Page : Research Supervisor-Scholar Collaboration
14. Change Password
15. Developers Page

### Admin Panel
1. Reset Admin
2. Admin Login
3. Admin Dashboard
4. Change Password
5. Set Batch
6. Expire Batch
7. Approve Registrations
8. Promote Research Scholars
9. Registration : Research Supervisors/Co-Supervisors, Special Users
10. Edit Researcher
11. Block Researcher
12. Remove Researcher
13. View Research Scholars
14. View Research Supervisors
15. View Research Co-Supervisors
16. View Special Users

## Instructions to run the app

### 1. Create a cluster on [Mongodb Cloud Atlas](https://www.mongodb.com/cloud/atlas)
### 2. Create a file .env in the following format
```
SESSION_TYPE=memcached
SECRET_KEY=<your_secret_key>
MONGO_URI =<your_mongodb cluster URI>
FLASK_ENV=development
UPLOAD_FOLDER=static/uploads
```
### 3. Install the Requirements
```
pip3 install -r requirements.txt
```
### 4. Run the Flask app
```
flask run
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Contributors
### 1. Safir Motiwala
### 2. Ram Suthar
### 3. Vinayak Sutar

## FootNotes

### Project Demo - https://drive.google.com/file/d/10vq2X4zs3OVkN9_1H3gIi6g9ekzglHRm/view?usp=sharing
