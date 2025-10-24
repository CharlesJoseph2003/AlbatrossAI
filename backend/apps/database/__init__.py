import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Engine is the central source of connections to database and is a holding space called connection pool for 
#database connections

#engine is global object and is created once for database server 

#engine includes 3 things:
# - what kind of database we are connecting with -  in this case digital ocean postgres
# - what Database API(DPAPI) we are using - allows python to talk to the database - in our case, I am using is
#psycopg2
# in the case of psycopg2, the ssl is required in the connection string - meaning that only secure connections can be
#established. If it was ssl=prefer, then if the connection fails, it will fall back on unencrypted connection
# - how do we locate the database - our database is in digital ocean in ny3
engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
#echo=True tell the library to print all sql commands to it executes to the console
#good for testing but not for production environments because it will make things slow
#set echo to False in production
#can configure to a logger instead

#Session establishes conversations with the database and represents the holding zone for all the objects
#it is the interface where SELECT and other queries are executed and will return and modify ORM mapped objects
#ORM objects are maintained inside of a session
#Session begins in stateless form 
#Once a query is issued, it will request a connection resource from the engine and then establish a transaction on that session
#Then when the transation ends, the connection resource is returned to the connection pool. Then when a new transation
#begins, it will request a connection resource from the connection pool and establish a new transaction on that session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Session sits on top of the engine and it is used to manage transactions, keeps track of objects that are loaded
#and modified, and converts python objects to sql statements 
#sessions are opened and closed on a per request basis


#steps to create a session
#1. session obejct is created in memeory
#2. it borrows connection from engins connection pool when needed
#3. it can now start a transation, add objects, and query the database
#4. then session is closed and the connection is returned to the connection pool
#5. it clears its internal object cache 


#context manager is for scripts, manual db operations, and testing, not for production
@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
        yield db      # make the session available to caller
    finally:
        db.close()    # always return connection to pool

#this is for fastapi depends, fastapi doesnt execute context managers, it executes functions
def get_db():
    db = SessionLocal()
    try:
        yield db      # make the session available to caller
    finally:
        db.close()    # always return connection to pool

#yield: this turns a normal function into a generator function
#generator function is able to pause and resume - it can return multiple values over time
#yield is like pressing pause on a video, the first part before the yield runs the setup, 
#the the vidoe is paused while something happens - this case being the fastapi route is running
#thenafter the yield runs, the cleanup happens and the db connection is closed and the system resumes

#generator functions are used when you want to produce a sequence of results lazily, as opposed to computing everything all at once
#use cases: streaming or large data - dont want to load a ton of data into memory at once


