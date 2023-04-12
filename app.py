from flask import Flask, render_template
from flask import request, jsonify
from flask import Response, stream_with_context
from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask import Blueprint, render_template
from replit import db, Database
from passlib.hash import sha256_crypt
import os
from google.cloud import vision
from google.cloud import vision_v1
import openai
import base64
import io
import cgi

formData = cgi.FieldStorage()



app = Flask(__name__)
openai.api_key = "replace with api key"
non_food = ", and ignore every single one of the non food items and dont even try to incorporate them into the food or the recipe, also generate all nutritonal info."
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'yourjsonfile.json'

client = vision.ImageAnnotatorClient()
image = vision_v1.types.Image()
mime_type = 'image/jpeg'



db = Database(db_url="https://kv.replit.com/v0/eyJhbGciOiJIUzUxMiIsImlzcyI6ImNvbm1hbiIsImtpZCI6InByb2Q6MSIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjb25tYW4iLCJleHAiOjE2ODExMDEwNzYsImlhdCI6MTY4MDk4OTQ3NiwiZGF0YWJhc2VfaWQiOiI5OTA4MzViYS1hMzUyLTQzMmQtYjAxOS0zYWI3ODc1YmE1ODgiLCJ1c2VyIjoiQzBEM1cxWiIsInNsdWciOiJEYXRhYmFzZUZvcktyaXNoYXkifQ.chsSX6Xgy7xRalCsuKst8MkaZVEyz4tRj19KkY_pIc-0Hu1MqO_V7LI2KPCJAi7gtp7rKAaarAYTZMOT7LBYiA")

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login():
  loggedIn = request.cookies.get("loggedIn")
  if loggedIn == "true":
    return redirect("/dashboard") 
  else:
    return render_template("login.html")

@app.route("/signup")
def signup():
  loggedIn = request.cookies.get("loggedIn")
  if loggedIn == "true":
    return redirect("/dashboard")
  else:
    return render_template("signup.html")
@app.route("/loginsubmit", methods=["GET", "POST"])
def loginsubmit():
  if request.method == "POST":
    username = request.form.get("username")
    password = request.form.get("password")
    if username in db.keys():
      if sha256_crypt.verify(password, db[username]) == True:
        resp = make_response(render_template('readcookie.html'))
        resp.set_cookie("loggedIn", "true")
        resp.set_cookie("username", username)
        return resp
      else:
        return render_template("error.html", error="Incorrect Password, please try again.")
    else:
      return render_template("error.html", error="Account does not exist, please sign up.")

@app.route("/createaccount", methods=["GET", "POST"])
def createaccount():
  if request.method == "POST":
    newusername = request.form.get("newusername")
    newpassword = sha256_crypt.encrypt((request.form.get("newpassword")))
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    cap_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    allchars = letters + cap_letters + numbers + ['_']
    print(newusername)
    for i in newusername:
      if i not in allchars:
        return "Username can only contain alphanumeric characters and underscores."
    if newusername in db.keys():
      return "Username taken."
    if newusername == "":
      return "Please enter a username."
    if newpassword == "":
      return "Please enter a password."
    db[newusername] = newpassword
    db[newusername+"stat"] = "user"
    resp = make_response(render_template('readcookie.html'))
    resp.set_cookie("loggedIn", "true")
    resp.set_cookie("username", newusername)
    return resp

@app.route("/logout")
def logout():
  resp = make_response(render_template('readcookie.html'))
  resp.set_cookie("loggedIn", "false")
  resp.set_cookie("username", "None")
  return resp

@app.route("/dashboard")
def dashboard():
  loggedIn = request.cookies.get("loggedIn")
  username = request.cookies.get("username")

  if loggedIn == "true":
    if username != None and username in db.keys():
        return render_template("dashboard.html", loggedIn = loggedIn, username = username)
  else:
    return redirect("/")

@app.route("/mealtype")
def getstarted():
    return render_template("mealtype.html")

@app.route("/uploadimage")
def uploadimage():
    return render_template("uploadimage.html")

@app.route("/index")
def index():
    return render_template("index.html")

def encode_image(image_path):
    with open(image_path, "rb") as f:
        image_content = f.read()
        return base64.b64encode(image_content)

def download_image_from_data_uri(data_uri, output_file_path):
    # Remove the "data:image/*;base64," prefix from the data URI
    base64_image = data_uri.split(",")[1]

    # Decode the base64-encoded image data
    image_data = base64.b64decode(base64_image)

    # Save the image data to a file
    with io.open(output_file_path, "wb") as file:
        file.write(image_data)




@app.route('/upload_image', methods=['POST'])
def upload_image():
    global food_list
    food_list = []
    # Get the image data from the POST request
    url = request.json.get('url')
    print(url, end="\n\n\n\n\n")

    # Set the image URI in the Vision API client
    image.source.image_uri = url

    # Label detection
    response_object = client.object_localization(image=image)
    for obj in response_object.localized_object_annotations:
        food_list.append(obj.name)

    # Text detection
    response_text = client.text_detection(image=image)
    for r in response_text.text_annotations:
        d = r.description
        food_list.append(d)

    print(food_list)


    # Return a response indicating that the image was processed successfully
    return 'Image processed successfully'

@app.route('/generate_recipe', methods=['POST'])
def generate_recipe():
    global output, final_recipe
    cuisine = request.values['cuisine']
    mealtype = request.values['mealtype']
    print(cuisine)
    print(mealtype)

    if cuisine == "any":
        cuisine = ""
    if mealtype.lower() == "any":
        mealtype = "meal"
    
    prompt = f"Make me a {cuisine} {mealtype} with "
    # Combine all the items in the food_list into a single string
    food_string = ', '.join(food_list)

    # Concatenate the food_string with the prompt
    prompt += food_string
    prompt += non_food
    print(prompt)
    output = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[{"role": "user", "content": 
                prompt}]
    )

    # Get the output text only
    final_recipe = output['choices'][0]['message']['content']
    print(final_recipe)
    
    # Redirect to the recipe page
    return redirect(url_for('recipe'))

@app.route('/recipe', methods=['POST', 'GET'])
def recipe():
    global final_recipe
    return render_template("recipe.html", recipe=final_recipe)
   
keys = db.keys()
print(keys)

if __name__ == "__main__":
    app.run(debug=True)

# cuisine = "all"
#     mealtype = "for breakfast"

#     if cuisine == "all":
#         cuisine = ""

#     if mealtype == "all":
#         mealtype = ""

#     prompt = f"Make me a {cuisine} {mealtype} with "
#     # Combine all the items in the food_list into a single string
#     food_string = ', '.join(food_list)

#     # Concatenate the food_string with the prompt
#     prompt += food_string
#     prompt += non_food
#     print(prompt)
#     output = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo", 
#     messages=[{"role": "user", "content": 
#                 prompt}]
#     )

#     # Get the output text only
#     print(output['choices'][0]['message']['content'])

#     # Process the image data here
