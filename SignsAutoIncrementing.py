import arcpy

trafficSignal_fc = r"\\san_marcos\arcfile\_Data\Connection Files\OSA Transportation.sde\Transportation.TRANSPORTATION.trTrafficSignals"
# signs_fc = r"\\san_marcos\arcfile\_Data\Connection Files\OSA Transportation.sde\Transportation.TRANSPORTATION.trSign_Inventory"
# connection_file = r"C:\Users\sipes_gene\AppData\Roaming\ESRI\Desktop10.8\ArcCatalog\OSA Transportation.sde"
connection_file = r"\\san_marcos\arcfile\_Data\Connection Files\OSA Transportation.sde"
# search_fields = ['MAXIMOID']
search_fields = ['MaximoID']
value_list = []

with arcpy.da.SearchCursor(trafficSignal_fc, search_fields) as sCursor:
    for row in sCursor:
        if row[0] is not None:
            max_id = row[0].split('SIG')
            value_list.append(int(max_id[1]))

starting_id = max(value_list) + 1


edit = arcpy.da.Editor(connection_file)
edit.startEditing(True, True)
edit.startOperation()
with arcpy.da.UpdateCursor(trafficSignal_fc, search_fields) as uCursor:
    for row in uCursor:
        if row[0] is None:
            id_string = "SIG" + str(starting_id)
            insert_values = [id_string]
            uCursor.updateRow(insert_values)
            starting_id += 1
edit.stopOperation()
edit.stopEditing(True)
print("I am finished")
