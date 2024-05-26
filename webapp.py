from flask import Flask, render_template, request, redirect, session
import secrets
from cookbook import Cookbook
from pyvis.network import Network

app = Flask(__name__)
cb =  Cookbook()


@app.route('/')
def Home():
    active_effects = _GetActiveEffects()
    effects = []
    for effect in cb.AllEffects():
        e = {}
        e["name"] = effect
        e["active"] = effect in active_effects
        e["compatible"] = True
        for ae in active_effects:
            if effect not in cb.GetCompatibleEffects(ae):
                e["compatible"] = False
                break

        effects.append(e)
    
    return render_template("index.html", effects=effects)

@app.route('/AddEffect',methods=['POST'])
def AddEffect():
    if "active_effects" in session:
        session["active_effects"].append(request.form["effect"])
        session.modified = True
    else:
        session["active_effects"] = [request.form["effect"]]

    return redirect('/')


@app.route("/Clear",methods=["POST"])
def Clear():
    if "active_effects" in session:
        session["active_effects"].clear()
        session.modified = True
    return redirect('/')

@app.route("/Graph")
def Graph():
    active_effects = _GetActiveEffects()
    if len(active_effects) > 0:
        # Max ingredients per potion is 3
        # For potions with only 2 ingredients to have an effect
        # both ingredients must share an effect.
        # For multiple effects, all effects must be shared between two ingredients, or for
        # potions with 3 ingredients they must be linked by an ingredient with both effects.
        g = Network(height="750px",bgcolor="#222222",font_color="#f2f2f2")
        for effect in active_effects:
            g.add_node(effect,color="#0d6efd",shape="star")
            ingredients = cb.GetIngredients(effect)
            for ingredient in ingredients:
                secondary_effects = cb.GetEffects(ingredient)
                title = ingredient + "\n" + "\n".join(f"* {e}" for e in secondary_effects)
                g.add_node(ingredient,color="#0dcaf0",title=title)
                g.add_edge(effect,ingredient)

                # for e in secondary_effects:
                #     if e not in active_effects:
                #         # add a secondary effect
                #         g.add_node(e,color="#adb5bd",shape="star")
                #         g.add_edge(e,ingredient)

        g.force_atlas_2based()
        return g.generate_html()
    else:
        return "<p style='color: white'>Select an effect to view ingredients.</p>"


def _GetActiveEffects():
    if "active_effects" in session:
        return session["active_effects"]
    else:
        return []

if __name__ == "__main__":
    app.secret_key = secrets.token_hex()
    app.run(host='0.0.0.0',port=5000)