from sqlalchemy import create_engine, Integer, String, Float, Column, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, sessionmaker, relationship
import datetime

from database_connection import engine

Base = declarative_base()

class Company(Base):
    __tablename__ = 'company'
    id: Mapped[int]= mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    location: Mapped[str] = mapped_column(String(30), nullable=False)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    industry: Mapped[str] = mapped_column(String(30), nullable=False)
    address: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False)

    #cascade="all, delete-orphan" this means that if a company is deleted, all of the users in that company will also be deleted
    users: Mapped[list["User"]] = relationship(back_populates="company", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Company(id={self.id}, name={self.name}, location={self.location}, size={self.size}, industry={self.industry})"


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30),nullable=False)
    email: Mapped[str] = mapped_column(String(100),nullable=False)

    #the backpopulate establishes a bidirectional relationship between the user and the posts -  if one side of the relationship is changed, it will update the other side as well
    #if we didn't have this, then the Post object won't be able to be connected it a user. would have to manually create that function
    #User.company and Company.user refer to each other
    #can go from user to company and company to user seamlessly
    company: Mapped["Company"] = relationship(back_populates="users")
    documents: Mapped[list["Document"]] = relationship(back_populates="users", cascade="all, delete-orphan")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False)

    def __repr__(self):
        return f"User(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, email={self.email})"

class Document(Base):
    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    user: Mapped["User"] = relationship(back_populates="documents")
    bucket_key: Mapped[str] = mapped_column(String(100), nullable=False)
    

    def __repr__(self):
        return f"Document(id={self.id}, title={self.title}, user_id={self.user_id})"


    


    
