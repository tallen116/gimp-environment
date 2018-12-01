#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Plug-in:      Create Layer Mask from...
# Version:      1.0
# Date:         29.08.2012
# Copyright:    Dmitry Dubyaga <dmitry.dubyaga@gmail.com>      
# Tested with:  GIMP 2.8
# ----------------------------------

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#  
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#  
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gimpfu import *

def show_message(m_id):
    messages = []
    messages.append("Can only be called on a layer, not on a mask.")
    messages.append("The layer is not selected.")
    pdb.gimp_message(messages[m_id])
    return

def python_fu_create_layer_mask(image, drawable, donor, transfer_type, selection_mode = 2, remove_source = True):
    gimp.context_push()
    image.undo_group_start()

    pdb.gimp_message_get_handler(ERROR_CONSOLE)
    
    if pdb.gimp_item_is_layer_mask(drawable):
        show_message(0)
        image.undo_group_end()
        gimp.context_pop()
        return
    if not pdb.gimp_item_is_layer(drawable):
        show_message(1)
        image.undo_group_end()
        gimp.context_pop()
        return

    donor_mask = pdb.gimp_layer_get_mask(donor)
    drawable_mask = pdb.gimp_layer_get_mask(drawable)
    
    pdb.gimp_selection_none(image)
    if donor_mask != None:
        pdb.gimp_image_select_item(image, CHANNEL_OP_ADD, donor_mask)
        if transfer_type != 'white_mask':
            pdb.gimp_selection_invert(image)
        donor_channel = pdb.gimp_selection_save(image)
        if drawable_mask != None:
            pdb.gimp_selection_none(image)
            pdb.gimp_image_select_item(image, CHANNEL_OP_ADD, drawable_mask)
            pdb.gimp_image_select_item(image, selection_mode, donor_channel)
            pdb.gimp_layer_remove_mask(drawable, MASK_DISCARD)
        created_mask = pdb.gimp_layer_create_mask(drawable, ADD_SELECTION_MASK)
        pdb.gimp_layer_add_mask(drawable, created_mask)
        pdb.gimp_selection_none(image)
        pdb.gimp_image_remove_channel(image, donor_channel)
        if remove_source:
            pdb.gimp_image_remove_layer(image, donor)
    else:
        donor_mask = pdb.gimp_layer_create_mask(donor, ADD_COPY_MASK)
        pdb.gimp_layer_add_mask(donor, donor_mask)
        pdb.gimp_image_select_item(image, CHANNEL_OP_ADD, donor_mask)
        pdb.gimp_layer_remove_mask(donor, MASK_DISCARD)
        if transfer_type != 'white_mask':
            pdb.gimp_selection_invert(image)
        donor_channel = pdb.gimp_selection_save(image)
        if drawable_mask != None:
            pdb.gimp_selection_none(image)
            pdb.gimp_image_select_item(image, CHANNEL_OP_ADD, drawable_mask)
            pdb.gimp_image_select_item(image, selection_mode, donor_channel)
            pdb.gimp_layer_remove_mask(drawable, MASK_DISCARD)
        created_mask = pdb.gimp_layer_create_mask(drawable, ADD_SELECTION_MASK)
        pdb.gimp_layer_add_mask(drawable, created_mask)
        pdb.gimp_selection_none(image)
        pdb.gimp_image_remove_channel(image, donor_channel)
        if remove_source:
            pdb.gimp_image_remove_layer(image, donor)

    gimp.displays_flush()
    image.undo_group_end()
    gimp.context_pop()    
    return

register (
    "python-fu-create-layer-mask",
    "Create Layer Mask from...\nVersion 1.0",
    "Create Layer Mask from...\nVersion 1.0",
    "Dmirty Dubyaga",
    "Dmitry Dubyaga <dmitry.dubyaga@gmail.com>",
    "29.08.2012",
    "Create Layer Mask from...",
    "*",
    [
        (PF_IMAGE, "image", "", None),
        (PF_DRAWABLE, "drawable", "", None),        
        (PF_LAYER, "donor", "Create mask from:", None),
        (PF_RADIO, "transfer_type", "Transfer type:", "white_mask", 
            (
                ("White mask", "white_mask"),
                ("Black mask", "black_mask")
            )
        ),
        (PF_OPTION, "selection_mode", "If mask exists:", 2, ("Add", "Subtract", "Replace", "Intersect")),
        (PF_TOGGLE, "remove_source", "Remove source:", True)
    ],
    [],
    python_fu_create_layer_mask, menu = "<Image>/Layer/Mask/"
    )
register (
    "python-fu-create-layer-mask-from",
    "Create Layer Mask from...\nVersion 1.0",
    "Create Layer Mask from...\nVersion 1.0",
    "Dmirty Dubyaga",
    "Dmitry Dubyaga <dmitry.dubyaga@gmail.com>",
    "29.08.2012",
    "Create Layer Mask from...",
    "*",
    [
        (PF_IMAGE, "image", "", None),
        (PF_DRAWABLE, "drawable", "", None),        
        (PF_LAYER, "donor", "Create mask from:", None),
        (PF_RADIO, "transfer_type", "Transfer type:", "white_mask", 
            (
                ("White mask", "white_mask"),
                ("Black mask", "black_mask")
            )
        ),
        (PF_OPTION, "selection_mode", "If mask exists:", 2, ("Add", "Subtract", "Replace", "Intersect")),
        (PF_TOGGLE, "remove_source", "Remove source:", True)
    ],
    [],
    python_fu_create_layer_mask, menu = "<Layers>/"
    )

main()
