# **<h1><b>Notaking</b></h1>**

### ***Video Demo:***  <URL HERE>

### ***Description:*** my final CS50 project is about a web application using (HTML, CSS, JAVASCRIPT) as a front end and (PYTHON FLASK) as a back end,  that allows users to take notes on the web, I named "Notaking" which combined the "Note" with "taking", it is an application where users can write, delete, and edit their notes.

<br>

## ***website specification aspect:***
1- **starting-page**: it is the first page that greets with user, basically tells the user to choose login or register, and this page provided a cool transition when the mouse hovers the div, the div will reduce it is size, also if the mouse hovers into the name of the webpage(Notaking) a transition will happen, and there also a mouse hover for the buttons which make it bigger and glow a yellow color.

2- **register-page**: users can create their account on this page, simply using their name, email, password, and password confirmation to access the use of Notakaing and functionality, in this page the user must enter a unique name and email that is not the same as other users in the database, and also for the password must consist of at least 7 letters, 2 numbers, and a minimum length of 9 characters, then the user info will be stored in the sqlite3 database, but before that, it encrypts the password for security and safety reasons, finally redirect the user to the home-page.

3- **login-page**: if the user created an account before, then using the login-page can log into the website, simply by using their email and password, the email must be in the database to ensure that the user created an account before, and the password must match the password that is associated with the email, after checking for these security validation the user can access to the home-page.

4- **home-page**: the main function of the home page is that the user can take their note which has three inputs to type three notes simultaneously, over on top is a navbar that represents the website name, and on the far right there are three buttons (name, my notes, logout) the 'name' is the name of the user that is currently logged in when clicked it will show up the profile-page, 'my notes' it is a page where there is a history of all the user notes with date and time, 'log out' when clicked it asks the user for confirmation to logout when agreed it redirects it to the starting-page, there is also a 'recent notes' button in the home-page it will apear if the user currently has any notes in the database simply when clicked it will show up a table of recent notes that the user typed up to three notes and a 'hide' button if user wants to hide the table.

5- **mynotes-page**: on this page the user can see the history of notes that has been added to the home-page, it is a table that consists of (note, date, time, delete, and edit) from newest to oldest, for the 'delete' and 'edit' column it is an image button that represents delete and edit, if the user clicked the delete button that corresponds to a specific note it will delete the note from the database and update the page if the user clocked of edit button a form will show up below the navbar where the user can change the note if user doesn’t want it, it can simply the cancel button or click the update button to change the note and also the date and time, the navbar is same as the home-page apart from 'my notes' changed into 'home'.

6- **profile-page**: finally, the last page user profile, is a page where users can view their information about (user name, email, date of joining, number of (notes, words, letters, deleted notes, and edited notes)), also in this page the user can change their password on the navbar there is a button called 'change password' when clicked a form will show up with three inputs, current password, new password and confirm pasword, the user must type their valid password, and the new and confirm password must match and must be at least 9 character, etc.., apart from changing the password the user can deactivate the account a button called 'delete account' when clicked a form will show up with two inputs, password and confirm password, if it is valid the user account and information will be deleted fom the database, and redirect t to the staring-page, but the user can register with the deleted account using deleted email account but the information has been removed from the database, so it is starting from scratch.

<br>

## ***programming specification aspect:***
two pyhon files used in this project:<br>

1- **app.py**: it is the primary file where most of the rendering, executing database, and checking inputs happens, it consists of seven routes each rendering a specific file from the templates.<br>

***A brief description about each route:***<br>

* **'/'**: rendering starting-page.

* **'/register'**: if the method is get it renders the register-page, if it is post assign the inputs name to the specific variables and then check if the user inputs are valid, hash the user password, then store the information in the users database, and finally assign the name and id to the sessions and redirect to the home-page.

* **'/login'**: if the method is get, it renders the login-page, if it is post, assign the inputs to the variables then check if the email is in the database and if the password is correct, then assign the name and id to the sessions and redirect to the home-page.

* **'/home'**: rendering the home-page in get method, if it is post assign the value of the inputs into the array, then loop through the array if it is not None('') it will insert the note with it is date and time to the user_notes database, and finally update the notes_archive database.

* **'/my_notes'**: rendering the mynotes-page in get method, in post method if the submit button is update_user_note it will update the user note with new note, date, and time, and finally update the notes_archive database, if the submit button is not update_user_note then it will delete the note first by assigning the note value then check if it exist in the database finally delete it from the notes_user and update the notes_archive database.

* **'/profile'**: rendering the userprofile-page in get method, in post method if the submit button is change_password then it will check the current password and the match between new_password and confirm_password, if all of this is valid it will update the user password in the database, if the sybnit button is delete_account it will check the password and the confirm password if all of this is valid it will delete the data first from the notes_archive then user_notes and finally in the users database, then redirect to the logout route.

* **'/logout'**: basically clears the user sessions and redirects back to the '/'(starting-page).


2- **helpers.py**: in this file, there are 5 function that is used in the app.py.

* **login_requied**: this is a decorator function used for checking if the user has logged-in in a valid way, simply by checking if the session contains 'user_id' if it is not!, then redirects back to the starting-page.

* **is_login**: used for (starting, login, register) page, if the user is already logged in no need to go to these pages anymore, if the user wants they must use thr logout button, else they will be redirected back to the home-page.

* **check_password**: checks the user password, when registering, and changing the password, it counts the number of letters and numbers in the password, to be a valid password must contain at least 7 letters, and 2 numbers, and the length of the password 9, if not it returns False(invalid).

* **date_time**: simply returns a list consists of date, time.

* **update_archive**: basically counts the number of words and letters in a note, the function accepts three parameters, 'which' to determine whether to edit or delete, 'text' the note, and 'db' the database object, after counting the words, and letters, if the 'which' is edit e_count will be one and d_count will be -1, if the 'which' is delete then the count for the letters, words, and note multiplied by -1, and d_count will be 1, after that we get the information in the notes_archive and simply add the corresponding data column to the variable count, and finally update the counts for the notes_archive database.

<br>

## ***database specification aspect:***
I used (SQLITE3) for my project, three tables used in this database.

* **users**: consists of 5 column (id, user_name, user_email, user_password, join_date), it is the primary table that store the primary user information.

* **user_notes**: consists of 4 column (user_id, note, date, time) it is the secondery table linked to the 'users' table using 'id', it is used to store the users notes.

* **notes_archive**: consists of 6 column (user_id, notes_count, words_count, letters_count, deleted_notes, edited_notes), it is the secondery table linked by 'id' to the 'users' table, it is used to store the count for the number of notes, number of words and letters in all notes, number of deleted and edited note so far.

