# Facebook_clone_project--Django
- (Please see sample videos below)
- Creater : Yeonghwan Park (John Park)
- Main Tools : Python(Django)
- Sub Tools : Html, CSS(Bootstrap), JS(Jquery), Python(Beautifulsoup)
- Explantion : <br>
This is Facebook clone page that I built by refering to orginal Facebook site.
- Hard Part and Solution : <br>
1. while implementing likes-function, I used to fix "model" file many time, as many "MVC" developer know, model file is very sensitive since it's about Database,
one day in the middle of deleting and migrating datas back and force, "migrate" was not working at all in error "no such table", so it makes me wasting a lot of time, thankfuly I've got the solution which is "py manage.py migrate --run-syncdb" that makes Datebase table once again, I don't know if it is difficult error to django developer or not, but back then I found it hard as I made it as 1st self-project without any help from others
2. basically Django and Jquery are not for SPA, so it was really hard to conceive all the logics to implement "likes number" that is changed in real time without moving on different page, so I did legwork going thru all the trials and errors repetively comparing likes-numbers that is input in real time and that is saved in database.
3. while implementing auth part and saving user-info in Database, I continually failed to log in since encrypted-password and input-password were not matched,
but I found that if I use formdata-method when password datas is sent from client to server with encryption, that password is manipulated to totaly diferent one that doesn't recognize encryption. so I used it to Json-method plus insted of using ajax, I used just form tag to send to server so I came to solve the error.
it took me almost entire 2 days to find solution,
- Things To Fix : need to get this clean code, better English-comment's grammer, replace success, error, complete in ajax about "console log"

<br>
- Word I want to leave about this project : <br>
since It is first time project that I made, There would be some lack, but my work is getting improved after this project.
I have found my lack in this project after all, but I didn't fix any code since I want to see my growing later on,
so please bear with discomfort.

<br>
- Comment language : English
- Date of creation : Sep 7th ~ Sep 18th 2022
- Date of debugging : Sep 19th ~ Sep 20th 2022
- Date of upload in Github : Sep 20th 2022
- Date of deployment : <strike>Nov 22th 2022</strike>
- Deployment Tool : <strike>Pythonanywhere</strike>

# Functions
- Navbar(responsive), Feed
- Feed upload (text, pic, text and pic)
- Feed like (likeicon, likecount)
- Comment
- Comment like
- Comment's comment
- Feed modify
- Feed delete (data delete)
- Feed hide (data exist)
- Feed share
- News (Beautiful soup(realtime news)
- News Search
- Login, Logout, Signup

# Sample pictures
![실제컬러](https://user-images.githubusercontent.com/106279616/191629643-d0877491-ecb7-4275-b022-5212485c4090.png)

![기능](https://user-images.githubusercontent.com/106279616/191629519-37debe87-b362-4a51-9093-6f3e14d13f81.png)

# Sample videos
All page looks like white in the videos but real look is like the picture above,
<br>So please pay attention only to functions.
<br>
<h3> 1. Upload feed, Like: </h3>
<video src="https://user-images.githubusercontent.com/106279616/191656908-86796606-6ba4-49bf-be79-ad199dacde5f.mp4"></video>
<h3> 2. Comment: </h3>
<video src="https://user-images.githubusercontent.com/106279616/191656944-58412787-06b1-467e-b67e-d903238acac0.mp4"></video>
<h3> 3. Comment Like, Comment's comment: </h3>
<video src="https://user-images.githubusercontent.com/106279616/191656972-dae22358-8c45-46f7-9e9d-07dbf779828e.mp4"></video>
<h3> 4. Share feed, Like and comment with another username: </h3>
<video src="https://user-images.githubusercontent.com/106279616/191657008-6713f692-ef85-44fd-a592-ecec8ce0e6e7.mp4"></video>
<h3> 5. Modify, Delete, Hide: </h3>
<video src="https://user-images.githubusercontent.com/106279616/191657027-db65ff9c-d218-434c-b7c5-d5f66ca07e06.mp4"></video>
<h3> 6. Realtime news(beautifulsoup), News search: </h3>
<video src="https://user-images.githubusercontent.com/106279616/191657054-35668db2-c213-4122-9ccb-03ac0c928826.mp4"></video>
<h3> 7. Signup, Login: </h3>
<video src="https://user-images.githubusercontent.com/106279616/191657084-865b5a94-30d8-455c-b0db-34b98b9e4414.mp4"></video>
<h3> 8. Responsive website: </h3>
<video src="https://user-images.githubusercontent.com/106279616/191657115-1e998ec3-60a5-4441-ab7c-7a4da2b1aad1.mp4"></video>
