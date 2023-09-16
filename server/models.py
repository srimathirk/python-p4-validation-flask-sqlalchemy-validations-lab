from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("All author should have a name")
        return name

    @validates('phone_number')
    def validate_email(self, key, phone_number):
        pattern = r'\d{10}$'
        if not re.match(pattern,phone_number):
            raise ValueError("All author should have a phonenumber exactly 10 digits")
        return phone_number


class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'


    @validates('title')
    def validate_title(self,key,title):
        
        if not title:
            raise ValueError("All posts have a title.")
        
        clickbait_words = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(word in title for word in clickbait_words):
            raise ValueError("All posts in title have clickbait validator.")
        return title

    @validates('content')
    def validate_content(self,key,content):
        if len(content) <= 250:
            raise ValueError("Post content is at least 250 characters long.")
        return content


    @validates('summary')
    def validate_summary(self,key,summary):
        
        if len(summary) >= 250:
            raise ValueError("Post summary is a maximum of 250 characters.")
        return summary

    @validates('category')
    def validate_category(self,key,category):
        
        if category not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Post category is either Fiction or Non-Fiction.")
        return category

    