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
    
    def GetIngredients(self,effects: list[str]) -> list:
        '''
        Gets a list of ingredients with the provided effects
        '''
        if len(effects) < 1:
            raise Exception("At least one effect must be provided")
        # Max ingredients per potion is 3
        # For potions with only 2 ingredients to have an effect
        # both ingredients must share an effect.
        # For multiple effects, all effects must be shared between two ingredients, or for
        # potions with 3 ingredients they must be linked by an ingredient with both effects.
        select_sql = """
            SELECT i.name
            FROM Ingredients i
            JOIN IngredientToEffect ite
                ON ite.ingredient_id = i.id
            JOIN Effects e
                ON e.id = ite.effect_id
            WHERE e.name = ?
            """
        #TODO: Fix this logic. Intersection does not work with multiple effects when joined by a 3rd ingredient
        sql = select_sql + ("INTERSECT " + select_sql) * (len(effects)-1)

        cur = self.db.cursor()
        cur.execute(sql,effects)
        return list(r[0] for r in cur.fetchall())
    
    def GetEffects(self,ingredient) -> list:
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