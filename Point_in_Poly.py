#Import Required packages
import os #Import operating system module
import csv #Import csv module
import numpy as np #import numpy module
import math #import math module
import matplotlib.pyplot as plt #import matplotlib module

#USER - REMEMBER TO CHANGE THE WORKING DIRECTORY
os.chdir()#Set working directory - This should be changed by the user!

class Geom(object): #Create Geometry class
    def getStartPoint(self): 
        return self.coords[0]
    def getEndPoint(self):
        return self.coords[-1]
    def getNumPoints(self): #Create a method that counts the number of points in a point or line object
        return self.coords.shape[0]
    def addPoint(self, point):
        self.coords = np.vstack([self.coords, point]) #np.vstack from numpy package
    @property
    def minX(self):#Returns the minimum X coordinate of every point, line or polygon inherited from the Geom class
        return min(self.coords[:,0])
    @property
    def minY(self): #Returns the minimum Y coordinate of every point, line or polygon inherited from the Geom class
        return min(self.coords[:,1])
    @property
    def maxX(self): #Returns the maximum X coordinate of every point, line or polygon inherited from the Geom class
        return max(self.coords[:,0])
    @property
    def maxY(self): #Returns the maximum Y coordinate of every point, line or polygon inherited from the Geom class
        return max(self.coords[:,1])
  

class Point(Geom):    #Create Point class to represent a set of geographic variables
    """A simple point class"""
    def __init__(self, x=0, y=0, z=float('nan')): 
        self.__coords = np.array([x,y,z], dtype=float)
        self.__coords.shape = (1,3)
    @property
    def x(self):
        return self.__coords[0,0] #Private variable
    @property
    def y(self):
        return self.__coords[0,1]
    @property
    def z(self):
        return self.__coords[0,2]
    @x.setter
    def x(self, x):
        self.__coords[0,0] = x
    @y.setter   
    def y(self, y):
        self.__coords[0,1] = y
    @z.setter
    def z(self, z):
        self.__coords[0,2] = z
    @property
    def coords(self):
        return self.__coords
    def addPoint(self, point): #Overrides addPoint method 
        return "Can't add a point to a point"

class Line(Geom):   #Create a Line class to represent a sequence of points
    def __init__(self, points = []): 
        self.__coords = np.vstack(points)
    @property
    def coords(self):
        return self.__coords
    @coords.setter
    def coords(self, points):
        self.__coords = np.vstack(points)

class Polygon(Line, Geom): #Create a polygon class which inherits from the Line and Geometry classes
    def getEndPoint(self): #Overrides the getEndPoint method in Geom and returns the start point
        return self.getStartPoint()
        #Adapted from: Github user (JoJoCoder), 2017. https://github.com/JoJocoder/PNPOLY
        #Adapted from: Github user (ayushub), 2014. https://github.com/ayushub/perimeter
        #Adapted from: Github user (nickodell), 2012. https://github.com/nickodell/point-in-polygon
        #Adapted from: Github user (VasiliosKalogirou), 2016. https://github.com/vasilioskalogirou/Point-in-Polygon
        #Adapted from: StackExchange user (squib1996), 2015. https://gis.stackexchange.com/questions/170264/python-point-in-polygon-boundary-and-vertex-check-ray-casting
        #Adapted from: Lawhead (2011). http://geospatialpython.com/2011/08/point-in-polygon-2-on-line.html
    def testBoundingBox(self, testPoint): #Creates a function that tests whether a point is within the bounding box 
        if (testPoint.x < self.minX) or (testPoint.x > self.maxX) or (testPoint.y<self.minY) or (testPoint.y>self.maxY):
            return 0 #The point is not positioned within the bounding box
        else:
            return 1 #The point is positioned within the bounding box
    def testPointInPoly(self, testPoint): #Creates a function that tests whether a point is within the polygon
        vertexPoint=False #Tests if the point is on one of the polygon vertices
        boundaryPoint=False #Tests if the point is on the polygon boundary
        test = False #True/False Boolean variable
        xP1 = testPoint.x #Assigns the X value of the testing point to the X coordinate of point 1
        yP1 = testPoint.y #Assigns the Y value of the testing point to the Y coordinate of point 1
        xP2 = self.maxX + 50 #Assigns point 2 X a value which is definitely greater than any expected bounding box
        yP2 = self.maxY + 50 #Assigns point 2 Y a value which is definitely greater than any expected bounding box

        for i in range(0,self.getNumPoints()-1): 
            if (testPoint.x==self.coords[i][0]) and (testPoint.y==self.coords[i][1]): #Setting conditions for determining if a point lies on a polygon vertex    
                VertexPoint=True
                return "Vertex"
                break
            else:
                xV1 = self.coords[i][0] #Assign the X coordinates of the first vertex of a line
                yV1 = self.coords[i][1] #Assign the Y coordinates of the first vertex of a line
                xV2 = self.coords[i+1][0] #Assign the X coordinates of the second vertex of a line
                yV2 = self.coords[i+1][1] #Assign the Y coordinates of the second vertex of a line
                lV1 = Point(xV1,yV1) #Creates the first vertex of a line (V1) using the above X and Y values
                lV2 = Point(xV2,yV2) #Creates the second vertex of a line (V2) using the above X and Y values
                line_seg = Line([lV1.coords,lV2.coords]) #Creates the Line Segment connecting the two points (lV1 and lV2) 
                
                if (xP1==xV1 and xP1==xV2 and yP1>line_seg.minY and yP1<line_seg.maxY): #Setting conditions for determining if a point lies on a polygon boundary
                    boundaryPoint=True
                    return "Boundary"
                    break
                elif (yP1==yV1 and yP1==yV2 and xP1>line_seg.minX and xP1<line_seg.maxX): #Setting conditions for determining if a point lies on a polygon boundary
                    BoundaryPoint=True
                    return "Boundary"
                    break
                else:
                    m=(yV2-yV1)/(xV2-xV1) #Calculate the slope of the line
                    beta=yV2-m*xV2 #Caclulate the beta parameter of the line
                    if ((yP1-(m*xP1)-beta)==0 and xP1>line_seg.minX and xP1<line_seg.maxX and yP1>line_seg.minY and yP1<line_seg.maxY): #Setting conditions for determining if a point lies on a polygon boundary
                        BoundaryPoint=True
                        return "Boundary"
                        break
                    else: #Ray-Casting algorithm parameters
                        RC_parameter1 = (xP2-xP1)*(yV1-yP2)-(yP2-yP1)*(xV1-xP2)
                        RC_parameter2 = (xP2-xP1)*(yV2-yP2)-(yP2-yP1)*(xV2-xP2)
                        RC_parameter3 = (xV2-xV1)*(yP1-yV2)-(yV2-yV1)*(xP1-xV2)
                        RC_parameter4 = (xV2-xV1)*(yP2-yV2)-(yV2-yV1)*(xP2-xV2)
                        if (RC_parameter1*RC_parameter2 <0) and (RC_parameter3*RC_parameter4<0):
                            test=not(test) #Switch the test status variable
        if vertexPoint==False and boundaryPoint==False: #If point is not on a vertices or boundary, return inside/outside 
            if test==True:
                return "inside"
            else:
                return "outside"


#Adapted from: PythonForBeginners (2013): http://www.pythonforbeginners.com/systems-programming/using-the-csv-module-in-python/
#Adapted from: StackExchange user (2015): https://stackoverflow.com/questions/29312209/ask-user-to-write-the-correct-file-name-if-he-wrote-wrong
file_loaded = False #True/False boolean variable
while file_loaded == False:
    user_PolyCsv = raw_input("Please type the full name, including .csv extension of the file which contains the polygon information, then hit enter: ") #Prompt user to enter polygon file
    if user_PolyCsv.endswith('.csv') and os.path.exists(user_PolyCsv): #Checks if relevent file type (.csv) entered and if the file exists
        file_loaded = True #Switch boolean variable status following a valid user entered file
    else: #If file not a .csv or does not exist, inform the user and prompt again
        print "" #Splits up the prompt text
        print "INVALID POLYGON FILE. Please enter a valid .csv file below." #Inform the user of an invalid file entered
        print "Tip: If you're having trouble, please include the full file path. Alternatively, you might find it easier to move the polygon file to the same folder as this script." #Advise the user
        print "" #Splits up the advice text before user promted to enter a file again

            
with open( user_PolyCsv, 'r') as csvfile: #Open the user entered .csv file
    dataReader = csv.reader(csvfile) #Variable to read the contents of a .csv file
    random_List= dataReader.next() #Reads the coordinates of the first point from the .csv file
    first_Point=Point(x=random_List[0], y =random_List[1]) #Creates a variable for the first point
    myPolygon=Polygon(first_Point.coords) #Begins to construct the polygon using the cooridnates from the first point
    for line in dataReader: #Iterates through polygon .csv file
        myPoint = Point(x=line[0],y=line[1]) #Assiging X and Y coordinates
        myPolygon.addPoint(myPoint.coords) #Creates polygon from X and Y coordinates
    myPolygon.addPoint(myPolygon.getEndPoint()) #Closes the polygon once all points are plotted and the shape is complete
    del random_List, first_Point, dataReader #Delete temporary variables used in polygon construction

#Adapted from: pythonprogramming.net (2013). https://pythonprogramming.net/reading-csv-files-python-3/    
outside_BoundingBoxX=[] #Empty list to append the X coorindate of any point outside the bounding box
outside_BoundingBoxY=[] #Empty list to append the Y coordinate of any point outside the bounding box
outside_PolyX=[] #Empty list to append the X cooridnate of any point outside the polygon (but inside the bounding box)
outside_PolyY=[] #Empty list to append the Y coordinate of any point outside the polygon (but inside the bounding box)
boundary_PolyX=[] #Empty list to append the X coorinate of any point on the boundary of the polygon 
boundary_PolyY=[] #Empty list to append the Y coordinate of any point on the boundary of the polygon 
on_verticesX=[] #Empty list to append the X coordinate of any point on the vertices of the polygon 
on_verticesY=[] #Empty list to append the Y coordinate of any point on the vertices of the polygon 
inside_PolyX=[] #Empty list to append the X cooridnate of any point within the polygon
inside_PolyY=[] #Empty list to append the Y coordinate of any point within the polygon

file_loaded = False #True/False boolean variable
while file_loaded == False:
    user_PointCsv = raw_input("Please type the full name, including .csv extension of the file which contains the points you want to test, then hit enter: ") #Prompt user to enter point file
    if user_PointCsv.endswith('.csv') and os.path.exists(user_PointCsv): #Checks if relevant file type (.csv) entered and if the file exists
        file_loaded = True #Switch boolean variable status following a user entered file
    else: #If file not a .csv or does not exist, inform the user and prompt again
        print "" #Splits up the prompt text
        print "INVALID POINT FILE. Please enter a valid .csv file below." #Inform the user of an invalid file entered
        print "Tip: If you're having trouble, please include the full file path. Alternatively, you might find it easier to move the point file to the same folder as this script" #Advise the user 
        print "" #Splits up the advice text before user promted to enter a file again

with open (user_PointCsv, 'r') as testingPoints:  #Open the user entered .csv file
    pointNumber=1 #Index used to show which point is being tested.
    dataReader = csv.reader(testingPoints) #Variable to read the contents of a .csv file
    skip_Header = dataReader.next() #Skips the first row of the point file 
    for line in dataReader: #Iterates through the csv file
        tpoint=Point(x=line[0],y=line[1]) #Creates a variable for the first test point
        if myPolygon.testBoundingBox(tpoint) == 0: #Test if point is within the bounding box
            print "Point " + str(pointNumber) + " is not within the bounding box and therefore, definitely not inside the polygon." #Prints point is outside of the bounding box
            outside_BoundingBoxX.append(tpoint.x) #Appends the X coordinate of the point to the empty outside_BoundingBoxX list
            outside_BoundingBoxY.append(tpoint.y) #Appends the Y coordinate of the point to the empty outside_BoundingBoxY list
        else:
                if myPolygon.testPointInPoly(tpoint) == "Boundary": #Test if point is on the polygon boundary
                    print "Point " + str(pointNumber) + " is on the polygon boundary." #Prints point is on the polygon boundary
                    boundary_PolyX.append(tpoint.x) #Append the X coordinate of the point to the empty boundary_PolyX list
                    boundary_PolyY.append(tpoint.y) #Append the Y coordinate of the point to the empty boundary_PolyY list
                elif myPolygon.testPointInPoly(tpoint) == "Vertex": #Test if point is on the polygon vertices
                    print "Point " + str(pointNumber) + " is on the vertex of the polygon boundary." #Prints point is on vertex of a polygon
                    on_verticesX.append(tpoint.x) #Append the X coordinate of the point to the empty on_verticesX list
                    on_verticesY.append(tpoint.y) #Append the Y coordinate of the point to the empty on_verticesY list
                elif myPolygon.testPointInPoly(tpoint) == "inside": #Test if point is within the polygon 
                    print "Point " + str(pointNumber) + " is inside the polygon." #Prints the point is inside the polygon
                    inside_PolyX.append(tpoint.x) #Append the X coordinate of the point to the empty inside_PolyX list
                    inside_PolyY.append(tpoint.y) #Append the Y coordinate of the point to the empty inside_PolyY list
                else: #If point is not inside the polygon, outside the bounding box, or on the polygon vertices or boundary, it must be outside the polygon (but within bounding box)
                    print "Point " + str(pointNumber) + " is outside the polygon." #Prints point is outside of the polygon 
                    outside_PolyX.append(tpoint.x) #Append the X coordinate of the point to the empty outside_PolyX list
                    outside_PolyY.append(tpoint.y) #Append the Y coordinate of the point to the empty outside_PolyY list
        pointNumber=pointNumber+1 #Maintains point count
    del skip_Header, dataReader, pointNumber, line #Delete temporary variables used in determining point position

#Adapted from: matplotlib development team (2017):
#https://matplotlib.org/gallery/event_handling/ginput_manual_clabel_sgskip.html#sphx-glr-gallery-event-handling-ginput-manual-clabel-sgskip-py
#https://matplotlib.org/api/colors_api.html
#https://matplotlib.org/users/legend_guide.html  
polygonPlot,=plt.plot(myPolygon.coords[:,0],myPolygon.coords[:,1],'k') #Plot the polygon with a black line
polygonPlot,=plt.fill(myPolygon.coords[:,0],myPolygon.coords[:,1],'k') #Fill the polygon with black 
polygonPlot,=plt.plot([myPolygon.minX, myPolygon.minX, myPolygon.maxX, myPolygon.maxX,myPolygon.minX],
                      [myPolygon.minY, myPolygon.maxY,myPolygon.maxY,myPolygon.minY,myPolygon.minY],'r-',linewidth=2.5) #Plot the bounding box in red
outsideBBPoints, =plt.plot(outside_BoundingBoxX, outside_BoundingBoxY, 'mo', ms = 10) #Plot the points outside the bounding box as purple circles
pointsOutside, =plt.plot(outside_PolyX, outside_PolyY, 'ro', ms=10) #Plot the points that are outside the polygon as red circles
boundaryPoints, = plt.plot(boundary_PolyX, boundary_PolyY, 'bo', ms = 10) #Plot the points that on the boundary of the polygon as dark blue circles
verticesPoints, =plt.plot(on_verticesX, on_verticesY, 'co', ms = 10) #Plot the points that are on the vertices of the polygon as cyan (light blue) circles
pointsInside, =plt.plot(inside_PolyX,inside_PolyY,'go', ms=10) #Plot the points that are inside the polygon as green circles
plt.axis([myPolygon.minX-6,myPolygon.maxX+6,myPolygon.minY-6,myPolygon.maxY+6]) #Alter plot extent
plt.xlabel("X axis") #Label the X axis
plt.ylabel("Y axis") #Label the Y axis
plt.legend([outsideBBPoints,pointsOutside,boundaryPoints, verticesPoints,pointsInside], #Plot the legend variables
           ["Outside bounding box","Outside polygon","Polygon boundary","Polygon vertex","Inside polygon"], #Label the legend variables
           numpoints = 1, loc=4, shadow=True, prop={'size':10}) #Alter the appearance of the legend
plt.show() #Make the plot and legend visible to the user

