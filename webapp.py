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
        e["compatible"] = True
        for ae in _active_effects:
            if effect not in cb.GetCompatibleEffects(ae):
                e["compatible"] = False
                break

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
            g.add_node(effect,color="#0d6efd",shape="star")
            ingredients = cb.GetIngredients(effect)
            for ingredient in ingredients:
                secondary_effects = cb.GetEffects(ingredient)
                title = ingredient + "\n" + "\n".join(f"* {e}" for e in secondary_effects)
                g.add_node(ingredient,color="#0dcaf0",title=title)
                g.add_edge(effect,ingredient)

                # for e in secondary_effects:
                #     if e not in _active_effects:
                #         # add a secondary effect
                #         g.add_node(e,color="#adb5bd",shape="star")
                #         g.add_edge(e,ingredient)

        g.force_atlas_2based()
        return g.generate_html()
    else:
        return "Select an effect to view ingredients."

if __name__ == "__main__":
    app.run()