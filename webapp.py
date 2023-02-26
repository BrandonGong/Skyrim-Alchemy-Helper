from flask import Flask, render_template, request, redirect, url_for
from cookbook import Cookbook

app = Flask(__name__)
cb =  Cookbook()

active_effects = []

@app.route('/')
def Home():
    effects = []
    for effect in cb.AllEffects():
        e = {}
        e["name"] = effect
        e["active"] = effect in active_effects
        effects.append(e)
    
    if len(active_effects) == 0:
        ingredients = None
    else:
        ingredients = cb.GetIngredients(active_effects)

    return render_template("index.html", effects=effects, ingredients=ingredients, active_effect=active_effects )

@app.route('/AddEffect',methods=['POST'])
def AddEffect():
    active_effects.append(request.form["effect"])
    return redirect('/')


@app.route("/Clear",methods=["POST"])
def Clear():
    active_effects.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)