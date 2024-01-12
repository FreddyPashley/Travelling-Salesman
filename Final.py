locations = 5

######################################
from random import randint
from math import factorial
from time import sleep
from matplotlib import pyplot as plt
from itertools import permutations

xy_range = 50
num = locations

figure, axis = plt.subplots(1, 3)

while True:
    axis[0].cla()
    axis[1].cla()
    axis[2].cla()

    cities = [[randint(1,xy_range), randint(1,xy_range)] for i in range(num)]
    cities.insert(0, [0,0])
    cities.append([0,0])

    def distanceBetweenPoints(x1, y1, x2, y2):
        dX = x2 - x1
        dY = y2 - y1
        distance = (dX**2 + dY**2)**.5
        return distance

    smallest_so_far, largest_so_far = None, None
    journeyCombinations = []
    journeyI = 1
    combos = len([i for i in permutations(cities[1:-1])])
    iters = factorial(num)

    if num <= 2:
        x = "Not enough cities"
        raise ValueError(x)

    perms = [i for i in permutations(cities[1:-1])]

    while perms != []:
        journey = perms[0]
        perms.pop(0)
        percentage = round(((journeyI+1)/combos)*100, 1)
        journey = [cities[0]] + list(journey) + [cities[-1]]
        journey = list(journey)

        journeyIprint = journeyI
        journeyI += 1

        x = [i[0] for i in cities]
        y = [i[1] for i in cities]

        axis[0].cla()

        axis[0].scatter(x, y)
        axis[1].scatter(x, y)
        axis[2].scatter(x, y)
        
        total = 0
        for j in range(len(cities)-1):
            points = journey[j:j+2]
            x1, y1 = points[0]
            x2, y2 = points[1]
            d = distanceBetweenPoints(x1, y1, x2, y2)
            total += d

        for j in range(len(journey)-1):
            points = journey[j:j+2]
            x1, y1 = points[0]
            x2, y2 = points[1]
            axis[0].plot([x1, x2], [y1, y2], 'bo', linestyle="dotted")

        for i, txt in enumerate(range(1, len(cities))):
            axis[0].set_title(f"Working journey\n{percentage}% ({iters})\nDistance: {round(total, 1)}")
                
        if smallest_so_far is None or total < smallest_so_far:
            axis[1].cla()
            smallest_so_far = total
            for j in range(len(journey)-1):
                points = journey[j:j+2]
                x1, y1 = points[0]
                x2, y2 = points[1]
                axis[1].plot([x1, x2], [y1, y2], 'go', linestyle="dotted")

            for i, txt in enumerate(range(1, len(cities))):
                axis[1].annotate(str(txt), (journey[i][0], journey[i][1]), xytext=(journey[i][0], journey[i][1]+max([i[1] for i in cities])//20), color="green")
                axis[1].set_title(f"Best journey\nIteration: {'{:,}'.format(journeyIprint)}\nMinimum distance: {round(smallest_so_far, 1)}")

        if largest_so_far is None or total > largest_so_far:
            axis[2].cla()
            largest_so_far = total
            for j in range(len(journey)-1):
                points = journey[j:j+2]
                x1, y1 = points[0]
                x2, y2 = points[1]
                axis[2].plot([x1, x2], [y1, y2], 'ro', linestyle="dotted")

            for i, txt in enumerate(range(1, len(cities))):
                axis[2].annotate(str(txt), (journey[i][0], journey[i][1]), xytext=(journey[i][0], journey[i][1]+max([i[1] for i in cities])//20), color="red")
                axis[2].set_title(f"Worst journey\nIteration: {'{:,}'.format(journeyIprint)}\nMaximum distance: {round(largest_so_far, 1)}")
                    
        plt.pause(.00001)

    axis[0].cla()
    axis[0].scatter(x, y)
    axis[0].set_title("Locations")

    plt.show(block=False)
    sleep(5)
