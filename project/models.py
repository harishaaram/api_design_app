import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Story(db.Model):
    __tablename__ = "story"
    sid = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    publishers = db.relationship("Publisher", backref="story", lazy=True)

    def add_publisher(self, name):
        p = Publisher(name=name, story_id=self.sid)
        db.session.add(p)
        db.session.commit()


class Publisher(db.Model):
    __tablename__ = "publisher"
    pid = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String, nullable=False)
    story_id = db.Column(db.Integer, db.ForeignKey("story.sid"), nullable=False)


