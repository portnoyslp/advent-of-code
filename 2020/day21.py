from aocd import data
import re
from collections import defaultdict


class AllergenAssessment:
    def __init__(self, input_str):
        self.ingredients_and_allergens = []
        self.poss_ingredients_for_allergen = defaultdict(set)
        self.poss_allergens_for_ingredient = defaultdict(set)
        self.parse_input(input_str)

    def parse_input(self, input_str):
        for line in input_str.splitlines():
            (ingredients_str, allergens_str) = re.match(r'([\w ]+) \(contains ([\w, ]+)\)', line).groups()
            ingredients = ingredients_str.split(' ')
            allergens = allergens_str.split(', ')
            self.ingredients_and_allergens.append((ingredients, allergens))
            for ingredient in ingredients:
                self.poss_allergens_for_ingredient[ingredient].update(allergens)
            for allergen in allergens:
                if len(self.poss_ingredients_for_allergen[allergen]) == 0:
                    self.poss_ingredients_for_allergen[allergen].update(ingredients)
                else:
                    self.poss_ingredients_for_allergen[allergen].intersection_update(ingredients)

    def resolve_singleton_allergens(self):
        while True:
            changes_made = False
            for allergen, ingredient in [(a, next(iter(iset))) for a, iset in self.poss_ingredients_for_allergen.items()
                                         if len(iset) == 1]:
                singleton = {allergen}
                if self.poss_allergens_for_ingredient[ingredient] > singleton:
                    self.poss_allergens_for_ingredient[ingredient] = singleton
                    changes_made = True
            # Check ing->all map, and get rid of any possibilities that are now impossible
            for allergen, ingredients in self.poss_ingredients_for_allergen.items():
                for ingredient in ingredients:
                    if allergen not in self.poss_allergens_for_ingredient[ingredient]:
                        self.poss_ingredients_for_allergen[allergen].remove(ingredient)
                        changes_made = True
                        break
            # Check all->ing map, and get rid of any possibilities that are now impossible
            for ingredient, allergens in self.poss_allergens_for_ingredient.items():
                for allergen in allergens:
                    if ingredient not in self.poss_ingredients_for_allergen[allergen]:
                        self.poss_allergens_for_ingredient[ingredient].remove(allergen)
                        changes_made = True
                        break
            if not changes_made:
                break

    def find_non_allergens(self):
        self.resolve_singleton_allergens()
        non_allergens = {i for i, aset in self.poss_allergens_for_ingredient.items() if len(aset) == 0}
        count = 0
        for non_allergen in non_allergens:
            for (ilist, _) in self.ingredients_and_allergens:
                if non_allergen in ilist:
                    count += 1
        return count

    def find_dangerous_ingredients(self):
        self.resolve_singleton_allergens()
        sorted_allergens = sorted(list(self.poss_ingredients_for_allergen.keys()))
        danger = [next(iter(self.poss_ingredients_for_allergen[x])) for x in sorted_allergens]
        return ','.join(danger)


test_input = '''mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)'''
assert AllergenAssessment(test_input).find_non_allergens() == 5
print('21a: ', AllergenAssessment(data).find_non_allergens())

assert AllergenAssessment(test_input).find_dangerous_ingredients() == 'mxmxvkd,sqjhc,fvjkl'
print('21b: ', AllergenAssessment(data).find_dangerous_ingredients())