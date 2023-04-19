Blog Lite 
Done by Akilesh KR
21f3001618@student.onlinedegree.iitm.ac.in

Server : http://127.0.0.1:5000/


In this project I  built a full stack web application called bloglite which helps users to
view blogs of people whom they follow.Also they can also create,edit and delete their
own blogs.They can search people to follow and unfollow them when necessary.

Main Technologies Used:
1..Flask - backend(used for developing our web application which is a python framework)
2.sqlite3 - backend database
3.Html , css , bootstrap - frontend designing
4.Python - language used in flask


2 main folders

├── static
│   │   │
│   │   │─ pro_pic
│   │   │─ styles.css




├── templates
│   │   │
│   │   │─ addblog.html
│   │   │─ comments.html
│   │   │─ deleteblog.html
│   │   │─ deleteconfirm.html
│   │   |─ editblog.html
        │─ editfull.html
│   │   │─ homepage.html
│   │   │─ login.html
│   │   │─ profile.html
│       |─ readblog.html
│   │   │─ signup.html




Database

I have used 4 tables in the database namely - User table , Posttable table , Comment Table
and Follow table.
In the User table the primary key is userid , this table contains the information about the
user’s username, password , email , Age , profile picture and no_of posts the particular
User has posted.This table has one to many relationship with Posttable table , Comment
Table and Follow table as each user can add multiple posts , comments and can have
followers
Next we have the Posttable table having post_id as primary key which contains the
information about the posts,here we have the username as the foreign key from the User
table.This table contains info of blog title , blog description , blog image , it’s time stamp , no
of likes and dislikes of the blog , comments it got.
Next we have the Comments table having 2 foreign keys of Posttable and User tables
Post_id and username columns.This table basically stores all the comments put forward
to each of the post by different individuals.Also it has timestamp of when a particular
user comments.
Finally we have the Follow table which has 2 foreign keys from Posttable and User tables.
This is used to store who follows who with timestamps

├── models
│   │   │
│   │   │─ User 
│   │   │─ Posttable
│   │   │─ Follow
│   │   │─ Comment


2 main python files 
    1. appl.py(run on port 5000)
    2. resources.py(run on port 3000)




My project mainly contains of static folder in which all the css and the profile images of users
gets saved in , Templates folder which comprises of all the html files and instance folder
contains database of my project.Then there are 2 main python files ,
1.appl.py and 2.resources.py
appl.py consists of all my controllers , models and app files into one file
resources.py consists of my api which i created for the CRUD operations on users.
To run normally in the terminal we can just type in python appl.py
If we want to add users through api operations run python resources.py
There is a simple login page implemented and the home page of my application is the
users feed where the user can see blogs of people which are followed by the user
There is a profile page tracking down your no of posts , followers and following
From here a user can add , edit and delete his blogs.
There is a search bar where the user can search other people in order to follow them

