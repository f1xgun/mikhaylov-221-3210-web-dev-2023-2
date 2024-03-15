n, m = map(int, input().split())
cargo = []
for i in range(m):
    name, weight, price = input().split()
    cargo.append({
        'name': name,
        'weight': float(weight),
        'price': float(price),
    })

cargo = sorted(cargo, key=lambda x: -(x['price'] / x['weight']))
cur_weight = 0
max_ind = 0
for i in range(len(cargo)):
    if cur_weight + cargo[i]['weight'] <= n:
        cur_weight += cargo[i]['weight']
    else:
        free_weight = n - cur_weight
        cargo[i]['price'] *= (free_weight / cargo[i]['weight'])
        cargo[i]['price'] = float("{:.2f}".format(cargo[i]['price']))
        cargo[i]['weight'] = free_weight
        cur_weight = n

    max_ind += 1
    if cur_weight == n:
        break

cargo = sorted(cargo[:max_ind], key=lambda x: -x['price'])
for i in range(max_ind):
    print(*cargo[i].values())
