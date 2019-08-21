import json

# Figure out whether it's better to make an item as a recipe, or just buy it

# Check if item is in ecodata. If so, return that
# If not, check if it's craftable. Then see if craftable parts are in ecodata.
# Otherwise, throw error.

# Eventual infrastructure:
# Check if item is in optimal_purchase. If so, return that
# Otherwise, throw error

server_name = 'Craftscade'

with open('../' + server_name + '/ecoinfo.json', 'r') as f:
    ecodata = json.load(f)

with open('../recipes.json', 'r') as f:
    recipedata = json.load(f)

def allIngredientsPurchaseable(recipe, recipedata, purchaseable): # recipe: dict -> (bool, float, dict)
    # Sets two bits:
    # 1. Is said ingredient also something that has a recipe? (Continue bit)
    # 2. Is said ingredient purchaseable? (Halting bit)

    # If (true, true),   move down to see if the subingredients are less expensive
    # If (true, false),  move down to see if the subingredients are purchaseable
    # If (false, true),  done with that ingredient
    # If (false, false), return false

    # Returns whether or not all ingredients can be obtained from eco, and if so, the optimal price

    def updateDict(d, key, value):
        if key in d:
            d[key] += value
        else:
            d[key] = value
        return d

    def dictMerge(a, b):
        for key, val in b.items():
            a = updateDict(a, key, val)
        return a
    
    cost_array = []
    final_ingredients = dict()
    for ingredient, quantity in recipe.items():
        parity = (ingredient in recipedata, ingredient in purchaseable)

        if parity == (False, False):
            return (False, -1.0, final_ingredients)

        if parity == (False, True):
            cost_array.append(purchaseable[ingredient]['Buy Price'] * quantity)
            final_ingredients = updateDict(final_ingredients, ingredient, quantity)

        if parity == (True, False):
            allowed, cost, subing = allIngredientsPurchaseable(recipedata[ingredient], recipedata, purchaseable)
            if allowed == False:
                return (False, -1.0, final_ingredients)
            else:
                cost_array.append(cost)
                final_ingredients = dictMerge(final_ingredients, subing)

        if parity == (True, True):
            current_cost = purchaseable[ingredient]['Buy Price'] * quantity
            allowed, cost, subing = allIngredientsPurchaseable(recipedata[ingredient], recipedata, purchaseable)
            if allowed == False:
                cost_array.append(current_cost)
                final_ingredients = updateDict(final_ingredients, ingredient, quantity)
            else:
                if cost < current_cost:
                    cost_array.append(cost)
                    final_ingredients = dictMerge(final_ingredients, subing)
                else:
                    cost_array.append(current_cost)
                    final_ingredients = updateDict(final_ingredients, ingredient, quantity)
    
    return (True, sum(cost_array), final_ingredients)

# Find crafting cost for all recipes

# Sets two bits:
# 1. Is said ingredient also something that has a recipe? (Continue bit)
# 2. Is said ingredient purchaseable? (Halting bit)

# # Testing (False, False)
# print(allIngredientsPurchaseable(recipedata['Clay Block'], recipedata, ecodata))
# # Testing (True, False)
# print(allIngredientsPurchaseable(recipedata['Daylight Sensor'], recipedata, ecodata))
# # Testing (False, True)
# print(allIngredientsPurchaseable(recipedata['Diamond Block'], recipedata, ecodata))
# # Testing (True, True)
# print(allIngredientsPurchaseable(recipedata['Cookie'], recipedata, ecodata))

purchaseable = {name:eco for name,eco in ecodata.items() if eco['Buy Price'] is not None}

purchase_set = set(list(purchaseable))
recipe_set = set(list(recipedata))
in_both = purchase_set & recipe_set

# Output data format:
# {
#     "Item Name": {
#         "Cost": float
#         "Crafting?": bool
#         "Ingredients": {
#             "Subitem Name": int
#             ...
#             # If crafting is true, just return original item name and 1
#         }
#     }
# }

optimal = dict()
for item_name in purchaseable:
    if item_name in in_both:
        topline_cost = ecodata[item_name]['Buy Price']
        # print(item_name, topline_cost)
        allowed, cost, subing = allIngredientsPurchaseable(recipedata[item_name], recipedata, purchaseable)
        if allowed: # you can buy the subingredients
            if cost < topline_cost: # the subingredients are more optimal than buying the crafted item
                optimal[item_name] = {
                    "Buy Price": cost,
                    "Crafting": True,
                    "Ingredients": subing
                }
            else:
                optimal[item_name] = {
                    "Buy Price": topline_cost,
                    "Crafting": False,
                    "Ingredients": {item_name: 1}
                }
        else:
            optimal[item_name] = {
                "Buy Price": ecodata[item_name]['Buy Price'],
                "Crafting": False,
                "Ingredients": {item_name: 1}
            }
    else: # There's no recipe for the item
        optimal[item_name] = {
            "Buy Price": ecodata[item_name]['Buy Price'],
            "Crafting": False,
            "Ingredients": {item_name: 1}
        }

# Before being done, add all items POTENTIALLY craftable with stuff in optimal.
# Order matters (for example, if stick isn't done, nothing else that requires sticks can be made),
# So doing a jury-rigged solution of doing a while loop while there are no changes.
# The alternative is making a graph and doing BFS.
# Worst case complexity is like 100!, which is bad, but unlikely.
changes = True
loop = 1
while changes:
    print(loop)
    changes = False
    search_region = recipe_set - set(optimal)
    print(len(search_region))
    for item in search_region:
        allowed, cost, subing = allIngredientsPurchaseable(recipedata[item], recipedata, optimal)
        if allowed:
            print(item, cost)
            optimal[item] = {
                "Buy Price": cost,
                "Crafting": True,
                "Ingredients": subing
            }
            changes = True
    loop += 1
    print()

with open('../' + server_name + '/purchase_optimal.json', 'w') as f:
    json.dump(optimal, f, indent=4)

# Not going to bother writing this as it's not likely to be worth it
# (ie, that you can craft something to make it more valuable)
saleable = {name:eco['Sell Price'] for name,eco in ecodata.items() if eco['Sell Price'] is not None}
with open('../' + server_name + '/sell_optimal.json', 'w') as f:
    json.dump(saleable, f, indent=4)
