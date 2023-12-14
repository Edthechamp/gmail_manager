from flask import Flask, render_template, request


import account_manage

app = Flask(__name__)

class Account:
    def __init__(self, name, gmail):
        self.name = name
        self.gmail = gmail
        self.pressed = False
        self.authenticate(self.gmail)

    def authenticate(self,gmail):
        self.token = account_manage.gmail_authenticate(self.gmail)
        print(self.token)
# In-memory storage for accounts
accounts = []

@app.route('/')
def index():
    return render_template('index.html', accounts=accounts)

@app.route('/add_account', methods=['POST'])
def add_account():
    name = request.form.get('name')
    gmail = request.form.get('Enter gmail:')
    new_account = Account(name, gmail)
    accounts.append(new_account)
    return render_template('index.html', accounts=accounts)

if __name__ == '__main__':
    app.run(debug=True)
