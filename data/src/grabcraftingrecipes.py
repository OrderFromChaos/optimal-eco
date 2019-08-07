from lxml import html
import requests
import json

url = 'http://diamondboots.com/#crafting' # Version 1.12

GET_DATA = False

if GET_DATA:
    page = requests.get(url)

    with open('test.html', 'w') as f:
        f.write(page.content.decode('utf-8'))

# Line 228 is the interesting one (1-indexed)
with open('test.html', 'r') as f:
    recipe_data = f.readlines()[227]
    tree = html.fromstring(recipe_data)

test_set = [x for x in tree]
# print(test_set)
# Wanted: names, crafting recipes

## ITEM DATABASE IDs
IDs = [x.get('id')[5:] for x in test_set]

### NAMES
def strongTolerant(elt):
    endStr = elt.text
    strong_text = elt.xpath('.//strong')
    if strong_text:
        endStr += ''.join([x.text for x in strong_text])
    return endStr

names = [strongTolerant(x) for x in tree.xpath('.//h2')]

### CRAFTING RECIPES
recipes = [x[1].get('recipe') for x in test_set]

### ALL TOGETHER NOW
ID_lookup = {i: {
                    'name': n,
                    'recipe': r if r is None else r.split(',')
                }
                for i, n, r in zip(IDs, names, recipes)}

### CONVERT RECIPES

ID_lookup['424']['recipe'] = '423,263' # One edge case for some reason

for key, subdict in ID_lookup.items():
    for name, recipe in subdict.items():
        if isinstance(recipe, list):
            if len(recipe) > 0:
                # Get names of all nonzero items
                newdict = dict()
                newdictkeys = []
                for ingredient in recipe:
                    if ingredient not in ['0', '']:
                        try:
                            iname = ID_lookup[ingredient]['name']
                        except KeyError:
                            try: # Another edge case
                                iname = ID_lookup['-' + ingredient]['name']
                            except KeyError:
                                print(key, name, recipe)
                                raise
                        if iname in newdictkeys:
                            newdict[iname] += 1
                        else:
                            newdict[iname] = 1
                            newdictkeys.append(iname)
                ID_lookup[key]['recipe'] = newdict

findict = dict()
for key, subdict in ID_lookup.items():
    if subdict['recipe'] is not None:
        findict[subdict['name']] = subdict['recipe']

with open('../recipes.json', 'w') as f:
    json.dump(findict, f, indent=4)