# Point-in-Polygon

The code contained in this repository was created as part of the assessment for <b>CEGEG082: GIS Principles & Technology</b>, as part of the MSc Geographic Information Science (GIS) course at University College London. 

The code is designed to determine if a point or points lies inside or outside of a polygon using the popular Ray-Casting Algorithm.
Before running the code, the user should set their working directory by appropriately editing the relevant line of code (as prompted in the comments).

The programme requires the user to input the file name of the .csv files which store the polygon and point information being used to test this algorithm.
You will be prompted to type the full file name and extension (.csv). The programme will then check this file exists before loading it.
You are first promted to supply the polygon file. If this is successful, you are promted to supply the point file.


The code determines if a point is positioned:

1) Outside of a bounding box (as determined by the minimum and maximum polygon coordinates supplied by the user .csv file).

2) Outside the polygon (but in this case, inside the bounding box).

3) On the boundary of the polygon.

4) On the vertices of the polygon (angular point of the polygon).

5) Inside the polygon.

Relevant documentation and sources are commented throughout.

### Additional Notes
Please ensure the polygon and point file are entered in the correct order.
This user input handles all errors apart from when the point file is incorrectly entered as the polygon file (due to the header). In this case, an error occurs and the script needs to be re-run. 
