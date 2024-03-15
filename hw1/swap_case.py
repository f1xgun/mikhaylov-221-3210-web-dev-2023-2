s = input()
new_str = ""
for char in s:
    if not char.isalpha():
        new_str += char
        continue
    if char.islower():
        new_str += char.upper()
    else:
        new_str += char.lower()
print(new_str)
