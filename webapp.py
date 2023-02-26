from flask import Flask
from flask import render_template
from flask import request

from cookbook import Cookbook
app = Flask(__name__)
cb =  Cookbook()

@app.route('/',methods=["GET","POST"])
def home():
    effects = cb.AllEffects()
    
    if request.method == "GET":
        active_effect = ""
        ingredients = cb.AllIngredients()
    else:
        active_effect = [request.form["effect"]]
        ingredients = cb.GetIngredients(active_effect)

    return render_template("index.html", effects=effects, ingredients=ingredients, active_effect=active_effect )


if __name__ == "__main__":
    app.run(debug=True)