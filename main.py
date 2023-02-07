
from fastapi import FastAPI, File
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
import requests
import base64
from PIL import Image
import io
from functions import getUserById
import models
import uuid

from email.message import EmailMessage
import ssl
import smtplib
import math
import random

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():

    db = mysql.connector.connect(
        host="sql866.main-hosting.eu",
        user="u124366181_emobettingvps",
        password="HZ96XCp7Lt3ZWe8%",
        database="u124366181_emobettingvps"
    )

    cursor = db.cursor()
    sql = "SELECT * FROM blogs"
    cursor.execute(sql)

    result = cursor.fetchall()

    return result


@app.post("/register")
async def register(register: models.Register):
    db = mysql.connector.connect(
        host="sql866.main-hosting.eu",
        user="u124366181_emobettingvps",
        password="HZ96XCp7Lt3ZWe8%",
        database="u124366181_emobettingvps"
    )
    cursor = db.cursor()

    userid = uuid.uuid1()

    userid = str(userid)

    sql = "INSERT INTO users (userid, username, email, password, status) VALUES (%s, %s, %s, %s, %s)"

    val = (userid, register.username, register.email,
           register.password, "client")
    cursor.execute(sql, val)

    db.commit()

    return "success"


@app.post("/login")
async def login(login: models.Login):
    db = mysql.connector.connect(
        host="sql866.main-hosting.eu",
        user="u124366181_emobettingvps",
        password="HZ96XCp7Lt3ZWe8%",
        database="u124366181_emobettingvps"
    )
    cursor = db.cursor()

    sql = "SELECT userid, password, username, status FROM users WHERE email = %s"
    val = (login.email,)
    cursor.execute(sql, val)
    data = {}
    result = cursor.fetchall()

    if result:
        # return result
        if result[0][1] == login.password:
            data["status"] = "success"
            data["username"] = result[0][2]
            data["userid"] = result[0][0]
            data["user_type"] = result[0][3]
            return data
        else:
            data["status"] = "Wrong Email or Password!"
            return data
    else:
        data["status"] = "Wrong Email or Password!"
        return data


@app.post("/post_blog")
async def post_blogs(blog: models.Blog):
    db = mysql.connector.connect(
        host="sql866.main-hosting.eu",
        user="u124366181_emobettingvps",
        password="HZ96XCp7Lt3ZWe8%",
        database="u124366181_emobettingvps"
    )

    cursor = db.cursor()

    blogid = uuid.uuid1()

    blogid = str(blogid)

    sql = "INSERT INTO blogs (blogid, blog_title, blog_description, blog_image) VALUES (%s, %s, %s, %s)"

    val = (blogid, blog.title, blog.description, blog.image)
    cursor.execute(sql, val)

    db.commit()

    return "success"


@app.get("/get_blogs")
async def get_blogs():
    db = mysql.connector.connect(
        host="sql866.main-hosting.eu",
        user="u124366181_emobettingvps",
        password="HZ96XCp7Lt3ZWe8%",
        database="u124366181_emobettingvps"
    )
    cursor = db.cursor()
    sql = "SELECT * FROM blogs"
    cursor.execute(sql)
    data = []
    results = cursor.fetchall()

    for result in results:
        data.append(
            {
                "blogid": result[1],
                "blog_title": result[2],
                "blog_description": result[3],
                "dop": result[5],
                "image": result[4]
            }
        )
    return data


@app.delete("/delete_blog")
async def delete_blog(blogid: str):
    db = mysql.connector.connect(
        host="sql866.main-hosting.eu",
        user="u124366181_emobettingvps",
        password="HZ96XCp7Lt3ZWe8%",
        database="u124366181_emobettingvps"
    )
    cursor = db.cursor()
    sql = "DELETE FROM blogs WHERE blogid = %s"
    val = (blogid,)

    cursor.execute(sql, val)

    db.commit()

    return "success"


@app.get("/getnoofcomments")
async def getnoofcomments(blogid: str):
    db = mysql.connector.connect(
        host="sql866.main-hosting.eu",
        user="u124366181_emobettingvps",
        password="HZ96XCp7Lt3ZWe8%",
        database="u124366181_emobettingvps"
    )
    cursor = db.cursor()
    sql = "SELECT COUNT(*) FROM comments WHERE blogid=%s"
    val = (blogid,)
    cursor.execute(sql, val)
    results = cursor.fetchall()

    for result in results:
        count = (result[0])

    return count


@app.get("/arbitrage-prematch")
async def get_arbitrage_prematch():
    db = mysql.connector.connect(
        host="sql866.main-hosting.eu",
        user="u124366181_emobettingvps",
        password="HZ96XCp7Lt3ZWe8%",
        database="u124366181_emobettingvps"
    )
    cursor = db.cursor()
    sql = "SELECT * FROM emo"

    cursor.execute(sql)

    data = []
    ids = []
    results = cursor.fetchall()

    for result in results:

        # if result[1] in ids:
        #     continue
        # else:
        ids.append(result[1])
        data.append(
            {
                "game_id": result[1],
                "rate": result[2],
                "time": result[3],
                "sport": result[4],
                "time_r": result[5],
                "date": result[6],
                "bookie_1": result[7],
                "bookie_2": result[8],
                "odd_1": result[9],
                "odd_2": result[10],
                "league_1": result[11],
                "league_2": result[12],
                "teams_1": result[13],
                "teams_2": result[14],
                "outcome_1": result[15],
                "outcome_2": result[16],
                "selection": result[17],
                "link_1": result[18],
                "link_2": result[19]
            }
        )
    print(ids)
    return data


@app.get("/single_game_data")
async def single_game_data(game_id: str):
    db = mysql.connector.connect(
        host="sql866.main-hosting.eu",
        user="u124366181_emobettingvps",
        password="HZ96XCp7Lt3ZWe8%",
        database="u124366181_emobettingvps"
    )
    cursor = db.cursor()
    sql = "SELECT * FROM emo WHERE game_id=%s"
    val = (game_id,)

    cursor.execute(sql, val)

    data = []

    results = cursor.fetchall()

    for result in results:

        data.append(
            {
                "game_id": result[1],
                "rate": result[2],
                "time": result[3],
                "sport": result[4],
                "time_r": result[5],
                "date": result[6],
                "bookie_1": result[7],
                "bookie_2": result[8],
                "odd_1": result[9],
                "odd_2": result[10],
                "league_1": result[11],
                "league_2": result[12],
                "teams_1": result[13],
                "teams_2": result[14],
                "outcome_1": result[15],
                "outcome_2": result[16],
                "selection": result[17],
                "link_1": result[18],
                "link_2": result[19]
            }
        )
    return data


@app.get("/sportsbooks")
async def sportsbooks():
    db = mysql.connector.connect(
        host="sql866.main-hosting.eu",
        user="u124366181_emobettingvps",
        password="HZ96XCp7Lt3ZWe8%",
        database="u124366181_emobettingvps"
    )
    cursor = db.cursor()
    sql = "SELECT DISTINCT bookie_1, bookie_2 FROM emo"

    cursor.execute(sql)

    data = []

    results = cursor.fetchall()

    for result in results:
        for r in result:
            data.append(r)

    data = list(dict.fromkeys(data))

    return data


@app.get("/get_by_sportsbooks")
async def get_by_sportsbooks(sportsbooks: str, min: float, max: float):
    db = mysql.connector.connect(
        host="sql866.main-hosting.eu",
        user="u124366181_emobettingvps",
        password="HZ96XCp7Lt3ZWe8%",
        database="u124366181_emobettingvps"
    )
    cursor = db.cursor()
    data = []
    books = sportsbooks.split(",")

    for book in books:
        sql = "SELECT * FROM emo WHERE bookie_1 = %s OR bookie_2 = %s"
        val = (book, book)
        cursor.execute(sql, val)

        ids = []
        results = cursor.fetchall()

        for result in results:
            if result[1] not in ids:
                rate = result[2]
                rate = float(rate.replace("%", ""))

                if min != 0 or max != 0:
                    if rate >= min and rate <= max:
                        data.append(
                            {
                                "game_id": result[1],
                                "rate": result[2],
                                "time": result[3],
                                "sport": result[4],
                                "time_r": result[5],
                                "date": result[6],
                                "bookie_1": result[7],
                                "bookie_2": result[8],
                                "odd_1": result[9],
                                "odd_2": result[10],
                                "league_1": result[11],
                                "league_2": result[12],
                                "teams_1": result[13],
                                "teams_2": result[14],
                                "outcome_1": result[15],
                                "outcome_2": result[16],
                                "selection": result[17],
                                "link_1": result[18],
                                "link_2": result[19]
                            }
                        )

                        ids.append(result[1])
                else:

                    data.append(
                        {
                            "game_id": result[1],
                            "rate": result[2],
                            "time": result[3],
                            "sport": result[4],
                            "time_r": result[5],
                            "date": result[6],
                            "bookie_1": result[7],
                            "bookie_2": result[8],
                            "odd_1": result[9],
                            "odd_2": result[10],
                            "league_1": result[11],
                            "league_2": result[12],
                            "teams_1": result[13],
                            "teams_2": result[14],
                            "outcome_1": result[15],
                            "outcome_2": result[16],
                            "selection": result[17],
                            "link_1": result[18],
                            "link_2": result[19]
                        }
                    )

                    ids.append(result[1])
    return data


@app.post("/post_question")
async def post_question(question: models.Question):
    db = mysql.connector.connect(
        host="sql866.main-hosting.eu",
        user="u124366181_emobettingvps",
        password="HZ96XCp7Lt3ZWe8%",
        database="u124366181_emobettingvps"
    )
    cursor = db.cursor()

    questionid = uuid.uuid1()

    questionid = str(questionid)

    sql = "INSERT INTO questions (question_id, question) VALUES (%s, %s)"

    val = (questionid, question.question)
    cursor.execute(sql, val)

    db.commit()

    return "success"


@app.get("/get_questions")
async def get_questions():
    db = mysql.connector.connect(
        host="sql866.main-hosting.eu",
        user="u124366181_emobettingvps",
        password="HZ96XCp7Lt3ZWe8%",
        database="u124366181_emobettingvps"
    )
    cursor = db.cursor()
    sql = "SELECT * FROM questions"

    cursor.execute(sql)

    data = []
    results = cursor.fetchall()

    for result in results:
        sql = "SELECT * FROM answers WHERE question_id = %s"
        val = (result[1],)
        cursor.execute(sql, val)

        answers = []
        anrs = cursor.fetchall()

        for anr in anrs:
            answers.append({
                "answer_id": anr[1],
                "qusetion_id": anr[2],
                "answer": anr[3]
            })

        data.append(
            {
                "question_id": result[1],
                "question": result[2],
                "answers": answers
            }
        )
    return data


@app.post("/post_answer")
async def post_answer(qID: str, answer: models.Answer):
    db = mysql.connector.connect(
        host="sql866.main-hosting.eu",
        user="u124366181_emobettingvps",
        password="HZ96XCp7Lt3ZWe8%",
        database="u124366181_emobettingvps"
    )
    cursor = db.cursor()

    answerid = uuid.uuid1()

    answerid = str(answerid)

    sql = "INSERT INTO answers (answer_id, question_id, answer) VALUES (%s, %s, %s)"

    val = (answerid, qID, answer.answer)
    cursor.execute(sql, val)

    db.commit()

    return "success"


@app.get("/verification")
async def verification():
    db = mysql.connector.connect(
        host="sql866.main-hosting.eu",
        user="u124366181_emobettingvps",
        password="HZ96XCp7Lt3ZWe8%",
        database="u124366181_emobettingvps"
    )
    email_sender = 'sithijakavee110@gmail.com'
    email_password = 'yaqfjenpkzpqnuta'

    email_receiver = 'sithijakavee420@gmail.com'

    subject = "Verify your account"
    body = """
        Heres your verification code : 434342432.
    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


@app.post("/check_email")
async def check_email(register: models.Register):
    db = mysql.connector.connect(
        host="sql866.main-hosting.eu",
        user="u124366181_emobettingvps",
        password="HZ96XCp7Lt3ZWe8%",
        database="u124366181_emobettingvps"
    )
    cursor = db.cursor()

    sql = "SELECT * FROM users WHERE email = %s"
    val = (register.email,)
    cursor.execute(sql, val)

    result = cursor.fetchall()

    if result:
        return "Email already used! Please try again with different email"
    else:
        digits = "0123456789"
        OTP = ""
        for i in range(6):
            OTP += digits[math.floor(random.random()*10)]

        email_sender = 'sithijakavee110@gmail.com'
        email_password = 'yaqfjenpkzpqnuta'

        email_receiver = register.email

        subject = "ODD NATIONAL | Verify your account"
        body = f"""
            Welcome to odd national. Thanks for joining with us.\n
            Heres your verification code is {OTP}
        """

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

        return OTP


@app.get("/delete")
async def delete():
    db = mysql.connector.connect(
        host="sql866.main-hosting.eu",
        user="u124366181_emobettingvps",
        password="HZ96XCp7Lt3ZWe8%",
        database="u124366181_emobettingvps"
    )
    cursor = db.cursor()

    sql = "DELETE FROM users WHERE id = 3"
    cursor.execute(sql,)


@app.post("/forget_password")
async def forget_password(forgetPassword: models.ForgetPassword):
    db = mysql.connector.connect(
        host="sql866.main-hosting.eu",
        user="u124366181_emobettingvps",
        password="HZ96XCp7Lt3ZWe8%",
        database="u124366181_emobettingvps"
    )
    digits = "0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random()*10)]

    email_sender = 'sithijakavee110@gmail.com'
    email_password = 'yaqfjenpkzpqnuta'

    email_receiver = forgetPassword.email

    subject = "ODD NATIONAL | Verify your email to change the password"
    body = f"""
        Welcome to odd national. Thanks for joining with us.\n
        Heres your verification code is {OTP}
    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

    return OTP


@app.post("/set_newPassword")
async def set_newPassword(newPassword: models.NewPassword):
    db = mysql.connector.connect(
        host="sql866.main-hosting.eu",
        user="u124366181_emobettingvps",
        password="HZ96XCp7Lt3ZWe8%",
        database="u124366181_emobettingvps"
    )
    cursor = db.cursor()

    sql = "UPDATE users SET password=%s WHERE email=%s"

    val = (newPassword.password, newPassword.email)
    cursor.execute(sql, val)

    db.commit()

    return "success"


@app.post("/post_comment")
async def post_comment(comment: models.Comment):
    db = mysql.connector.connect(
        host="sql866.main-hosting.eu",
        user="u124366181_emobettingvps",
        password="HZ96XCp7Lt3ZWe8%",
        database="u124366181_emobettingvps"
    )
    cursor = db.cursor()
    commentid = uuid.uuid1()
    commentid = str(commentid)
    sql = "INSERT INTO comments (commentid, userid, username, blogid, comment) VALUES (%s, %s, %s, %s, %s)"
    val = (commentid, comment.userid, comment.username,
           comment.blogid, comment.comment)
    cursor.execute(sql, val)

    db.commit()

    return "success"


@app.get("/get_comments")
async def get_comments(blogid: str):
    db = mysql.connector.connect(
        host="sql866.main-hosting.eu",
        user="u124366181_emobettingvps",
        password="HZ96XCp7Lt3ZWe8%",
        database="u124366181_emobettingvps"
    )
    cursor = db.cursor()
    sql = "SELECT * FROM comments WHERE blogid = %s"
    val = (blogid,)

    cursor.execute(sql, val)

    comments = cursor.fetchall()
    data = []

    for comment in comments:
        data.append(
            {
                "commentid": comment[1],
                "userid": comment[2],
                "username": comment[3],
                "blogid": comment[4],
                "comment": comment[5]
            }
        )
    return data


@app.delete("/delete_comment")
async def delete_comment(commentid: str):
    db = mysql.connector.connect(
        host="sql866.main-hosting.eu",
        user="u124366181_emobettingvps",
        password="HZ96XCp7Lt3ZWe8%",
        database="u124366181_emobettingvps"
    )
    cursor = db.cursor()
    sql = "DELETE FROM comments WHERE commentid=%s"
    val = (commentid,)
    cursor.execute(sql, val)
    db.commit()
    return "success"


@app.put("/edit_comment")
async def delete_comment(commentid: str, editcomment: models.EditComment):
    db = mysql.connector.connect(
        host="sql866.main-hosting.eu",
        user="u124366181_emobettingvps",
        password="HZ96XCp7Lt3ZWe8%",
        database="u124366181_emobettingvps"
    )
    cursor = db.cursor()
    sql = "UPDATE comments SET comment=%s WHERE commentid=%s"
    val = (editcomment.newComment, commentid)
    cursor.execute(sql, val)
    db.commit()
    return "success"


@app.post("/subscribed")
async def subscribed(subscribed: models.Subscribed):
    db = mysql.connector.connect(
        host="sql866.main-hosting.eu",
        user="u124366181_emobettingvps",
        password="HZ96XCp7Lt3ZWe8%",
        database="u124366181_emobettingvps"
    )
    cursor = db.cursor()
    sql = "UPDATE users SET subscribed=%s WHERE userid=%s"
    val = (1, subscribed.userid)
    cursor.execute(sql, val)
    db.commit()
    return "success"


@app.post("/check_subscribed")
async def check_subscribed(subscribed: models.Subscribed):
    db = mysql.connector.connect(
        host="sql866.main-hosting.eu",
        user="u124366181_emobettingvps",
        password="HZ96XCp7Lt3ZWe8%",
        database="u124366181_emobettingvps"
    )
    cursor = db.cursor()
    sql = "SELECT subscribed FROM users WHERE userid=%s"
    val = (subscribed.userid,)

    cursor.execute(sql, val)

    status = cursor.fetchall()

    for s in status:
        condition = s[0]

    if condition == 1:
        return True
    else:
        return False


@app.post("/upload_image")
async def upload_image(file: bytes = File(...)):
    fileName = str(uuid.uuid1()) + ".png"
    image = Image.open(io.BytesIO(file))
    image.save(f"""./images/{fileName}""")
    api_key = "00002c271048ee18441615750618d44b"
    query = {'key': api_key,
             'media': "https://cdn.eso.org/images/thumb300y/eso1907a.jpg"}
    url = f"""https://thumbsnap.com/api/upload"""
    r = requests.post(url=url, params=query)
    print(r)
