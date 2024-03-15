prices = [0, 0, 0]
with open("products.csv", "r", encoding="utf-8") as file:
    for line in file:
        if line == '':
            continue

        product_name, adult_price, pensioner_price, child_price = line.strip().split(",")
        if product_name == "Продукт":
            continue

        prices[0] += float(adult_price)
        prices[1] += float(pensioner_price)
        prices[2] += float(child_price)

output_template = """{:.2f} {:.2f} {:.2f}"""

print(output_template.format(*prices))
