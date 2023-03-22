from typing import List
from objects.FoodItem import FoodItem

class Category(object):

    category_name : str

    def __init__(
        self,
        category_name : str,
        items : List[FoodItem] = []
    ) -> None:
        
        self.category_name = category_name
        self.items = items

    @classmethod
    def parseFromJSON(
        _,
        json_data : dict
    ) -> "Category":
        return Category(
            json_data["name"],
            items = [FoodItem.parseFromJSON(fij) for fij in json_data['items']]
        )