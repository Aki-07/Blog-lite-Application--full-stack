from flask import Flask , render_template , request , redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy

import os

import datetime

app = Flask(__name__) #instantiation only takes name parameter



app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///MAD.sqlite3"
db = SQLAlchemy()


db.init_app(app)



app.app_context().push()  

class User(db.Model):
    userid = db.Column(db.Integer , primary_key = True , nullable= False , autoincrement = True)
    username = db.Column(db.String , unique = True , nullable= False)
    password = db.Column(db.String , nullable = False)
    Age = db.Column(db.Integer , nullable  = False)
    email = db.Column(db.String)
    Image = db.Column(db.String)
    no_of_posts = db.Column(db.Integer , default = 0  , nullable = False)
    post = db.relationship('Posttable' , backref  = "user")
    comme = db.relationship('Comment' , backref = 'user')
    fole = db.relationship('Follow' , backref = 'user')



   

class Posttable(db.Model):
    #one to many relationship one user can have multiple posts
    post_id = db.Column(db.Integer , primary_key  = True , autoincrement = True  , nullable = False )
    username_post = db.Column(db.String , db.ForeignKey("user.username"))
    title  = db.Column(db.String , nullable = False)
    description = db.Column(db.String  , nullable = False)
    image = db.Column(db.String)
    timestamp  = db.Column(db.DateTime , nullable = False)
    likes = db.Column(db.Integer , default = 0  , nullable = False)
    dislikes = db.Column(db.Integer , default = 0  , nullable = False)
    comments = db.Column(db.String , nullable = False)
    comm = db.relationship('Comment' , backref = 'posttable')
    fol = db.relationship('Follow' , backref = 'posttable')


class Comment(db.Model):
   
    comment_id = db.Column(db.Integer, primary_key=True , autoincrement = True , nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey("posttable.post_id"), nullable=False)
    username= db.Column(db.String, db.ForeignKey("user.username"), nullable = False)
    timestamp = db.Column(db.DateTime, nullable= False)
    comment = db.Column(db.String, nullable = False)

class Follow(db.Model):
    follow_id = db.Column(db.Integer, primary_key=True , autoincrement =True)
    following = db.Column(db.String, db.ForeignKey("user.username"), nullable = False )
    follower = db.Column(db.String, db.ForeignKey("posttable.username_post"), nullable = False)
    timestamp = db.Column(db.DateTime, nullable= False)



@app.route('/' , methods = ['POST' , 'GET']) # verum slash nu pota that is the default one
def index():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password  = request.form['password']
        name = username
        ##FIRST IS FOR THE SIGNIN PAGEEE
        
        if password == '':
            return "<h2> Please Enter Your Password <a href='/'>Back</h2></a>"
        else:
            result = db.session.query(User).filter(User.username == username ).first()
            passw= db.session.query(User).filter(User.password == password).first()
            image = db.session.query(User.Image).filter(User.username == username).first()
            image = image[0]
            posts = db.session.query(User.no_of_posts).filter(User.username == username).first()
            posts = posts[0]
           
            
            
            follow = Follow.query.filter(Follow.follower == name).order_by(Follow.timestamp.desc()).all()
            print(follow)
            users = []
            for elem in follow:
                elem = elem.following
                print(elem)
                if elem == []:
                    continue
                else:
                    s = Posttable.query.filter(Posttable.username_post == elem).all()
                    print(s)
                    for item in s[::-1]:
                        users.append(item)
                    print(users)
       
            
    
            print(users)

            if result and passw is None:

                return render_template('signup.html')
            else:
                comm = Comment.query.filter(Comment.username == username ).all()
                return render_template('homepage.html' , pic = image , user = name , blogs = users, comments = comm , users = users)
   
@app.route('/login/<username>' , methods = ['POST' , 'GET']) # verum slash nu pota that is the default one
def login(username):
    if request.method == "GET":
        name = username
        result = db.session.query(User).filter(User.username == username ).first()
        image = db.session.query(User.Image).filter(User.username == username).first()
        image = image[0]
        posts = db.session.query(User.no_of_posts).filter(User.username == username).first()
        posts = posts[0]
        print(name)
        follow = Follow.query.filter(Follow.follower == name).order_by(Follow.timestamp.desc()).all()
        print(follow)
        users = []
        for elem in follow:
            elem = elem.following
            print(elem)
            if elem == []:
                continue
            else:
                s = Posttable.query.filter(Posttable.username_post == elem).all()
                print(s)
                for item in s[::-1]:
                    users.append(item)
                print(users)
        print(users)
        print("-------------------------")
    
        like = Posttable.query.filter(Posttable.username_post != username).first()
     
        comm = Comment.query.filter(Comment.username == username ).all()
        print(comm)
        return render_template('homepage.html' , pic = image , user = username , blogs = users, comments = comm , users = users )

    




@app.route('/myprofile/<username>' , methods = ['GET','POST'])
def myprofile(username):
    image = db.session.query(User.Image).filter(User.username == username).first()
    print(image)
    image = image[0]
    print(image)
        
    posts = db.session.query(User.no_of_posts).filter(User.username == username).first()
    posts = posts[0]
    fol  = Follow.query.filter(Follow.follower == username).count()
    print(fol)
    folw = Follow.query.filter(Follow.following == username).count()
    
    if request.method == 'GET':
        

        return render_template('profile.html' ,pic = image, user = username, name= username , posts = posts , following = fol , followers = folw )
    



@app.route('/signup.html')
def register():
    return render_template('signup.html')

@app.route('/search/<user>', methods=[ "GET" , "POST"])
def search(user):
    if request.method == "POST":
        name = user
        search = request.form["search"]
        users = User.query.filter(User.username.like('%'+search+'%')).first()
        label = users.username
        image = db.session.query(User.Image).filter(User.username == name).first()
        image = image[0]
        blogs = Posttable.query.filter(Posttable.username_post == label).all()

        return render_template("readblog.html", user=name, pic = image , blogs =  blogs  , label = label)



@app.route('/myprofile/<username>/homepage.html')
def move(username):
        image = db.session.query(User.Image).filter(User.username == username).first()
        image = image[0]
        print(image)
        name = username
        blogs = Posttable.query.filter(Posttable.username_post != username).all()
       
        return redirect(url_for('login' , username = username))

@app.route('/unfollow/<user>/<label>', methods=["GET"])
def unfollow(user , label):
    flag =0
    name = user
    want = label
    print(name)
    print(want)
    
    fol =  db.session.query(Follow).filter(Follow.follower == name and Follow.following == want).all()
    print(fol)


    for elem in fol:
        if(elem.follower == name and elem.following == want):
            result = elem
    print(result)
    db.session.delete(result)
    db.session.commit()
    return redirect(url_for('move' , username= name))


@app.route('/follow/<user>/<label>', methods=["GET"])
def follow(user , label):
        flag =0
        name = user
        want = label
        print(name)
        print(want)
        follower_id  = db.session.query(User.username).filter(User.username == name).first()
        print(follower_id)
        following_id  = db.session.query(User.username).filter(User.username == want).first()
        print(following_id)
        fo = db.session.query(Follow.following).filter(Follow.follower == name).all()
        print(fo)
        for elem in fo:
            elem = elem[0]
            print(elem)
            if(elem == following_id[0]) :
                flag = 1
        if flag ==1:
            return redirect(url_for('move' , username= name))
        
        else:
            fol = Follow(
                following = following_id[0],
                follower = follower_id[0],
                timestamp = datetime.datetime.now()
            )
            
            db.session.add(fol)
            db.session.commit()
            return redirect(url_for('move' , username= name))


@app.route('/addblog.html/<username>' ,  methods = ['POST' , 'GET'])
def add(username):
    if request.method == "GET":
        name = username
        image = db.session.query(User.Image).filter(User.username == username).first()
        image = image[0]
        print(image)
        return render_template('addblog.html'  , pic = image , user = name )
    if request.method == "POST":
        picture = request.files['Image_add']
        pic = 'static/pro_pic/' + picture.filename
        picture.save(pic)
        posts = db.session.query(User.no_of_posts).filter(User.username == username).first()
        print(username)
        
        posts = posts[0]
      
        posts = posts+1
      
        post = Posttable(

            username_post = username,
            title = request.form['title'],
            description = request.form['description'],
            image = pic,
            timestamp = datetime.datetime.now(),
            comments = ""
        )
        
        user = User.query.filter_by(username =username).first()
        user.no_of_posts += 1
        db.session.add(post)
        local_object = db.session.merge(user)
        db.session.add(local_object)

        # db_session.add(user)
        db.session.commit()
        image = db.session.query(User.Image).filter(User.username == username).first()
        image = image[0]
        name = username
       

        return redirect(url_for('myprofile' , username = username))


@app.route('/deleteblog.html/<username>' ,  methods = ['POST' , 'GET'])
def delete(username):
    if request.method == "GET":
        name = username
        image = db.session.query(User.Image).filter(User.username == username).first()
        image = image[0]
       
        posts = Posttable.query.filter_by( username_post = username).all()
        return render_template('deleteblog.html' , pic = image , user = name ,posts = posts)

@app.route('/delete/<post_id>/<username>' ,  methods = ['POST' , 'GET'])
def deblog(post_id , username):
    if request.method == "GET": 
        number = post_id
        name = username
        return render_template('deleteconfirm.html', user = name ,  postid = number)


@app.route('/delete/<post_id>/<username>/YES' ,  methods = ['POST' , 'GET']) 
def dblog(post_id , username):
    number = post_id
    name = username
    pos = Posttable.query.filter_by(post_id = number).first()
    user = User.query.filter_by(username =username).first()
    user.no_of_posts -=1
    print(user.no_of_posts)
    local_object1 = db.session.merge(pos)
    db.session.delete(local_object1)
    local_object = db.session.merge(user)
    db.session.add(local_object)
    db.session.commit()
    return redirect(url_for('delete' , username = username))

    
@app.route('/delete/<post_id>/<username>/NO' ,  methods = ['POST' , 'GET']) 
def Nodel(post_id , username):
    return redirect(url_for('delete' , username = username))




@app.route('/editblog.html/<username>' ,  methods = ['POST' , 'GET'])
def edit(username):
    if request.method == "GET":
        name = username
        image = db.session.query(User.Image).filter(User.username == username).first()
        image = image[0]
        
        posts = Posttable.query.filter_by( username_post = username).all()
        return render_template('editblog.html' , pic = image , user = name ,posts = posts)


@app.route('/edit/<post_id>/<username>' ,  methods = ['POST' , 'GET'])
def editful(post_id,username):
    if request.method == "GET":
        name = username
        number  = post_id
        print(number)
        image = db.session.query(User.Image).filter(User.username == username).first()
        image = image[0]
        
        posts = Posttable.query.filter_by(post_id = number).first()
        print(posts.post_id)
        o = posts.image
        o = o[15:]
        return render_template('editfull.html' , pic = image , user = name ,posts = posts , img = o , post_id = number)



@app.route('/editdone/<post_id>/<username>' ,  methods = ['POST' , 'GET'])
def editdone(post_id , username):
    if request.method == "POST":
        print("dfdf")
        picture = request.files['Image_add']
        number = post_id
        pic = 'static/pro_pic/' + picture.filename
        picture.save(pic)
        print("dfdf")
        posts = db.session.query(User.no_of_posts).filter(User.username == username).first()
        posts = posts[0]
        

        
        title = request.form['title']
        description = request.form['description']
        image = pic

        post = Posttable.query.filter(Posttable.post_id == number).first()
        print(post)
        post.title = title
        post.description = description
        post.image = image
            
        local_object = db.session.merge(post)
        db.session.add(local_object)
        db.session.commit()
        image = db.session.query(User.Image).filter(User.username == username).first()
        image = image[0]
        name = username
        posts = Posttable.query.filter_by( username_post = username).all()
        return redirect(url_for('edit' ,  username = name))


@app.route('/<post_id>/<user>/like' ,  methods = ['POST' , 'GET'])
def like(post_id , user):
    blogs = Posttable.query.filter_by(post_id = post_id).first()
    name = user
    print(name)
    username  = db.session.query(Posttable.username_post).filter(Posttable.post_id == post_id).first()
    blogs.likes+=1
    username = username[0]
    local_object = db.session.merge(blogs)
    db.session.add(local_object)
    db.session.commit()
    image = db.session.query(User.Image).filter(User.username == name).first()
    image = image[0]
    print(name)

    blogs = Posttable.query.filter(Posttable.username_post != name).all()
    return redirect(url_for('move' , username  = user))

@app.route('/<post_id>/<user>/dislike' ,  methods = ['POST' , 'GET'])
def dislike(post_id , user):
    blogs = Posttable.query.filter_by(post_id = post_id).first()
    name = user
    print(name)
    username  = db.session.query(Posttable.username_post).filter(Posttable.post_id == post_id).first()
    blogs.dislikes+=1
    username = username[0]
    local_object = db.session.merge(blogs)
    db.session.add(local_object)
    db.session.commit()
    image = db.session.query(User.Image).filter(User.username == name).first()
    image = image[0]
    print(name)

    blogs = Posttable.query.filter(Posttable.username_post != name).all()
    return redirect(url_for('move' , username  = user))

@app.route('/edituser/<user>' , methods  = ["GET" , "POST"])
def edituser(user):
    if request.method == "GET":
        u = User.query.filter(User.username == user).first()
        pas = u.password
        mail = u.email
        a = u.Age
        return render_template("edituser.html" , pas = pas , mail = mail , a = a , user = user)
    elif request.method == "POST":
        u = User.query.filter(User.username == user).first()
        print(user)
        u.password = request.form['password']
        u.email = request.form['mail']
        u.Age = request.form['age']
        picture = request.files["Image_add"]
        ol = picture.filename
        
        pic = 'static/pro_pic/' + ol
        u.Image = pic

     
        db.session.commit()
        return redirect(url_for('myprofile' , username = user))

        
        a = user.Age
@app.route('/comments/<user>/<post_id>' , methods  = ["GET" , "POST"])
def comment(user  , post_id):
    name = user
    number= post_id
    image = db.session.query(User.Image).filter(User.username == name).first()
    image = image[0]
    if(request.method == "GET"):
        return render_template('comments.html' , pic = image, user = name  , postid = number )
    if request.method == "POST":
        com = request.form['cmt']
        ct = Comment(
            post_id = number , 
            username = name,
            timestamp = datetime.datetime.now(),
            comment = com
        )
        db.session.add(ct)
        db.session.commit()
        blogs = Posttable.query.filter(Posttable.username_post != name).all()
        
        return redirect(url_for('move' , username = user))
    

@app.route('/signup' , methods  = ["GET" , "POST"])
def regiser():
    if request.method == "POST":
        image = request.files['image']
        pic = 'static/pro_pic/' + image.filename
        image.save(pic)
        user = User(
            username = request.form["new_username"],
            password = request.form["new_password"],
            Age = request.form["new_age"],
            email = request.form["new_email"],
            Image = pic
            
        )
        db.session.add(user)
        db.session.commit()
        username = User.username
        image = db.session.query(User.Image).filter(User.username == username).first()
        image = image[0]
        
        return render_template('login.html')
    else:
        return render_template('signup.html')






if __name__ == "__main__":
    app.run(debug=True ,   port = 5000)