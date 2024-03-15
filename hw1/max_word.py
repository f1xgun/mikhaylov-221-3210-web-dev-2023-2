words = []
with open("example.txt", "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip().split()
        for word in line:
            word = ''.join(list(filter(lambda x: x.isalpha(), word)))
            words.append(word)

max_len = -1
words_with_max_len = []
for word in words:
    word_len = len(word)
    if word_len > max_len:
        words_with_max_len = [word]
        max_len = word_len
    elif word_len == max_len:
        words_with_max_len.append(word)

print('\n'.join(words_with_max_len))
