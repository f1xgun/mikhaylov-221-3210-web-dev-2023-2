s = input().strip()
kevin_count = 0
stuart_count = 0

VOWEL_LETTERS = 'AEUIOY'

for i in range(len(s)):
    if s[i] in VOWEL_LETTERS:
        kevin_count += len(s) - i
    else:
        stuart_count += len(s) - i

if kevin_count > stuart_count:
    print(f"KEVIN {kevin_count}")
elif kevin_count < stuart_count:
    print(f"STUART {stuart_count}")
else:
    print("NOBODY WIN")
