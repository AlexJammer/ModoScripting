#!/usr/bin/env python
import modo


def rename_hierarchy(modo_scene):
    PolyList = set()
    SubdList = set()

    for bone in modo_scene.selectedByType("locator"):
        selected_item_name = bone.name

        parentheses_deleted = False
        if selected_item_name[-1] == ')':  # Check if the name has a '(2)' style duplication.
            old_name = selected_item_name  # Preserve the old name for logging.

            size = len(selected_item_name)
            selected_item_name = selected_item_name[:size - 3]  # Delete the parenthesis.

            parentheses_deleted = True

        if '_l_' in selected_item_name:
            old_name = selected_item_name  # Preserve the old name for logging.

            selected_item_name = selected_item_name.replace('_l_', '_r_')  # Replace left for right.

            bone.name = selected_item_name  # Rename the item.

            print(f'Renamed {old_name} to {selected_item_name}')

        else:
            if parentheses_deleted:
                bone.name = selected_item_name  # Rename the item.
                print(f'Renamed {old_name} to {selected_item_name}')
            else:
                print(f"item {selected_item_name} doesn't need to be renamed.")


rename_hierarchy(modo.Scene())
