from aocd import data
import re
import numpy as np
import itertools

class Cookie:
    def __init__(self):
        self.ingredient_list = {}
        self.ingredients = np.zeros((1,1),dtype=int)
        self.amounts = np.ones(1,dtype=int)

    def add_ingredient(self, line):
        ing, cap, dur, fla, tex, cal = re.match(r'(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)', line).groups()
        self.ingredient_list[ing] = tuple(map(int, [cap,dur,fla,tex,cal]))

    @classmethod
    def with_ingredients(cls, input_str):
        cookie = Cookie()
        for ing in input_str.splitlines():
            cookie.add_ingredient(ing)
        # create ingredients and amounts matrices
        cookie.ingredients = np.zeros((len(cookie.ingredient_list), 5))
        cookie.amounts = np.ones(len(cookie.ingredient_list))
        for idx, props in enumerate(cookie.ingredient_list.values()):
            cookie.ingredients[idx] = np.array(props)
        cookie.amounts[0] = 101 - len(cookie.ingredient_list)
        return cookie

    def score(self):
        props = np.dot(self.amounts, self.ingredients[:,:4])
        props = np.maximum(props, np.zeros(4))
        return np.prod(props)

    def calories(self):
        cals = np.dot(self.amounts, self.ingredients[:,4])
        return cals

    def best_score(self, calorie_count=None):
        max_score = self.score()
        # Brute force method.
        for amts in itertools.product(range(1,100 - len(self.amounts)), repeat=len(self.amounts) - 1):
            last_amt = 100 - sum(amts)
            self.amounts = list(amts) + [last_amt]
            if not calorie_count or self.calories() == calorie_count:
                score = self.score()
                if score > max_score:
                    max_score = score
        return max_score


test_input = '''Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3'''
assert Cookie.with_ingredients(test_input).best_score() == 62842880
print('15a: ', Cookie.with_ingredients(data).best_score())
assert Cookie.with_ingredients(test_input).best_score(500) == 57600000
print('15b: ', Cookie.with_ingredients(data).best_score(500))
