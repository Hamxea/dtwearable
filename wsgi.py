from app import app

""" This class is added to be able to start the application with application servers of type wsgi """

if __name__ == '__main__':
    app.run()