import re
from flask import Flask, make_response, render_template, request

app = Flask(__name__)
application = app

requests_data = []    

def check_number(number: str) -> {str, str}:
    number = re.sub(r'[-\(\)\s.+]', '', number)

    digits_count = sum(map(lambda x: x.isdigit(), number))
    if not(digits_count == 10 or digits_count == 11 and (number[0] == "7" or number[0] == "8")):
        return "Недопустимый ввод. Неверное количество цифр.", ""
   
    if digits_count != len(number):
        return "Недопустмый ввод. В номере телефона встречаются недопустимые символы", ""
    
    number_without_prefix: str = number[len(number) - 10:]
    formatted_number = f"8-{number_without_prefix[:3]}-{number_without_prefix[3:6]}-{number_without_prefix[6:8]}-{number_without_prefix[8:]}"

    return "", formatted_number

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods=["GET", "POST"])
def form():
    log_request()
    if request.method == "GET":
        return render_template('form.html')

    error, number = check_number(request.form.get("phone_number", ""))
    return render_template('form.html', error=error, number=number)

@app.route('/requests')
def requests():
    log_request()
    return render_template('requests.html', requests=requests_data)

def log_request():
    requestData = {
        "params": request.args,
        "headers": request.headers,
        "cookie": request.cookies,
        "form_params": request.form
    }
    requests_data.append(requestData)
    return

@app.route('/set_or_delete_cookie')
def set_or_delete_cookie():
    log_request()
    cookie_name = 'Something cookie'
    cookie_value = request.cookies.get(cookie_name)

    content = render_template('cookie.html', cookie_exists=(cookie_value is not None))

    resp = make_response(content)

    if cookie_value is None:
        resp.set_cookie(cookie_name, 'cookie_value')
    else:
        resp.delete_cookie(cookie_name)

    return resp
