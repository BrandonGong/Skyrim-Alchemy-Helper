import sqlite3
import json
class Cookbook:
    def __init__(self):
        self.db = sqlite3.connect(":memory:")
        
        # Create data structures
        cur = self.db.cursor()
        cur.execute("CREATE TABLE Ingredients(id INT, name TEXT)")
        cur.execute("CREATE TABLE Effects(id INT, name TEXT)")
        cur.execute("CREATE TABLE IngredientToEffect(ingredientId INT, effectId INT)")


        # Load data from JSON file
        data = {}
        with open("./Data/data.json") as f:
            data = json.load(f)

        ingredient_id = 0
        effect_id = 0
        for ingredient in data:
            cur.execute("INSERT INTO Ingredients VALUES(?,?)",(ingredient_id,ingredient["name"]))
            for effect in ingredient["effects"]:
                res = cur.execute("SELECT id FROM Effects WHERE name = ?",(effect,)).fetchone()
                e = 0
                if res is None:
                    cur.execute("INSERT INTO Effects VALUES(?,?)",(effect_id,effect))
                    e = effect_id
                    effect_id += 1
                else:
                    e = res[0]
                cur.execute("INSERT INTO IngredientToEffect VALUES(?,?)",(ingredient_id,e))
            ingredient_id += 1


    def AllIngredients(self):
        cur = self.db.cursor()
        cur.execute("SELECT name FROM Ingredients")
        return (r[0] for r in cur.fetchall())
    
    def AllEffects(self):
        cur = self.db.cursor()
        cur.execute("SELECT name FROM Effects")
        return (r[0] for r in cur.fetchall())
    
    def GetIngredients(self,effect):
        cur = self.db.cursor()
        cur.execute("""
            SELECT i.name
            FROM Ingredients i
            JOIN IngredientToEffect ite
                ON ite.ingredient_id = i.id
            JOIN Effects e
                ON e.id = ite.effect_id
            WHERE e.name = ?
                    """,(effect,))
        return (r[0] for r in cur.fetchall())
    
    def GetEffects(self,ingredient):
        cur = self.db.cursor()
        cur.execute("""
            SELECT e.name
            FROM Ingredients i
            JOIN IngredientToEffect ite
                ON ite.ingredient_id = i.id
            JOIN Effects e
                ON e.id = ite.effect_id
            WHERE i.name = ?
                    """,(ingredient,))
        return (r[0] for r in cur.fetchall())