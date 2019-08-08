import json

# Evaulates farms

server_name = 'SkyblockOriginal'
farm_names = ['0-tick Sugarcane (ilmango)',
              'Auto Sugarcane (GreenGuitarGuyGames)',
              'ilmango Simple Tree Farm (TNT Duper)',
              'Melon/Pumpkin Farm',
              '1 level xsisumavoid cactus farm']

with open('../data/_autofarms/autofarms.json', 'r') as f:
    autofarms = json.load(f)

with open('../data/' + server_name + '/purchase_optimal.json', 'r') as f:
    purchase_optimal = json.load(f)

with open('../data/' + server_name + '/sell_optimal.json', 'r') as f:
    sell_optimal = json.load(f)

def evaluateFarm(farm, purchase_optimal, sell_optimal):
    # Want to find the following summary stats:
    # 1. Itemized build cost
    # 2. Itemized input cost
    # 3. Itemized output profit
    # 4. Volume efficiency
    # 5. Profit/hr
    # 6. Time to payoff
    
    def getCost(item, quantity, purchase_optimal, sell_optimal):
        return purchase_optimal[item]['Buy Price'] * quantity
    
    build_cost = 0
    input_cost = 0
    output_profit = 0
    x, y, z = farm['Size']
    volume = x * y * z

    for build_item, quantity in farm['Build Cost'].items():
        if build_item in purchase_optimal:
            build_cost += getCost(build_item, quantity, purchase_optimal, sell_optimal)
        else:
            print('Unable to find:', build_item)
    
    for input_item, quantity in farm['Inputs'].items():
        if input_item in purchase_optimal:
            input_cost += getCost(input_item, quantity, purchase_optimal, sell_optimal)
        else:
            print('Unable to find:', input_item)
    
    for output_item, quantity in farm['Outputs'].items():
        if output_item in sell_optimal:
            output_profit += sell_optimal[output_item] * quantity
        else:
            print('Unable to find:', output_item)
    
    profit = output_profit - input_cost
    
    return (build_cost,
            input_cost,
            output_profit,
            profit,
            profit / (volume/1000),
            build_cost / profit)

print('CAVEAT ON ALL RESULTS: THIS WILL BE MISLEADING')
print('FOR ITEMS THAT PRODUCE MULTIPLE OUTPUTS IN CRAFTING TABLE')
for fname in farm_names:
    print('----====[ ' + fname.upper() + ' ]====----')
    metadata = evaluateFarm(autofarms[fname], purchase_optimal, sell_optimal)
    metadata = [round(x,2) for x in metadata]
    build_cost, input_cost, output_profit, profit, volume_efficiency, payoff_time = metadata
    leftpad = '25'
    print('----------------------------------------------')
    print(('{:' + leftpad + '}{:8}').format('Build cost:', build_cost))
    print(('{:' + leftpad + '}{:8}').format('Input cost:', input_cost))
    print(('{:' + leftpad + '}{:8}').format('Output profit:', output_profit))
    print(('{:' + leftpad + '}{:8}').format('Profit per hr:', profit))
    print(('{:' + leftpad + '}{:8}').format('Volume efficiency:', volume_efficiency))
    print(('{:' + leftpad + '}{:8}').format('Payoff Time (hr):', payoff_time,2))
    print('----------------------------------------------')