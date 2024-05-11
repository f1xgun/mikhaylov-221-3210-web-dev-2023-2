import csv
from io import BytesIO, StringIO
from flask import Blueprint, make_response, render_template, request, url_for
from flask_login import current_user, login_required
from init import db_connector
from decorators import check_rights

visit_logs = Blueprint('visit_logs', __name__, template_folder="templates", static_folder="static")

class VisitRecord():
    def __init__(self, id, path, user_name, created_at):
        self.id = id
        self.user_name = user_name
        self.path = path
        self.created_at = created_at
    
class VisitLogsButton():
    def __init__(self, text, url):
        self.text = text
        self.url = url

@visit_logs.route('/')
@login_required
def all_logs():
    page = int(request.args.get("page", 0))
    has_prev_page = page != 0
    is_admin=current_user.is_admin()
    url_for_prev = url_for('visit_logs.all_logs', page=page-1)
    url_for_next = url_for('visit_logs.all_logs', page=page+1)

    title = 'Журнал посещений'
    cols_name = ['№', 'Пользователь', "Страница", "Дата"]

    visit_records, has_next_page = get_all_logs(is_admin, page=page)
    records = [[record.id, record.user_name, record.path, record.created_at] for record in visit_records]

    buttons = []
    if is_admin:
        buttons = [VisitLogsButton('Отчет по страницам', url_for('visit_logs.pages_report')), VisitLogsButton('Отчет по пользователям', url_for('visit_logs.users_report'))]

    return render_template('visit_logs.html', 
                           title=title, 
                           cols_name=cols_name, 
                           records=records, 
                           buttons=buttons, 
                           has_next_page=has_next_page, 
                           has_prev_page=has_prev_page, 
                           page=page + 1,
                           url_for_prev=url_for_prev,
                           url_for_next=url_for_next)

def get_all_logs(is_admin=False, page=0, limit=10):
    query = '''
    SELECT vl.id, vl.path, vl.created_at, users.last_name, users.first_name, users.middle_name 
    FROM visit_logs vl LEFT JOIN users ON users.id = vl.user_id
    {is_not_admin_placeholder}
    ORDER BY created_at DESC
    '''
    placeholder = {
        'is_not_admin_placeholder': '' if is_admin else 'WHERE users.id = %s'
    }
    query = query.format(**placeholder)
    parameters = []
    if not is_admin:
        parameters.append(current_user.id)
    if limit:
        query += " LIMIT %s"
        parameters.append(limit + 1)
    if page:
        query += " OFFSET %s"
        parameters.append(page * limit)
    with db_connector.connect().cursor(named_tuple=True) as cursor:
        cursor.execute(query, tuple(parameters))
        
        visit_logs = cursor.fetchall()
    records = []
    for log in visit_logs:
        name = ""
        if log.last_name:
            name += log.last_name
        if log.first_name:
            name += " " + log.first_name
        if log.middle_name:
            name += " " + log.middle_name
        if name == "":
            name = "Неаутентифицированный пользователь"
        records.append(VisitRecord(id=log.id, path=log.path, user_name=name, created_at=log.created_at))
    has_more = len(records) == limit + 1
    return (records[:limit], has_more)

@visit_logs.route('/pages_report')
@login_required
@check_rights(required_role="Администратор")
def pages_report():
    page = int(request.args.get("page", 0))
    has_prev_page = page != 0
    url_for_prev = url_for('visit_logs.pages_report', page=page-1)
    url_for_next = url_for('visit_logs.pages_report', page=page+1)

    title="Отчет посещений по страницам"
    buttons=[VisitLogsButton("Экспортировать в CSV", url_for("visit_logs.export_pages_report_in_csv"))]
    cols_name=["№", "Страница", "Количество посещений"]

    records, has_next_page = get_pages_report(page=page, limit=10)
    return render_template("visit_logs.html", 
                           title=title, 
                           buttons=buttons, 
                           cols_name=cols_name, 
                           records=records,
                           has_next_page=has_next_page,
                           has_prev_page=has_prev_page,
                           url_for_prev=url_for_prev,
                           url_for_next=url_for_next,
                           page=page + 1)

def get_pages_report(page=0, limit=10):
    query = '''
    SELECT path, COUNT(*) as views_count
    FROM visit_logs
    GROUP BY path
    ORDER BY COUNT(*) DESC
    '''
    parameters = []
    if limit:
        query += " LIMIT %s"
        parameters.append(limit + 1)
    if page:
        query += " OFFSET %s"
        parameters.append(page * limit)

    with db_connector.connect().cursor(named_tuple=True) as cursor:
        cursor.execute(query, tuple(parameters))
        visit_logs = cursor.fetchall()

    records = []
    for i in range(len(visit_logs)):
        number = i + 1
        if page:
            number += page
        record = [number, visit_logs[i].path, visit_logs[i].views_count]
        records.append(record)
    has_more = False
    if limit:
        has_more = len(records) == limit + 1 
    return (records[:limit], has_more)

@visit_logs.route("/export_pages_report")
@login_required
@check_rights(required_role="Администратор")
def export_pages_report_in_csv():
    records, _ = get_pages_report(None, None)
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['№', 'Страница', 'Количество посещений'])
    for record in records:
        cw.writerow([str(item) for item in record])
    output = make_response(si.getvalue().encode('utf-8'))
    output.headers["Content-Disposition"] = "attachment; filename=pages_report.csv"
    output.headers["Content-type"] = "text/csv; charset=utf-8"
    return output

@visit_logs.route('/users_report')
@login_required
@check_rights(required_role="Администратор")
def users_report():
    page = int(request.args.get("page", 0))
    has_prev_page = page != 0
    url_for_prev = url_for('visit_logs.users_report', page=page-1)
    url_for_next = url_for('visit_logs.users_report', page=page+1)
    title="Отчет посещений по пользователям"
    buttons=[VisitLogsButton("Экспортировать в CSV", url_for("visit_logs.export_users_report_in_csv"))]
    cols_name=["№", "Пользователь", "Количество посещений"]

    records, has_next_page = get_users_report(page=page, limit=10)
    return render_template("visit_logs.html", 
                           title=title, 
                           buttons=buttons, 
                           cols_name=cols_name, 
                           records=records,
                           page=page + 1,
                           has_prev_page=has_prev_page,
                           has_next_page=has_next_page,
                           url_for_prev=url_for_prev,
                           url_for_next=url_for_next)

def get_users_report(page=0, limit=10):
    query = '''
    SELECT u.last_name, u.first_name, u.middle_name, COUNT(*) as views_count
    FROM visit_logs vl LEFT JOIN users u ON vl.user_id = u.id
    GROUP BY vl.user_id
    ORDER BY COUNT(*) DESC
    '''
    parameters = []
    if limit:
        query += " LIMIT %s"
        parameters.append(limit + 1)
    if page:
        query += " OFFSET %s"
        parameters.append(page * limit)

    with db_connector.connect().cursor(named_tuple=True) as cursor:
        cursor.execute(query, tuple(parameters))
        visit_logs = cursor.fetchall()

    records = []
    for i in range(len(visit_logs)):
        name = ""
        if visit_logs[i].last_name:
            name += visit_logs[i].last_name
        if visit_logs[i].first_name:
            name += " " + visit_logs[i].first_name
        if visit_logs[i].middle_name:
            name += " " + visit_logs[i].middle_name
        if name == "":
            name = "Неаутентифицированный пользователь"
        number = i + 1
        if page:
            number += page
        record = [number, name, visit_logs[i].views_count]
        records.append(record)
    
    has_more = False
    if limit:
        has_more = len(records) == limit + 1  
    return (records[:limit], has_more)

@visit_logs.route("/export_users_report")
@login_required
@check_rights(required_role="Администратор")
def export_users_report_in_csv():
    records, _ = get_users_report(None, None)
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['№', 'Пользователь', 'Количество посещений'])
    for record in records:
        cw.writerow([str(item) for item in record])
    output = make_response(si.getvalue().encode('utf-8'))
    output.headers["Content-Disposition"] = "attachment; filename=users_report.csv"
    output.headers["Content-type"] = "text/csv; charset=utf-8"
    return output    

# Названия столбцов - []str
# Записи - [][]str
# Кнопки - []Button
# Button(title, href)
