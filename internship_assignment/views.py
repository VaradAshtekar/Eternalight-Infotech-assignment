from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user, user_logged_out
from django.contrib.auth.models import User
import mysql.connector
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="root",
    database = "internship_task"
)

# mycursor = mydb.cursor()
#
# mycursor.execute("ALTER TABLE users ADD COLUMN email VARCHAR(255) AFTER name;")
#
#
# mycursor = mydb.cursor()
# mydb.commit()
# mycursor.execute("CREATE DATABASE internship_task")
#
# print("Database: ", mydb)

# mycursor = mydb.cursor()
#
# mycursor.execute("SHOW TABLES")
#
# for x in mycursor:
#   print(x)
username = ""
email = ""
user = ""
def index(request):
    s_stat = "Register here!!"
    color = "dark"
    if request.method == "POST":

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        print(username, type(username))
        s_stat = "Register here!"

        if password == password2 and len(password) >= 8:
            finalpassword = password
            user = User.objects.create_user(username, email, finalpassword)
            user.save()
            mycursor = mydb.cursor()

            sql = "INSERT INTO users (name,email, password) VALUES (%s,%s, %s)"
            val = (username,email, finalpassword)
            mycursor.execute(sql, val)

            mydb.commit()

            print(mycursor.rowcount, "record inserted.")
            s_stat = "Registration successful!!"
            color = "success"
        elif len(password) < 8:
            s_stat = "Password must be equal to or greater than 8 characters!!"
            color = "danger"
        else:
            s_stat = "Sorry! failed to register! check your passwords once again..."
            color = "danger"

    return render(request, 'index.html', context={"s_stat": s_stat, "color":color })



def loginsystem(request):
    if request.method == "POST":
        loginusername = request.POST.get('emaillog')
        loginpassword = request.POST.get('password')
        user = authenticate(request, username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            msg = "Successfully logged in!!"
            return redirect("info")
        else:
            msg = "Failed to log in!! please enter right password/ username!!"

        return render(request, 'login.html', context={"msg": msg})

    return render(request, 'login.html')

def info(request):

    print("user info: ",get_user(request), request.user.email)
    if request.method == "POST":
        newpass = request.POST.get('newpass')
        confirmnewpass = request.POST.get('confirmnewpass')
        if(confirmnewpass == newpass):
            finalresetpass = newpass
            print(finalresetpass)
            u = User.objects.get(username=request.user.username)
            print(u)
            u.set_password(finalresetpass)
            mycursor = mydb.cursor()
            mycursor.execute("UPDATE users SET password = (%s) WHERE name = (%s)", (finalresetpass, request.user.username))
            mydb.commit()
    return render(request, 'info.html')

def logout_view(request):
        logout(request)
        if(user_logged_out):
            return render(request, 'login.html')