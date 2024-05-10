data = open('data.txt', mode='r')
lines = data.readlines()

dataList = []
for i in lines:
    dataList.append(i.split(","))

for a in dataList[0:]:
    a[-1] = a[-1].replace("\n", "")

for b in dataList[1:]:
    for c in b[0:4]:
        b[b.index(c)] = int(c)


def colourOccuranceOrActiveTime(list, colour, mode):
    colours = {
        "Red": 0,
        "Yellow": 1,
        "Green": 2,
    }

    count = 0
    for n in list:
        if n[colours[colour]] == 1:
            if mode == 'colour':
                count += 1
            elif mode == 'time':
                count += n[3]
    return count


def faultyLines(list):
    temporaryList = []
    for l in list[1:]:
        if sum(l[0:3]) != 1:
            temporaryList.append(l)
    return temporaryList


def numberOfCompleteCycles(list):
    count = 0
    for i in range(1, len(list) + 1):
        try:
            if sum(list[i][0:3]) > 1:
                continue
            else:
                count += 1
        except IndexError:
            return count


greenActiveTimes = [g for g in dataList if g[0] == 1]

print(f'#1\nRed colour occurances: {colourOccuranceOrActiveTime(dataList, "Red", "colour")},\n'
      f'Yellow colour occurances: {colourOccuranceOrActiveTime(dataList, "Yellow", "colour")},\n'
      f'Green colour occurances: {colourOccuranceOrActiveTime(dataList, "Green", "colour")}.')
print(f'#2\nRed colour active time: {colourOccuranceOrActiveTime(dataList, "Red", "time")} seconds,\n'
      f'Yellow colour active time: {colourOccuranceOrActiveTime(dataList, "Yellow", "time")} seconds,\n'
      f'Green colour active time: {colourOccuranceOrActiveTime(dataList, "Green", "time")} seconds.')
print(f'#3\nAll times when Green was active (by time):{greenActiveTimes[0:5]}')
print(f'#4\nNumber of complete cycles Red-Yellow-Green-Yellow-Red in the data: {numberOfCompleteCycles(dataList)}')
print(f'#5 First five faulty lines: \n{faultyLines(dataList)[0:5]}')
