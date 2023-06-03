from flask import redirect, session
from functools import wraps
from datetime import datetime
from cs50 import SQL


def login_required(func):
    """make sure that the user is loged in, in a valid way"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:  # if the user is not logged in, redirect to starting page
            return redirect("/")
        return func(*args, **kwargs)
    return wrapper


def is_login(func):
    """is the user already loged in no need to go to the first three pages, redirects it directly into home page"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" in session:
            return redirect("/home")
        return func(*args, **kwargs)
    return wrapper


def check_password(password):
    """check if the user at least typed 7 letters and 2 numbers, returns a bool, True if valid"""
    count = [0, 0]  # count for the letter and number, first index is letter, second is number

    for char in password:
        if char.isalpha():
            count[0] += 1
        elif char.isdigit():
            count[1] += 1

    return count[0] >= 7 and count[1] >= 2  # True if the user password is valid


def date_time():
    """return a list of two index [date, time]"""
    return datetime.now().strftime("%Y-%m-%d %H:%M").split(" ")


def update_archive(which, text, db):
    """basically it adds the counts to the notes_archive database by default, if which is edit the e_count is one, if delete deduct the counts from the database
        and we use the db argument from the app.py to execute the sql query"""

    letter_count, d_count, e_count = 0, 0, 0
    words_count, n_count = 1, 1

    # count the number of letters and words
    for char in text:
        if char.isalpha():
            letter_count += 1
        elif char.isspace():
            words_count += 1

    if which == "edit":
        e_count = 1
        d_count = -1
    elif which == "delete":
        # using this it will deduct the number without repeating teh code twice
        letter_count *= -1
        words_count *= -1
        n_count *= -1
        d_count = 1

    # only one row of archive per user is created always
    Archive = db.execute("SELECT * FROM notes_archive WHERE user_id = ?", session["user_id"])[0]

    l = Archive['letters_count'] + letter_count
    w = Archive['words_count'] + words_count
    n = Archive['notes_count'] + n_count
    d = Archive['deleted_notes'] + d_count
    e = Archive['edited_notes'] + e_count

    # update the values
    db.execute("UPDATE notes_archive SET notes_count = ?, words_count = ?, letters_count = ?, deleted_notes = ?, edited_notes = ? WHERE user_id = ?",
               n, w, l, d, e, session["user_id"])

