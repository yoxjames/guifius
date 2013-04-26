import sys
from app import app
import app.db
from contextlib import closing

def init_db():
    app.db.init_db()

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


