md_scripts
==========

Data Processing &amp; ArcGIS Scripts
Just some basic scripts I've been developing in Python for ArcGIS to intersect various sea level rise 
scenario shapefiles with whatever "assets" are of interest. 

<accessibility_script.py: 
Accessibility script applies either an exponential decay function to calculate total zonal accessiblity of every zone or a gravity function, it uses numpy matrix calculation. 

<Faster_Point_Intersection:
This is an arcpy script to inersect any feature class and add a column indicating a binary 1 if it intersects the layers passed in the slr_list.

<Poly_Line_Intersect:
This is an arcpy script hat intersects feature class and runs a tabulate intersection, it creates a single table of intersected areas or lengths for all layers passed in the slr_list.


This work is related to my thesis, I hope to finalize, clean and "package" these scripts for other in the next few months. 
