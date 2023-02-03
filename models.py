from pydantic import BaseModel


class Register(BaseModel):
    username: str
    email: str
    password: str

class Login(BaseModel):
    email: str
    password: str


class Blog(BaseModel):
    title: str
    description: str
    image: str

class Question(BaseModel):
    question: str

class Answer(BaseModel):
    answer: str

class ForgetPassword(BaseModel):
    email: str

class NewPassword(BaseModel):
    email: str
    password: str

class Comment(BaseModel):
    userid: str
    comment: str
    blogid: str
    username: str

class EditComment(BaseModel):
    newComment: str

class Subscribed(BaseModel):
    userid: str