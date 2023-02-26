import sqlite3
import json
class Cookbook:
    '''
    Alchemist's cookbook for retrieving information on potions and their ingredients
    '''
    def __init__(self):
        self.db = sqlite3.connect(":memory:",check_same_thread=False)
        
        # Create data structures
        cur = self.db.cursor()
        cur.execute("CREATE TABLE Ingredients(id INT, name TEXT)")
        cur.execute("CREATE TABLE Effects(id INT, name TEXT)")
        cur.execute("CREATE TABLE IngredientToEffect(ingredient_id INT, effect_id INT)")


        # Load data from JSON file
        data = {}
        with open("./data/data.json") as f:
            data = json.load(f)
        
        # Build SQLite database from data
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
        self.db.commit()
    # end __init__


    def AllIngredients(self) -> list:
        '''
        Gets a list of all available ingredients
        '''
        cur = self.db.cursor()
        cur.execute("SELECT name FROM Ingredients ORDER BY name")
        return list(r[0] for r in cur.fetchall())
    

    def AllEffects(self) -> list:
        '''
        Gets a list of all available effects
        '''
        cur = self.db.cursor()
        cur.execute("SELECT name FROM Effects ORDER BY name")
        return list(r[0] for r in cur.fetchall())
    
    def GetIngredients(self,effect: str) -> list:
        '''
        Gets a list of ingredients with the provided effect
        '''
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
        return list(r[0] for r in cur.fetchall())
    
    def GetEffects(self,ingredient) -> list:
        '''
        Gets a list of effects for an ingredient
        '''
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
        return list(r[0] for r in cur.fetchall())
    
    def GetCompatibleEffects(self,effect) -> list:
        '''
        Gets a list of effects that share an ingredient with the
        provided effect
        '''
        cur = self.db.cursor()
        cur.execute("""
            SELECT s.name
            FROM Effects p
            JOIN IngredientToEffect ite1
                ON ite1.effect_id = p.id
            JOIN IngredientToEffect ite2
                ON ite2.ingredient_id = ite1.ingredient_id
            JOIN Effects s
                ON s.id = ite2.effect_id
            WHERE p.name = ?
            """,(effect,))
        return list(r[0] for r in cur.fetchall())