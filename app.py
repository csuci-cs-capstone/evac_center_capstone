from flask import Flask, render_template
from templates import create_app

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route("/")
def index():
    return render_template ('index.html')

@app.route("/new_user")
def new_user():
    return render_template ('new-user.html')

@app.route("/dashboard")
def dashboard():
    return render_template ('dashboard.html')

#####
#@app.route("/calamity_type")
#def calamity_type():
  #  return render_template ('calamaity-type.html')

#@app.route("/evacuation_center")
#def evacuation_center():
#    return render_template ('evacuation-center.html')

# mutliple routing? - related to evacuee information
#@app.route("/add_evacuees")
#def add_evacuees():
#    return render_template ('add-evacuees.html')

#multiple routing? - related to evacuee information
#@app.route("/manage_evacuees")
#def manage_evacuees():
#    return render_template ('manage-evacuees.html')

# mutliple routing? - related to Users
#@app.route("/add_user")
#def add_user():
#    return render_template ('add-user.html')

#multiple routing? - related to Users
#@app.route("/manage_user")
#def manage_user():
#    return render_template ('manage-user.html')

if __name__ == "__main__":
    app.run(debug=True)