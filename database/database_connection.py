import os
from sqlalchemy import create_engine, text


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

