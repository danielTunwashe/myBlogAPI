#creating a script to run our application instead of our flask run
from api import create_app


app=create_app()

if __name__ == "__main__":
    app.run()