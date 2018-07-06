import itchat

itchat.login()

# itchat.send('hello', 'tony55199293')

friends = itchat.get_friends(update=True)[0:]
male = female = other = 0

for i in friends[1:]:
    sex = i["Sex"]
    if sex == 1:
        male += 1
    elif sex == 2:
        female += 1
    else:
        other +=1

print("male", male)
print("female", female)
print("other", other)