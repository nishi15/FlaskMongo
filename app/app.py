from flask import Flask,render_template,redirect
from flask_pymongo import PyMongo
from flask import request
import datetime,json
from bson.objectid import ObjectId

from pymongo import MongoClient

# setting app variable
app = Flask(__name__)

# setting up MongoClient connection variable
client = MongoClient('localhost', 27017)

# db used
db = client.flaskAPI_Mongo


@app.route("/")
def home():


    # get the notes from the database
    notes = list(db.notes.find({}).sort("createdAt",-1))
    print(notes)

    # render a view
    return render_template("/home.html",homeIsActive=True,addNoteIsActive=False,notes=notes)


@app.route("/add-note",methods=["GET","POST"])
def add_notes():

	# if get request then return the empty form
	if request.method == "GET":
		return render_template("/add-note.html",homeIsActive=False,addNoteIsActive=True)
	
	# if post request then submit the form to db collection
	elif request.method == "POST":
		print(request.form)
		
		# getting details from request
		title = request.form.get("title").strip()
		description = request.form.get("description").strip()
		createdAt = datetime.datetime.now()

		# inserting record into the db
		db.notes.insert_one({"title":title,"description":description,"createdAt":createdAt})

		# directing to home page which will eventually list up all notes
		return redirect("/")
	
	else:
		return json.dumps({"mssg":"Wrong Method"})



@app.route("/edit-note",methods=["GET","POST"])
def edit_note():

	if request.method == "GET":

		# from home.html (get request /edit-note?nid=<6aab3qe3>)
		note_id = request.args.get("nid")

		# get the note details from the db
		note = dict(db.notes.find_one({"_id":ObjectId(note_id)}))

		print(note)

		# direct to edit note page
		return render_template('edit-note.html',note=note)


	elif request.method == "POST":
		
		#get the data of the note
		noteId = request.form['_id']
		title = request.form['title'].strip()
		description = request.form['description'].strip()

		# update the data in the db
		db.notes.update_one({"_id":ObjectId(noteId)},{"$set":{"title":title,"description":description}})

		# redirect to home page
		return redirect("/")

	else:
		return json.dumps({"mssg":"Wrong Method"})


@app.route('/delete-note',methods=["POST"])
def delete_note():

	# getting the noteid from "form" in home.html
	note_id = request.form.get("nid")

	# delete note from collection
	db.notes.delete_one({"_id":ObjectId(note_id)})

	# direct to home page
	return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)