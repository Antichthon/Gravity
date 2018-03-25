import numpy

def probability():
    position = 10
    tick = 0
    finalposhistory = []
    jumphistory = []
    while tick < 10:
        coinflip = numpy.random.randint(1,3)
        if coinflip == 1:
            position -= 1
            jumphistory.append(position)
            continue
        else:
            position += 1
            jumphistory.append(position)
        finalposhistory.append(position)
        tick += 1
    return [finalposhistory, jumphistory]

finalposhistory_total = 0
finalposhistory_length = 0
jumphistory_total = 0
jumphistory_length = 0

for _ in range(100000):
    result = probability()
    finalposhistory_total += sum(result[0])
    finalposhistory_length += len(result[0])
    jumphistory_total += sum(result[1])
    jumphistory_length += len(result[1])

print(finalposhistory_total/finalposhistory_length)
print(jumphistory_total/jumphistory_length)
