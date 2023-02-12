#!/usr/bin/env python
import lx
import modo
import os


def detect_subd(modo_scene):
    """
    From the user's selection, detect which meshs are in sub-d mode and which are in polygon mode. Return two lists.
    :param modo_scene: Modo scene for context.
    :return PolyList: List of models in polygon mode.
    :return SubdList: List of models in sub-d mode.
    """
    PolyList = set()
    SubdList = set()

    for mesh in modo_scene.selectedByType("mesh"):
        PolyList.add(mesh)
        for polygon in mesh.geometry.polygons.iterByType("SUBD"):
            if polygon:
                SubdList.add(mesh)
        for polygon in mesh.geometry.polygons.iterByType("PSUB"):
            if polygon:
                SubdList.add(mesh)

    if SubdList:
        if PolyList:
            for item in SubdList:
                PolyList.remove(item)

    return PolyList, SubdList

# Launch a dialog box to ask the user where to export the final FBX.
lx.eval('dialog.setup dir')
lx.eval('dialog.title "Export Path"')
lx.eval('dialog.msg "Select path to export to."')

try:
    lx.eval('dialog.open')

except:
    pass

else:
    output_dir = lx.eval1("dialog.result ?")

    PolyList, SubdList = detect_subd(modo.Scene())  # From the selected models, detect which ones are in sub-d mode and
                                                    # which ones are in polygon mode. Return the lists.

    duplicated_list = []

    for item in SubdList:
        new_item = modo.Scene().duplicateItem(item, instance=False)
        modo.Scene().select(new_item)
        lx.eval("poly.freeze face")
        duplicated_list.append(new_item)
        # lx.eval("item.duplicate")
        # for duplicated_item in modo.Scene().selectedByType("mesh"):
        #     lx.eval("poly.freeze face")
        #     duplicated_list.append(duplicated_item)

    SubdList.clear()

    for item in duplicated_list:
        SubdList.add(item)

    modo.Scene().deselect

    for item in PolyList:
        modo.Scene().select(item, True)
    for item in SubdList:
        modo.Scene().select(item, True)

    filename = os.path.basename(modo.Scene().filename)
    filepath = os.path.join(output_dir, os.path.splitext(filename)[0] + ".fbx")

    lx.eval('!scene.saveAs "%s" fbx true' % filepath)
    for item in SubdList:
        modo.Scene().removeItems(item)
