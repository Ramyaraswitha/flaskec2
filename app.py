from flask import Flask,render_template,redirect,url_for,request,flash
import mysql.connector

app=Flask(__name__)
app.secret_key="something"

conn=mysql.connector.connect(
    host="localhost",
    username="root",
    password="Ram@1997",
    database="flaskdb"
)
cursor=conn.cursor()

@app.route('/')
def index():
    cursor.execute("select * from users")
    res=cursor.fetchall()
    return render_template('index.html',data=res)

@app.route('/add',methods=['POST','GET'])
def add():
    if request.method=='POST':
        title=request.form['title']
        author=request.form['author']
        price=request.form['price']
        cursor.execute("insert into users (Title,Author,Price) values(%s,%s,%s)",(title,author,price))
        conn.commit()
        flash("Book Added Successfully","success")
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/update',methods=['POST','GET'])
def update():
    if request.method=='POST':
        id_data=request.form['id']
        title=request.form['title']
        author=request.form['author']
        price=request.form['price']
        cursor.execute("""
             update users
             set Title=%s, Author=%s, Price=%s
             where id=%s                    
                       """,(title,author,price,id_data))
        flash("Book Updated Successfully","success")
        conn.commit()
        return redirect(url_for('index'))
    return render_template('index.html')   

@app.route('/delete/<string:id_data>',methods=['POST','GET'])
def delete(id_data):
    cursor.execute("delete from users where id=%s",(id_data,))
    conn.commit()
    flash("Book deleted Successfully","danger")
    return redirect(url_for('index'))




if __name__=='__main__':
    app.run(debug=True)