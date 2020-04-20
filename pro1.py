from flask import Flask
from flask import request,render_template,redirect,url_for

import sqlite3
from flask import g


app=Flask(__name__)
app.debug = True

DATABASE  ='E:/Project Documents/Project_pyt/flaskapp.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# @app.teardown_appcontext
 #def close_connection(exception):
 #    db = getattr(g, '_database', None)
  #   if db is not None:
  #       db.close()
def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select Name,Mobile,E_mail,Other_tech from tb1 order by Name desc')
    tb1 = cur.fetchall()
    return render_template('index1.html', tb1=tb1)

@app.route('/add', methods=['GET','POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into tb1 (Name,Mobile,E_mail,Other_tech) values (?, ?,?,?)',
            [request.form['Name'], request.form['Mobile'], request.form['E_mail'], request.form['Other_tech']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))
@app.route('/dropdowns', methods=['GET','POST'])
def dropdown_entry():
	work_status=['Working','Not Working']			
	know_about=['Website','Poster','Hand Bill','Just Dial','UrbanPro','Sulekha','Friend','Seminar','Newspaper','Sign Board','Telecall','Others']
	Branch=['Gachibowli','Kukatpally']
	Area_interest=['Android','DevOps','AWS','Unity3D','Python','Data Analysis','Data Science','Big Data','Digital Marketing','Blockchain','Visual Design']
	Full_Stack=['HTML,CSS','Java Script','Bootstrap','Angular JS','Express JS','Mongo DB','Python','Node JS']
	sql1='insert into tb1 values (?,?) %(work_status)'
	sql2='insert into tb1 values (?,?,?,?,?,?,?,?,?,?,?,?) %(know_about)'
	sql3='insert into tb1 values (?,?) %(Branch)'
	sql4='insert into tb1 values (?,?,?,?,?,?,?,?,?,?,?) %(Area_interest)'
	sql5='insert into tb1 values (?,?,?,?,?,?,?,?) %(Full_Stack)'
	db.executemany(sql1,sql2,sql3,sql4,sql5)
	db.commit()
	return redirect(url_for('show_entries'))
	return render_template('index1.html',work_status=work_status,know_about=know_about,Branch=Branch,Area_interest=Area_interest,Full_Stack=Full_Stack)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('submit') == 'submit':
            print("submitted")

        return render_template('buttons.html',submit=submit)
  #  return redirect(url_for('show_entries'))


'''@app.route("/selection", methods=['GET','POST'])
def sel_action():
	if request.method == 'POST':
        if request.form.get('submit') == 'submit':'''

if __name__=="__main__":
	app.run(host='localhost',port=5000)