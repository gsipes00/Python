
import arcpy
import pythonaddins
import os
from os.path import expanduser



class ToolClass2(object):
    """Implementation for ExportShapeOnRectangle_addin.tool (Tool)"""
    def __init__(self):
        self.enabled = True
        self.cursor = 3
        self.shape = "Rectangle" # Can set to "Line", "Circle" or "Rectangle" for interactive shape drawing and to activate the onLine/Polygon/Circle event sinks.

#The following code executes upon release of the left mouse click that draws the rectangle.
    def onRectangle(self, rectangle_geometry):
        extent = rectangle_geometry
        home = expanduser("~")
        
        pathCheck = os.path.isdir(home + "\Documents\\" + "OutShapefiles")
        if pathCheck is True:
            pass
        else:
            os.mkdir(home + "\Documents\\" + "OutShapefiles")
        
        arcpy.env.workspace = home + "\Documents\\" + "OutShapefiles\\"
        arcpy.env.overwriteOutput = True

        a = arcpy.Array()
        a.add(extent.lowerLeft)
        a.add(extent.lowerRight)
        a.add(extent.upperRight)
        a.add(extent.upperLeft)
        a.add(extent.lowerLeft)
        boundary_poly = arcpy.Polygon(a)


        mxd = arcpy.mapping.MapDocument("Current")
        lyrList = arcpy.mapping.ListLayers(mxd)
        for lyr in lyrList:
            if lyr.visible is True:

                if '.' in lyr.name:
                    name_split = lyr.name.split('.')
                    out_shp = os.path.join(arcpy.env.workspace, str(name_split[2]) + '_copy')
                    print("Found period in name and split")
                else:
                    out_shp = (os.path.join(arcpy.env.workspace, str(lyr)) + '_Copy')
                    print("Did't find a period in name, using name as is in TOC.")
                arcpy.SelectLayerByLocation_management(lyr, 'Intersect', boundary_poly, 0, 'New_Selection')
                shapeLoc = out_shp + ".shp"
                print("Checking to see if layer already exists.")

                if arcpy.Exists(shapeLoc):
                    arcpy.Delete_management(shapeLoc)
                    print ("Duplicate shapefile " + str(lyr) + " found. " + "Deleted the shapefile from" + str(shapeLoc))
                    print ("Copying new shapefile to folder now")
                else:
                    print ("Did not find duplicate shapefile in folder destination")
                    print ("Copying new shapefile to folder now.")
                arcpy.CopyFeatures_management(lyr, out_shp)
                # arcpy.SelectLayerByLocation_management(lyr, "CLEAR_SELECTION")
                arcpy.RefreshActiveView()

        print("Finished copying all shapefiles.")
        result = pythonaddins.MessageBox("Copied files to " + arcpy.env.workspace, "Progress Report","0")
        print (result)
