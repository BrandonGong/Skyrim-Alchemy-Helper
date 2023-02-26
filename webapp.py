from flask import Flask, render_template, request, redirect, url_for
from cookbook import Cookbook
from pyvis.network import Network

app = Flask(__name__)
cb =  Cookbook()

_active_effects = []

@app.route('/')
def Home():
    effects = []
    for effect in cb.AllEffects():
        e = {}
        e["name"] = effect
        e["active"] = effect in _active_effects
        effects.append(e)
    
    return render_template("index.html", effects=effects, active_effect=_active_effects )

@app.route('/AddEffect',methods=['POST'])
def AddEffect():
    _active_effects.append(request.form["effect"])
    return redirect('/')


@app.route("/Clear",methods=["POST"])
def Clear():
    _active_effects.clear()
    return redirect('/')

@app.route("/Graph")
def Graph():
    if len(_active_effects) > 0:
        # Max ingredients per potion is 3
        # For potions with only 2 ingredients to have an effect
        # both ingredients must share an effect.
        # For multiple effects, all effects must be shared between two ingredients, or for
        # potions with 3 ingredients they must be linked by an ingredient with both effects.
        g = Network(height="750px",bgcolor="#222222",font_color="#f2f2f2")
        for effect in _active_effects:
            g.add_node(effect,color="#cc0000")
            ingredients = cb.GetIngredients(effect)
            for ingredient in ingredients:
                g.add_node(ingredient,color="#0099cc")
                g.add_edge(effect,ingredient)

        return g.generate_html()
    else:
        return "Select an effect to view ingredients"

if __name__ == "__main__":
    app.run(debug=True)