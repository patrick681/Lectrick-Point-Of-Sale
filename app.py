""" app.py """

from server.main import app

if __name__ == "__main__":
    app.run(debug=True, port=5555)