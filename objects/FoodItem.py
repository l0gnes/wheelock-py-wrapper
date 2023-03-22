from typing import List

class FoodItem(object):

    name : str
    desc : str
    calories : int
    ingredients : List[str]

    is_vegan : bool = False
    is_vegetarian : bool = False


    def __init__(
        self,
        name : str,
        desc : str = "~",
        calories : int = 0,
        ingredients : List[str] = [],

        is_vegan : bool = False,
        is_vegetarian : bool = False
    ) -> None:
        
        self.name = name
        self.desc = desc
        self.calories = calories

        self.ingredients = ingredients

        self.is_vegan = is_vegan
        self.is_vegetarian = is_vegetarian

    @classmethod
    def parseFromJSON(_, json : dict) -> "FoodItem":
        return FoodItem(
            name = json["name"],
            desc = json["desc"],
            calories = json["calories"],

            ingredients = list(map(lambda n: n.strip(), str(json["ingredients"]).split(","))),

            is_vegan = "Vegan" in [n["name"] for n in json["filters"]],
            is_vegetarian = "Vegetarian" in [n["name"] for n in json["filters"]]
        )