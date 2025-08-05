from extensions import db  # Import db from the project's root extensions.py
from flask_login import UserMixin
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey

# CONFIGURE TABLES
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    comments = relationship("Comment", back_populates="parent_post")


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    badge: Mapped[str] = mapped_column(String(100), unique=True)
    pin: Mapped[str] = mapped_column(String(100))
    category: Mapped[str] = mapped_column(String(50), nullable=True) # Added user category
    company: Mapped[str] = mapped_column(String(150), nullable=True) # Changed to Mapped syntax
    posts = relationship("BlogPost", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="comment_author", cascade="all, delete-orphan")


class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("blog_posts.id")) # Corrected Mapped[str] to Mapped[int]
    parent_post = relationship("BlogPost", back_populates="comments")