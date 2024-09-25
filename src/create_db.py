from sqlmodel import Session
from .database import create_db_and_tables, engine
from .models import *

def main():
    create_db_and_tables()

if __name__ == "__main__":
    main()
