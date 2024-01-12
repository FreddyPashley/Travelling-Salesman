locations = 5  # Change me!

######################################
# CODE
######################################

# Imports
from random import randint
from math import factorial
from time import sleep
from matplotlib import pyplot as plt
from itertools import permutations


# Global variables
timeBetweenLoops = 5  # Seconds
xy_range = 50  # Max x and y values


# Globals constants
num = locations
graphs = 3
figure, axis = plt.subplots(1, graphs)


# Functions
def distanceBetweenPoints(x, y) -> float:
    """Distances between two coordinates using Pythagoras"""
    x1, x2 = x
    y1, y2 = y
    dX = x2 - x1
    dY = y2 - y1
    distance = (dX**2 + dY**2)**.5  # Calculating hypot
    return distance


def clearAll():
    """Reset all graphs"""
    for i in range(graphs):
        axis[i].cla()


def clearAxis(num):
    """Reset specific graph"""
    if num in range(graphs):
        axis[num].cla()


def scatterXY(axisNum, x, y):
    """Scatter coordinates as points on a graph"""
    axis[axisNum].scatter(x, y)


def generateLocations() -> list:
    """Generate certain amount of locations and their coordinates"""
    locations = [[randint(1, xy_range), randint(1, xy_range)] for i in range(num)]
    locations.insert(0, [0, 0])
    locations.append([0, 0])
    return locations


def generateCombinations(locations) -> list:
    """Generate all possible combinations from list of coordinates"""
    return [i for i in permutations(locations[1:-1])]


def plotLine(axisNum, x, y, colour, style="dotted"):
    """Plots a line on a graph"""
    if axisNum in range(graphs):
        axis[axisNum].plot(x, y, colour+'o', linestyle=style)


def annotateAxis(axisNum, text, xy, xytext, colour):
    """Labels points on a graph"""
    if axisNum in range(graphs):
        axis[axisNum].annotate(text, xy, xytext=xytext, color=colour)


def axisTitle(axisNum, title):
    """Assigns a graph a title"""
    if axisNum in range(graphs):
        axis[axisNum].set_title(title)


# Main
while True:
    clearAll()  # Reset the window
    cities = generateLocations()
    perms = generateCombinations(cities)

    smallest_so_far, largest_so_far = None, None
    journeyCombinations = []
    journeyI = 1
    combos = len(perms)

    if num <= 2:
        err = "Not enough locations"
        raise ValueError(err)

    while perms != []:
        journey = perms[0]
        perms.pop(0)
        journey = [cities[0]] + list(journey) + [cities[-1]]
        journey = list(journey)

        percentage = round(((journeyI+1)/combos)*100, 1)

        journeyI += 1

        x = [i[0] for i in cities]
        y = [i[1] for i in cities]

        clearAxis(0)

        for i in range(graphs):
            scatterXY(i, x, y)
        
        total = 0  # Total distance travelled for journey
        for j in range(len(cities)-1):
            points = journey[j:j+2]  # Get steps in journey, from 1-2, 2-3, 3-4...
            x1, y1 = points[0]
            x2, y2 = points[1]
            d = distanceBetweenPoints([x1, x2], [y1, y2])
            total += d

        for j in range(len(journey)-1):
            points = journey[j:j+2]
            x1, y1 = points[0]
            x2, y2 = points[1]
            plotLine(0, [x1, x2], [y1, y2], "b")  # Plot each step of the journey as a line

        for i, txt in enumerate(range(1, len(cities))):
            axisTitle(0, f"Working journey\n{percentage}% ({combos})\nDistance: {round(total, 1)}")
                
        if smallest_so_far is None or total < smallest_so_far:  # If journey distance is less than minimum record
            clearAxis(1)
            smallest_so_far = total
            for j in range(len(journey)-1):
                points = journey[j:j+2]
                x1, y1 = points[0]
                x2, y2 = points[1]
                plotLine(1, [x1, x2], [y1, y2], "g")  # Plot each step of the journey as a line

            for i, txt in enumerate(range(1, len(cities))):
                annotateAxis(1, str(txt), (journey[i][0], journey[i][1]), (journey[i][0], journey[i][1]+max([i[1] for i in cities])//20), "green")
                axisTitle(1, f"Best journey\nIteration: {'{:,}'.format(journeyI-1)}\nMinimum distance: {round(smallest_so_far, 1)}")

        if largest_so_far is None or total > largest_so_far:  # If journey distance is more than maximum record
            clearAxis(2)
            largest_so_far = total
            for j in range(len(journey)-1):
                points = journey[j:j+2]
                x1, y1 = points[0]
                x2, y2 = points[1]
                plotLine(2, [x1, x2], [y1, y2], "r")  # Plot each step of the journey as a line

            for i, txt in enumerate(range(1, len(cities))):
                annotateAxis(2, str(txt), (journey[i][0], journey[i][1]), (journey[i][0], journey[i][1]+max([i[1] for i in cities])//20), "red")
                axisTitle(2, f"Worst journey\nIteration: {'{:,}'.format(journeyI-1)}\nMaximum distance: {round(largest_so_far, 1)}")
                    
        plt.pause(.00001)  # To enable live updating of graphs

    clearAxis(0)
    scatterXY(0, x, y)
    axisTitle(0, "Locations")  # Replace graph 1 title to 'Locations' once work has done

    plt.show(block=False)
    sleep(timeBetweenLoops)  # Allow time for user to see result before new combinations
