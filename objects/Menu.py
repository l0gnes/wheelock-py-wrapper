from datetime import date
from objects.Category import Category
from typing import List

class Menu(object):
    
    name : str
    d : date
    cateogries : List[Category]

    def __init__(
        self,
        name : str,
        d : date,
        categories : List[Category] = []
    ) -> None:
        self.name = name
        self.d = date
        self.cateogries = categories

    @classmethod
    def parseFromJSON(
        _,
        json_data : dict
    ) -> "Menu":
        return Menu(
            name = json_data['periods']['name'],
            d = date.fromisoformat(json_data['date']),
            categories = [Category.parseFromJSON(cij) for cij in json_data['periods']['categories']]
        )