from flask_restful import Api,Resource
from flask import Flask
from flask_restful import fields, marshal_with
from flask_cors import CORS
from appl import *
from flask import request

api = Api(app)

CORS(app)






class UserApi(Resource):
    # @marshal_with(resource_fields)
    def get(self , username):
        print(username)
        print("-----------------")
        user = db.session.query(User).filter(User.username == username).first()
        print(user)
        if user is None:
            return {"RESULT" : "NOT LOGGED IN USER"}
        else:
            return {"username" : user.username , "email" : user.email}
        

    def post(self ):
        image = request.files['image']
        pic = 'static/pro_pic/' + image.filename
        image.save(pic)
        print(image)
        user = User(
            username = request.form["username"],
            password = request.form["password"],
            Age = request.form["Age"],
            email = request.form["email"],
            Image = pic
            
        )
        db.session.add(user)
        db.session.commit()
        return {"result":"Successfully created" }

        
    def put(self , username):
        image = request.files['image']
        pic = 'static/pro_pic/' + image.filename
        image.save(pic)
        password = request.form["password"],
        Age = request.form["Age"],
        email = request.form["email"],
        Image = pic
        p = User.query.filter(User.username == username).first()
        p.password = password[0]
        p.Age = Age[0]
        p.email = email[0]
        p.Image = Image
        db.session.commit()
        return {"result" : "successfull"}
        


    def delete(self , username):
        user = db.session.query(User).filter(User.username == username).first()
        if user == None:
            return {"result" : "User Not Found"}
        else:
            db.session.delete(user)
            db.session.commit()
            return {"result" : "successfull"}

api.add_resource(UserApi,  "/api/user/<username>" ,"/api/user")

if __name__ == "__main__":
    app.run(debug=True  , port = 3000)
