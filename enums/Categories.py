from enum import Enum


class Categories(Enum):
    YUGIOH = '/yugioh/4736'
    POKEMON = '/pokemon/7061'
    ONE_PIECE = '/one-piece-tcg/19304'

    @staticmethod
    def get(value):
        for category in Categories:
            if category.name.lower() == value.lower():
                return category
        return None
