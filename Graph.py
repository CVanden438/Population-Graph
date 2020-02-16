# Program to plot data from GBplaces.csv file onto a graph

# Importing python packages to use in program
# For plotting graph
import matplotlib.pyplot as plt
# For plotting 3D annotations and for updating annotation position as graph is moved
from mpl_toolkits.mplot3d import proj3d
# For numerous mathematical operations
import math

# Defining functions
# Function to update position of annotations as graph is moved
def update_position(e):
    # Transforms the coordinates into a 2D projection
    tX, tY, _ = proj3d.proj_transform(Long, Lat, LogPop, ax.get_proj())
    # Loops through every point, changing the labels x and y coordinates to the new position
    for i in range(len(Names)):
        label = labels[i]
        label.xy = tX[i],tY[i]
        label.update_positions(fig.canvas.renderer)
    # Draws the annotations in their new positions
    fig.canvas.draw()
    return

# Main program starts here

# Reads in the GBplaces.csv file to take data from
readFile = open('GBplaces.csv','r');

# Defining Arrays
# Array to store place names
Names = [];
# Array to store place type
Type = [];
# Array to store log base 2 of population, done in order to give London a suitable position on graph
LogPop = [];
# Array to store place lattitudes
Lat = [];
# Array to store place longitudes
Long = [];
# Array to store annotations of the places
labels = [];

# Defining variables
# Setting z to 0 for use in cutting off first line of GBPlaces file
z = 0

# Reads through the file
for line in readFile:
  # Splits each line of the file up
  splitUp = line.split(",")
  # Gets here once it reaches second line of file
  if z == 1:
    # Adds each secion of the line to the various arrays
    Names.append(splitUp[0]);
    Type.append(splitUp[1]);
    # Converts the population column into log base 2 of the population
    lowpop = math.log2(int(splitUp[2]));
    LogPop.append(lowpop);
    Lat.append(float(splitUp[3]));
    Long.append(float(splitUp[4]));
  # Gets here only on first line of file to prevent it from including it in the arrays
  # Sets z to one so program will now go to if function above for rest of loop
  z = 1
# Closes the GBplaces file
readFile.close();

# Plotting the 3D scatter graph
# Sets the plot to the fig variable so the ax subplot can be added
# Sets the intial size of the graph window
fig = plt.figure(figsize=(20,20))
# Creates a 3D subplot and adds it to the fig variable
ax = fig.add_subplot(111, projection='3d')

# Loops through the data points
for i in range(len(Names)):
  # Plots a different marker and colour for each point depending on if it is a Town or City
  if Type[i] == "Town":
    # If the point is a town, program gets here and plots the point with a star marker, green colour and a size of 90
    ax1 = ax.scatter(Long[i], Lat[i], LogPop[i], marker="*", c='#19e619', s=80)
  else:
    # If the point is a city, program gets here and plots the point with a square marker, blue colour and a size of 30
    ax2 = ax.scatter(Long[i], Lat[i], LogPop[i], marker="s", c='b', s=25)

# Adding titles, axis titles and legend to the graph
# Adds a legend to the graph in the top right, showing the Town points as a green star and the City points as a blue square
plt.legend((ax1, ax2), ('Town', 'City'), scatterpoints=1)
# Changes the z axis labels from the log values to the equivalent population values on a log scale
ax.set_zticklabels([pow(2,15),pow(2,16),pow(2,17),pow(2,18),pow(2,19),pow(2,20),pow(2,21),pow(2,22),pow(2,23)])
# Changes the background colour of the graph to a light blue
# ax.set_axis_bgcolor('#e5eeff')
# Adds a title to the graph
ax.set_title('Graph of 100 Most Populated Towns in GB')
# Adds label to the x-axis
ax.set_xlabel('Longitude')
# Adds label to the y-axis
ax.set_ylabel('Latitude')
# Adds label to the z-axis
ax.set_zlabel('Population (Log Scale)')

# Projects the points onto a 2D plane in order to add annotations
tX, tY, _ = proj3d.proj_transform(Long, Lat, LogPop, ax.get_proj())

# Loops through the data points and adds an annotation to each one
for i in range(len(Names)):
    text=str(Names[i])
    label = ax.annotate(text,
            xycoords='data',
            xy = (tX[i], tY[i]), xytext = (-20, 20),
            textcoords = 'offset points', ha = 'right', va = 'top', fontsize=6,
            bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
            arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
    labels.append(label)

# Calls on the update position function to update the positions of the annotations as the graph is moved
fig.canvas.mpl_connect('button_release_event', update_position)

# Displays the 3D scatter graph
plt.show();
