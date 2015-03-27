#!/usr/bin/python
# -*-coding:utf-8-*-
import arcpy
import os
import pythonaddins


class ButtonProcess(object):
    """Implementation for FieldSplit_addin.buttonProcess (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        global featureLayer
        global field
        rows = arcpy.SearchCursor(featureLayer)
        rowSet = set()
        for row in rows:
            rowSet.add(row.getValue(field))
        if len(rowSet) < 10 or (pythonaddins.MessageBox(u"所选字段种类: %d,\n是否继续生成" % len(rowSet), u"所选字段种类大于10", 1) is "Ok"):
            del row
            splitFeature(featureLayer, field, rowSet)


class ComboBoxFeatureClass(object):
    """Implementation for FieldSplit_addin.comboboxFeatureClass (ComboBox)"""

    def __init__(self):
        self.items = []
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWWWWWWWW'
        self.width = 'WWWWWWWWWWWW'

    def onSelChange(self, selection):
        global featureLayer
        global mxd
        featureLayer = arcpy.mapping.ListLayers(mxd, selection)[0]
        pass

    def onEditChange(self, text):
        pass

    def onFocus(self, focused):
        global mxd
        self.items = []
        mxd = arcpy.mapping.MapDocument('current')
        layers = arcpy.mapping.ListLayers(mxd)
        for layer in layers:
            self.items.append(layer.name)
        pass

    def onEnter(self):
        pass

    def refresh(self):
        pass


class ComboBoxFields(object):
    """Implementation for FieldSplit_addin.comboboxFidlds (ComboBox)"""

    def __init__(self):
        self.items = []
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWWWWWWWW'
        self.width = 'WWWWWWWWWWWW'

    def onSelChange(self, selection):
        global field
        field = selection
        pass

    def onEditChange(self, text):
        pass

    def onFocus(self, focused):
        self.items = []
        global featureLayer
        fields = arcpy.ListFields(featureLayer)
        for field in fields:
            self.items.append(field.aliasName)
        pass

    def onEnter(self):
        pass

    def refresh(self):
        pass


def splitFeature(featureClass, field, rowSet):
    featureType = arcpy.Describe(featureClass).featureClass.shapeType
    featureClassOutDict = dict()
    for row in rowSet:
        # if  row is " ":
        # row = "Space"
        # if  row is "":
        #     row = "Empty"
        arcpy.CreateFeatureclass_management(os.path.split(featureClass.dataSource)[0], featureClass.name + "_" + row,
                                            featureType, featureClass)
        # locals()["outFeature_%s" % row] = os.path.split(featureClass.dataSource)[0] + "\\" + featureClass.name + "_" + row
        featureClassOutDict[row] = arcpy.InsertCursor(
            os.path.split(featureClass.dataSource)[0] + "\\" + featureClass.name + "_" + row + ".shp")
    rows = arcpy.SearchCursor(featureClass)
    for row in rows:
        featureClassOutDict[row.getValue(field)].insertRow(row)
    pass
