import os
import sqlite3
from flask import Flask,request,g,redirect,url_for,render_template,flash,session
from functools import wraps


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
   DATABASE=os.path.join(app.root_path,'student.db'),
   DEBUG=True,
   SECRET_KEY='aslam'
))
app.config.from_envvar('FLASKR_SETTINGS',silent=True)



def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash(' You need to login first.')
            return redirect(url_for('login'))
    return wrap


def connect_db():
  rv=sqlite3.connect(app.config['DATABASE'])
  rv.row_factory=sqlite3.Row
  return rv
def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def get_db():
  if not hasattr(g,'sqlite_db'):
     g.sqlite_db=connect_db()
  return g.sqlite_db



@app.route('/add',methods=['GET','POST'])
@login_required
def add():
  if request.method=='POST':
    if request.form['action']=="add":
      print ("in add")
      print (request)
      print (request.form['regnos'],request.form['name'],request.form['Address'],request.form['age'],request.form['Gender'],request.form['Department'],request.form['Year'])
      db = get_db()
      cur=db.execute('insert into studentdetails(regno,name,Address,age,Gender,department,year) values(?,?,?,?,?,?,?)',[request.form['regnos'],request.form['name'],request.form['Address'],request.form['age'],request.form['Gender'],request.form['Department'],request.form['Year']])
      db.commit()
      flash(' Details added')
  return render_template('add.html')

@app.route('/edit',methods=['GET','POST'])
@login_required
def edit():
  if request.method=='POST':
    if request.form['action']=="edit":
      print ("in edit")
      print (request)
      print (request.form['regno'],request.form['name'],request.form['Address'],request.form['age'],request.form['Gender'],request.form['Department'],request.form['Year'])
      db = get_db()
      cur=db.execute('update studentdetails set name=?,Address=?,age=?,Gender=?,department=?,year=? where regno=?',[request.form['name'],request.form['Address'],request.form['age'],request.form['Gender'],request.form['Department'],request.form['Year'],request.form['regno']])      
      db.commit()
      flash(' Details updated')
  return render_template('Forgot.html')
  
@app.route('/addd',methods=['GET','POST'])
@login_required
def addd():
  if request.method=='POST':
    if request.form['action']=="addd":
      print ("in add")
      print (request)
      print (request.form['regno'],request.form['Semester'],request.form['subject1'],request.form['subject2'],request.form['subject3'],request.form['subject4'],request.form['subject5'],request.form['GPA'])
      db = get_db()
      cur=db.execute('insert into students(regno,sem,subject1,subject2,subject3,subject4,subject5,GPA) values(?,?,?,?,?,?,?,?)',[request.form['regno'],request.form['Semester'],request.form['subject1'],request.form['subject2'],request.form['subject3'],request.form['subject4'],request.form['subject5'],request.form['GPA']])
      db.commit()
      flash(' Details added')
  return render_template('addmark.html')
@app.route('/forgott',methods=['GET','POST'])
@login_required
def editt():
  if request.method=='POST':
    if request.form['action']=="edit":
      print ("in edit")
      print (request)
      print (request.form['regno'],request.form['Semester'],request.form['subject1'],request.form['subject2'],request.form['subject3'],request.form['subject4'],request.form['subject5'],request.form['GPA'])
      db = get_db()
      cur=db.execute('update students set sem=?,subject1=?,subject2=?,subject3=?,subject4=?,subject5=?,GPA=? where regno=?',[request.form['Semester'],request.form['subject1'],request.form['subject2'],request.form['subject3'],request.form['subject4'],request.form['subject5'],request.form['GPA'],request.form['regno']])
      db.commit()
      flash(' Details updated')
  return render_template('editt.html')

@app.route('/view',methods=['GET','POST'])
@login_required
def view():
      
     db = get_db()
     cur = db.execute('SELECT * from studentdetails,students where studentdetails.regno=students.regno;')
     entries = cur.fetchall()
     return render_template('view.html', entries=entries)

     
   
	  
	   
@app.route('/search',methods=['GET','POST'])
@login_required
def search():
	
	if request.method=='POST':
		if request.form['search']=="SEARCH":
		  db=get_db()
		  cur=db.execute('select * from students,studentdetails where studentdetails.regno = ? collate nocase', (request.form['regno']))
		  entries=cur.fetchall()
		  return render_template('view.html', entries=entries)
	return render_template('search.html')


@app.route('/delete',methods=['GET','POST'])
@login_required
def delete():
    if request.method=='POST':
        if request.form['delete']=="delete":
            print ("haaaaaaaaaaai")
            print (request.form['regno'])
            db=get_db()
            cur=db.execute('delete from studentdetails where regno = ? ', (request.form['regno'],) )		
            cur=db.execute('delete from students where regno = ? ', (request.form['regno'],) )		
            db.commit()
            flash('Sucessfully Deleted')
    return render_template('delete.html')

@app.route('/',methods=['GET','POST'])
def home():
  if request.method=='POST':
    if request.form['opt']=="LOGIN":
      return redirect(url_for('login'))
    if request.form['opt']=="LOGOUT":
      return redirect(url_for('logout'))
  return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if 'logged_in' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username_form  = request.form['username']
        password_form  = request.form['password']
        db=sqlite3.connect(app.config['DATABASE'])
        cur = db.cursor()
        cur.execute("SELECT COUNT(1) FROM users WHERE name = ?", [username_form]) # CHECKS IF USERNAME EXSIST
        if cur.fetchone()[0]:
            cur.execute("SELECT pass FROM users WHERE name = ?", [username_form]) # FETCH THE HASHED PASSWORD
            for row in cur.fetchall():
                #if md5(password_form).hexdigest() == row[0]:
                if password_form == row[0]:
                    session['logged_in'] = True
                    flash('You were logged in')
                    return redirect(url_for('home'))
                else:
                    error ='invalid username or password'
        else:
            error = 'invalid username or password'
    return render_template('login.html', error=error)

@app.route('/added',methods=['GET','POST'])
@login_required
def added():
  if request.method=='POST':
    if request.form['action']=="Report":
      print ("in add")
      print (request)
      print (request.form['Department'],request.form['Year'],request.form['Semester'],request.form['Filter'],request.form['Sort'])
      if request.form['Filter']=='GPA':
        if request.form['Sort']=='High':
          db = get_db()
          cur = db.execute('SELECT studentdetails.regno,students.regno,name,Department,year,sem,subject1,subject2,subject3,subject4,subject5,GPA FROM students , studentdetails WHERE studentdetails.regno=students.regno AND studentdetails.Department="MCA" AND students.sem =4  AND studentdetails.year=2 ORDER by GPA DESC;')
          entries=cur.fetchall()
          return render_template('view.html', entries=entries)
        elif request.form['Sort']=='Pass':
          db = get_db()
          cur = db.execute('SELECT studentdetails.regno,students.regno,name,Department,year,sem,subject1,subject2,subject3,subject4,subject5,GPA FROM students , studentdetails WHERE studentdetails.regno=students.regno AND studentdetails.Department="MCA" AND students.sem =4 AND students.GPA >= 50 AND studentdetails.year=2;')
          entries=cur.fetchall()
          return render_template('view.html', entries=entries)
        elif request.form['Sort']=='Arrear':
          db = get_db()
          cur = db.execute('SELECT studentdetails.regno,students.regno,name,Department,year,sem,subject1,subject2,subject3,subject4,subject5,GPA FROM students , studentdetails WHERE studentdetails.regno=students.regno AND studentdetails.Department="MCA" AND students.sem =4 AND students.GPA < 50 AND studentdetails.year=2;')
          entries=cur.fetchall()
          return render_template('view.html', entries=entries)
      elif request.form['Filter']=='subject1':
        if request.form['Sort']=='High':
          db = get_db()
          cur = db.execute('SELECT studentdetails.regno,students.regno,name,Department,year,sem,subject1 FROM students , studentdetails WHERE studentdetails.regno=students.regno AND studentdetails.Department="MCA" AND students.sem =4 AND studentdetails.year=2 ORDER by subject1 DESC')
          entries=cur.fetchall()
          return render_template('view.html', entries=entries)
        elif request.form['Sort']=='Pass':
          db = get_db()
          cur = db.execute('SELECT studentdetails.regno,students.regno,name,Department,year,sem,subject1 FROM students , studentdetails WHERE studentdetails.regno=students.regno AND studentdetails.Department="MCA" AND students.sem =4 AND students.subject1 >=50 AND studentdetails.year=2;')
          entries=cur.fetchall()
          return render_template('view.html', entries=entries)
        elif request.form['Sort']=='Arrear':
          db = get_db()
          cur = db.execute('SELECT studentdetails.regno,students.regno,name,Department,year,sem,subject1 FROM students , studentdetails WHERE studentdetails.regno=students.regno AND studentdetails.Department="MCA" AND students.sem =4 AND students.subject1 <50 AND studentdetails.year=2;')
          entries=cur.fetchall()
          return render_template('view.html', entries=entries)
      elif request.form['Filter']=='subject2':
        if request.form['Sort']=='High':
          db = get_db()
          cur = db.execute('SELECT studentdetails.regno,students.regno,name,Department,year,sem,subject2 FROM students , studentdetails WHERE studentdetails.regno=students.regno AND studentdetails.Department="MCA" AND students.sem =4 AND studentdetails.year=2 ORDER by subject2 DESC;')
          entries=cur.fetchall()
          return render_template('view.html', entries=entries)
        elif request.form['Sort']=='Pass':
          db = get_db()
          cur = db.execute('SELECT studentdetails.regno,students.regno,name,Department,year,sem,subject2 FROM students , studentdetails WHERE studentdetails.regno=students.regno AND studentdetails.Department="MCA" AND students.sem =4 AND students.subject2 >=50 AND studentdetails.year=2;')
          entries=cur.fetchall()
          return render_template('view.html', entries=entries)
        elif request.form['Sort']=='Arrear':
          db = get_db()
          cur = db.execute('SELECT studentdetails.regno,students.regno,name,Department,year,sem,subject2 FROM students , studentdetails WHERE studentdetails.regno=students.regno AND studentdetails.Department="MCA" AND students.sem =4 AND students.subject2 <50 AND studentdetails.year=2;')
          entries=cur.fetchall()
          return render_template('view.html', entries=entries)
      elif request.form['Filter']=='subject3':
        if request.form['Sort']=='High':
          db = get_db()
          cur = db.execute('SELECT studentdetails.regno,students.regno,name,Department,year,sem,subject3 FROM students , studentdetails WHERE studentdetails.regno=students.regno AND studentdetails.Department="MCA" AND students.sem =4 AND studentdetails.year=2 ORDER by subject3 DESC;')
          entries=cur.fetchall()
          return render_template('view.html', entries=entries)
        elif request.form['Sort']=='Pass':
          db = get_db()
          cur = db.execute('SELECT studentdetails.regno,students.regno,name,Department,year,sem,subject3 FROM students , studentdetails WHERE studentdetails.regno=students.regno AND studentdetails.Department="MCA" AND students.sem =4 AND students.subject3 >=50 AND studentdetails.year=2;')
          entries=cur.fetchall()
          return render_template('view.html', entries=entries)
        elif request.form['Sort']=='Arrear':
          db = get_db()
          cur = db.execute('SELECT studentdetails.regno,students.regno,name,Department,year,sem,subject3 FROM students , studentdetails WHERE studentdetails.regno=students.regno AND studentdetails.Department="MCA" AND students.sem =4 AND students.subject3 <50 AND studentdetails.year=2;')
          entries=cur.fetchall()
          return render_template('view.html', entries=entries)
      elif request.form['Filter']=='subject4':
        if request.form['Sort']=='High':
          db = get_db()
          cur = db.execute('SELECT studentdetails.regno,students.regno,name,Department,year,sem,subject4 FROM students , studentdetails WHERE studentdetails.regno=students.regno AND studentdetails.Department="MCA" AND students.sem =4 AND studentdetails.year=2 ORDER by subject4 DESC;')
          entries=cur.fetchall()
          return render_template('view.html', entries=entries)
        elif request.form['Sort']=='Pass':
          db = get_db()
          cur = db.execute('SELECT studentdetails.regno,students.regno,name,Department,year,sem,subject4 FROM students , studentdetails WHERE studentdetails.regno=students.regno AND studentdetails.Department="MCA" AND students.sem =4 AND students.subject4 >=50 AND studentdetails.year=2;')
          entries=cur.fetchall()
          return render_template('view.html', entries=entries)
        elif request.form['Sort']=='Arrear':
          db = get_db()
          cur = db.execute('SELECT studentdetails.regno,students.regno,name,Department,year,sem,subject4 FROM students , studentdetails WHERE studentdetails.regno=students.regno AND studentdetails.Department="MCA" AND students.sem =4 AND students.subject4 <50 AND studentdetails.year=2;')
          entries=cur.fetchall()
          return render_template('view.html', entries=entries)
      elif request.form['Filter']=='subject5':
        if request.form['Sort']=='High':
          db = get_db()
          cur = db.execute('SELECT studentdetails.regno,students.regno,name,Department,year,sem,subject5 FROM students , studentdetails WHERE studentdetails.regno=students.regno AND studentdetails.Department="MCA" AND students.sem =4 AND studentdetails.year=2 ORDER by subject5 DESC;')
          entries=cur.fetchall()
          return render_template('view.html', entries=entries)
        elif request.form['Sort']=='Pass':
          db = get_db()
          cur = db.execute('SELECT studentdetails.regno,students.regno,name,Department,year,sem,subject5 FROM students , studentdetails WHERE studentdetails.regno=students.regno AND studentdetails.Department="MCA" AND students.sem =4 AND students.subject5 >=50 AND studentdetails.year=2;')
          entries=cur.fetchall()
          return render_template('view.html', entries=entries)
        elif request.form['Sort']=='Arrear':
          db = get_db()
          cur = db.execute('SELECT studentdetails.regno,students.regno,name,Department,year,sem,subject5 FROM students , studentdetails WHERE studentdetails.regno=students.regno AND studentdetails.Department="MCA" AND students.sem =4 AND students.subject5 <50 AND studentdetails.year=2;')
          entries=cur.fetchall()
          return render_template('view.html', entries=entries)
      flash(' Details added')
  return render_template('rep.html')
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash(' You were logged out')
    return redirect(url_for('home'))

@app.teardown_appcontext
def close_db(error):
  if hasattr(g,'sqlite_db'):
     g.sqlite_db.close()



if __name__=='__main__':
 app.run(debug=True)
