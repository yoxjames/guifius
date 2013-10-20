import sys
from app import app
import app.db
from contextlib import closing

def init_db():
    database = app.db.Database(refresh=True, code_val=True)

def reset_codes():
    database = app.db.Database(refresh=False, code_val=True)

def main(argv):
    if argv == "init":
        init_db()
    elif argv == "help":
        print("manage.py help:")
        print("manage.py init: Initialize Database")
    else:
        print("Invalid: Try manage.py help a = " + argv)


if __name__ == "__main__":
    main(sys.argv[1:])


