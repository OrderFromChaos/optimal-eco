import json

# Want to find unique between ecoinfo.json and recipes.json;
# this probably indicates some kind of misnaming
# Note that this will also return everything that doesn't have a recipe...

server_name = 'BreakdownCraft'

with open('../' + server_name + '/ecoinfo.json', 'r') as f:
    economydata = json.load(f)

with open('../recipes.json', 'r') as f:
    recipedata = json.load(f)

eco_set = set(list(economydata))
recipe_set = set(list(recipedata))

in_both = eco_set & recipe_set
eco_unique = eco_set - recipe_set
recipe_unique = recipe_set - eco_set

print('In both:')
print(in_both)
print()
print('Unique to economy (not craftable):')
print(eco_unique)
print()
print('Unique to recipe list (should be most items)')
print(recipe_unique)