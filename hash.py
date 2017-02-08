import mmh3

words = ['Arthur Dent', 'Tricia McMillan', 'Zaphod Beeblebrox', 'Ford Prefect', 'Marvin', 'Fenchurch', 'Slartibartfast', 'Prostetnic Vogon Jeltz']
S1 = words[:6]
S2 = words[2:]

for word in words:
    print word, [mmh3.hash(word, i) % 16 for i in range(2)]
    

