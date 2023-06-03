from flask import Flask, render_template, redirect, request, session
from flask_session import Session

from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL

from helpers import login_required, date_time, check_password, update_archive, is_login


app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = "#notaking"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")


@app.route("/")
@is_login
def starting_page():
    return render_template("starting-page.html")


@app.route("/login", methods=["GET", "POST"])
@is_login
def login_page():

    if request.method == "POST":

        email = request.form.get("email").lower()
        password = request.form.get("password")

        if not email or not password:
            return redirect("/login")

        User = db.execute("SELECT * FROM users WHERE user_email = ?", email)

        # check user input, if the email is available in the database and the password is correct
        if len(User) != 1 or not check_password_hash(User[0]["user_password"], password):
            return render_template("login-page.html", error_message="block")

        # setting the sessions for id and name
        session["user_id"] = User[0]["id"]
        session["name"] = User[0]["user_name"]

        return redirect("/home")

    else:
        return render_template("login-page.html", error_message="none")


@app.route("/register", methods=["GET", "POST"])
@is_login
def register_page():

    if request.method == "POST":
        # getting user inputs
        name = request.form.get("name").upper()
        email = request.form.get("email").lower()
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")

        if not name or not email or not password or not confirm_password or len(password) < 9:
            return redirect("/register")

        is_email_exist = db.execute("SELECT user_email FROM users WHERE user_email = ?", email)
        is_name_exist = db.execute("SELECT user_name FROM users WHERE user_email = ?", name)

        # checks the user input, for [email, user name, password match, and password validation]
        if not name.isalpha():
            return render_template("register-page.html", error="block", error_message="user name must be letters!")
        if is_email_exist:
            return render_template("register-page.html", error="block", error_message="email already exist!")
        elif is_name_exist:
            return render_template("register-page.html", error="block", error_message="user name is taken")
        elif password != confirm_password:
            return render_template("register-page.html", error="block", error_message="passwords don't match!")
        elif not check_password(password):
            return render_template("register-page.html", error="block", error_message="password must contain 7 letters and 2 numbers at least!")

        hash_password = generate_password_hash(password)  # encypt the password

        join_date, time = date_time()  # only need the date

        db.execute("INSERT INTO users (user_name, user_email, user_password, join_date) VALUES (?, ?, ?, ?)",
                   name, email, hash_password, join_date)

        User = db.execute("SELECT * FROM users WHERE user_email = ?", email)

        session["user_id"] = User[0]["id"]
        session["name"] = User[0]["user_name"]

        db.execute("INSERT INTO notes_archive (user_id, notes_count, words_count, letters_count, deleted_notes, edited_notes) VALUES (?, ?, ?, ?, ?, ?)",
                   session["user_id"], 0, 0, 0, 0, 0)

        return redirect("/home")

    else:
        return render_template("register-page.html", error="none", error_message="")


@app.route("/home", methods=["GET", "POST"])
@login_required
def home_page():
    if request.method == "POST":
        fields = ['field1', 'field2', 'field3']  # the name of the inputs
        Fields_value = []  # the value of the inputs will append to this

        for field in fields:
            Fields_value.append(request.form.get(field).lstrip())

        for note in Fields_value:
            if note != '':
                if note == "update_user_note":  # for security reason the name of update button is this!
                    note = note.replace("_", "-")

                date, time = date_time()

                # insert new note inot the database
                db.execute("INSERT INTO user_notes (user_id, note, date, time) VALUES (?, ?, ?, ?)",
                           session["user_id"], note, date, time)

                update_archive("", note, db)  # update the archive with new note

        return redirect("/home")

    else:
        Notes = db.execute("SELECT note FROM user_notes WHERE user_id = ? ORDER BY date DESC, time DESC LIMIT 3",
                           session["user_id"])
        return render_template("home-page.html", name=session["name"].title(), Data=Notes)


@app.route("/my_notes", methods=["GET", "POST"])
@login_required
def mynotes_page():
    # getting all the info from the user_notes database
    Notes = db.execute("SELECT * FROM user_notes WHERE user_id = ? ORDER BY date DESC, time DESC", session["user_id"])

    if request.method == "POST":
        if request.form["submit_button"] == "update_user_note":  # if user want to edit a note
            try:
                new_note = request.form.get("new_note").lstrip()
                old_note = request.form.get("old_note").lstrip()
            except TypeError:
                return redirect("/my_note")

            if not new_note or not old_note or new_note == "" or old_note == "":
                return redirect("/my_notes")
            elif new_note == "update_user_note":  # security reason
                new_note = new_note.replace("_", "-")

            # searching through notes, if found update archive first with delete, then update the note finnaly update archive with edit
            for data in Notes:
                if data['note'] == old_note:
                    update_archive("delete", old_note, db)

                    date, time = date_time()
                    db.execute("UPDATE user_notes SET note = ?, date = ?, time = ? WHERE user_id = ? AND note = ?",
                               new_note, date, time, session["user_id"], old_note)

                    update_archive("edit", new_note, db)
                    break

            return redirect("/my_notes")

        else:
            delete_note = request.form.get("submit_button")  # if user wants to delete a note

            if delete_note:
                for data in Notes:  # searching through notes
                    if data['note'] == delete_note:
                        db.execute("DELETE FROM user_notes WHERE user_id = ? AND note = ?", session["user_id"], delete_note)
                        update_archive("delete", delete_note, db)
                        break

            return redirect("/my_notes")

    else:
        return render_template("mynotes-page.html", name=session["name"].title(), notes=Notes)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile_page():
    # getting all the info about the user and the archive to display it in a table
    User = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    Archive = db.execute("SELECT * FROM notes_archive WHERE user_id = ?", session["user_id"])

    if request.method == "POST":
        if request.form["submit_button"] == "change_password":  # if user wants to change the password

            # getting the inputs
            current_password = request.form.get("current_password")
            new_password = request.form.get("new_password")
            confirm_password = request.form.get("confirm_password")

            # checking the user inputs, not providing =, password don't match, password validaty
            if not current_password or not new_password or not confirm_password or len(new_password) < 9:
                return redirect("/profile")
            elif not check_password_hash(User[0]["user_password"], current_password):
                return render_template("user-page.html", error=True, msg="Incorrect Password!!", archive=Archive[0], user=User[0])
            elif new_password != confirm_password:
                return render_template("user-page.html", error=True, msg="Passwords Don't Match!!", archive=Archive[0], user=User[0])
            elif not check_password(new_password):
                return render_template("user-page.html", error=True, msg="password must contain 7 letters and 2 numbers at least!!!", archive=Archive[0], user=User[0])

            hash_password = generate_password_hash(new_password)  # encrypt the new password

            # update the user password with new password(hash) in the database
            db.execute("UPDATE users SET user_password = ? WHERE id = ?", hash_password, session["user_id"])

            return render_template("user-page.html", error=True, msg="password successfully changed :)", archive=Archive[0], user=User[0])

        elif request.form["submit_button"] == "deactivate_account":  # if user wants to delete account
            # getting user inputs
            password = request.form.get("password")
            confirm_password = request.form.get("confirm_to_delete")

            # checking user inputs [password]
            if not password or not confirm_password or len(password) < 9:
                return redirect("/profile")
            elif not check_password_hash(User[0]["user_password"], password):
                return render_template("user-page.html", error=True, msg="Unable To Deactivate Incorrect Password!!", archive=Archive[0], user=User[0])
            elif password != confirm_password:
                return render_template("user-page.html", error=True, msg="Passwords Don't Match", archive=Archive[0], user=User[0])

            # delete the user information from teh database, first in the secondery tables then in the primary table
            db.execute("DELETE FROM notes_archive WHERE user_id = ?", session["user_id"])
            db.execute("DELETE FROM user_notes WHERE user_id = ?", session["user_id"])
            db.execute("DELETE FROM users WHERE id = ?", session["user_id"])

            return redirect("/logout")

    else:
        return render_template("user-page.html", error=False, msg="", archive=Archive[0], user=User[0])


@app.route("/logout")
def logout():
    """clears the sessions and redirect the user to the starting-page"""
    session.clear()  # clearing the user session

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)