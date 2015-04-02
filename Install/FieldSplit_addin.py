#!/usr/bin/python
# -*-coding:utf-8-*-
import arcpy
import os
import pythonaddins
import time


global fieldFilter
fieldFilter = ""
class ButtonProcess(object):
    """Implementation for FieldSplit_addin.buttonProcess (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        global featureLayer
        global field
        global fieldFilter

        if len(fieldFilter) != 0:
            ''' filter not empty '''
            rows = arcpy.SearchCursor(featureLayer)
            isFilterInRow = False
            for row in rows:
                if fieldFilter in row.getValue(field):
                    isFilterInRow = True
            if isFilterInRow is False:
                pythonaddins.MessageBox(u"所选字段: %s 不包含: %s" % (field, fieldFilter), u"过滤字段错误", 1)
            else:
                splitFeatureWithFilter(featureLayer, field, fieldFilter)
        else:
            rows = arcpy.SearchCursor(featureLayer)
            rowSet = set()
            for row in rows:
                rowSet.add(row.getValue(field))
            if len(rowSet) < 10 or (
                        pythonaddins.MessageBox(u"所选字段种类: %d,\n是否继续生成" % len(rowSet), u"所选字段种类大于10", 1) is "Ok"):
                del row
                print featureLayer.name + ", " + field
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


class ComboBoxFieldFilter(object):
    """Implementation for FieldSplit_addin.comboboxFidlds (ComboBox)"""

    def __init__(self):
        self.items = []
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWWWWWWWW'
        self.width = 'WWWWWWWWWWWW'

    def onSelChange(self, selection):
        pass

    def onEditChange(self, text):
        global fieldFilter
        fieldFilter = text
        print text
        pass

    def onFocus(self, focused):
        pass

    def onEnter(self):
        pass

    def refresh(self):
        pass


def splitFeature(featureClass, field, rowSet):
    featureType = arcpy.Describe(featureClass).featureClass.shapeType
    featureClassOutDict = dict()
    nowTime = time.strftime('_%y%m%d_%H%I%M_', time.localtime(time.time()))
    for row in rowSet:
        print featureClass.name + "," + featureClass.dataSource + "," + row + "," + featureType + "," + nowTime + "," + \
              os.path.split(featureClass.dataSource)[0]
        arcpy.CreateFeatureclass_management(os.path.split(featureClass.dataSource)[0] + "\\",
                                            featureClass.name + nowTime + row,
                                            featureType, featureClass)
        featureClassOutDict[row] = arcpy.InsertCursor(
            os.path.split(featureClass.dataSource)[0] + "\\" + featureClass.name + nowTime + row + ".shp")
    rows = arcpy.SearchCursor(featureClass)
    for row in rows:
        featureClassOutDict[row.getValue(field)].insertRow(row)
    pass


def splitFeatureWithFilter(featureClass, field, fieldFilter):
    featureType = arcpy.Describe(featureClass).featureClass.shapeType
    nowTime = time.strftime('_%y%m%d_%H%I%M_', time.localtime(time.time()))
    arcpy.CreateFeatureclass_management(os.path.split(featureClass.dataSource)[0] + "\\", featureClass.name + nowTime + fieldFilter, featureType, featureClass)
    featureClassOut = arcpy.InsertCursor(os.path.split(featureClass.dataSource)[0] + "\\" + featureClass.name + nowTime + fieldFilter + ".shp")
    rows = arcpy.SearchCursor(featureClass)
    for row in rows:
        if fieldFilter in row.getValue(field):
            featureClassOut.insertRow(row)
    pass
