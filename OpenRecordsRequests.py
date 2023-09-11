# Import ArcPy site-package and os modules
import arcpy
import os

# Connection root folder
rootFolder = r"\\san_marcos\arcfile\_Data\Connection Files"

# List of data connections
connections = [
    # rootFolder + "\OSA WWWW",
    r"\\san_marcos\arcfile\_Data\Connection Files\OSA Transportation.sde",
    # rootFolder + "\OSA DS",
    # rootFolder + "\OSA Electric",
]


# Set the clip featureclass
clipFeatures = r"\\san_marcos\arcfile\Department Projects and File Geodatabases\Public Services\Transportation\GSipes\ProProjects\OpenRecordsRequests\OpenRecordsRequests.gdb\SelectionPoly"

# Set the directory path where the clipped shapefiles will be stored
path = r"C:\Users\sipes_gene\Documents\OpenRecords"

# script will ask user to enter new folder name, folder will be place in path
outFolder = input('Enter your folder name :')

# join the path to the new folder name
outWorkspace = os.path.join(path, outFolder)

# Set the XY tolerance of the clip function
clusterTolerance = .000378

# create the new open records folder


try:

    for conn in connections:
        arcpy.env.workspace = conn
        print(conn)
    # Get a list of the featureclasses in the input folder
        fcs = arcpy.ListFeatureClasses()

        for fc in fcs:
            if fc != 'WaterWW.UTILITY.waMeter_old':
                # Validate the new feature class name for the output workspace.
                featureClassName = arcpy.ValidateTableName(fc, outWorkspace)
                outFeatureClass = os.path.join(outWorkspace, featureClassName)
                arcpy.MakeFeatureLayer_management(fc, fc)
                arcpy.SelectLayerByLocation_management(
                    fc, "within", clipFeatures)
                count = int(arcpy.GetCount_management(fc)[0])
                if count == 0:
                    print("%s features do not exist within AOI" % fc)
                else:

                    # Clip each feature class in the list with the clip feature class.
                    # looks for clip feature so as not to clip it.
                    # if fc != os.path.basename(clipFeatures):
                    arcpy.Clip_analysis(
                        fc, clipFeatures, outFeatureClass, clusterTolerance)
                    print("{} {} features clipped to AOI".format(count, format))
    print("All is well in the Universe, good bye")


except Exception as err:
    arcpy.AddError(err)
    print(err)
