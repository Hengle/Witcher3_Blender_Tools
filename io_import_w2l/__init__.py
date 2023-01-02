import os
from pathlib import Path

from io_import_w2l.setup_logging_bl import *
log = logging.getLogger(__name__)

def get_uncook_path(context) -> str:
    addon_prefs = context.preferences.addons[__package__].preferences
    uncook_path = addon_prefs.uncook_path
    return uncook_path

def get_fbx_uncook_path(context) -> str:
    addon_prefs = context.preferences.addons[__package__].preferences
    fbx_uncook_path = addon_prefs.fbx_uncook_path
    return fbx_uncook_path

def get_texture_path(context) -> str:
    addon_prefs = context.preferences.addons[__package__].preferences
    tex_uncook_path = addon_prefs.tex_uncook_path
    return tex_uncook_path

def get_modded_texture_path(context) -> str:
    addon_prefs = context.preferences.addons[__package__].preferences
    tex_mod_uncook_path = addon_prefs.tex_mod_uncook_path
    return tex_mod_uncook_path

def get_W3_VOICE_PATH(context) -> str:
    addon_prefs = context.preferences.addons[__package__].preferences
    W3_VOICE_PATH = addon_prefs.W3_VOICE_PATH
    return W3_VOICE_PATH

def get_W3_OGG_PATH(context) -> str:
    addon_prefs = context.preferences.addons[__package__].preferences
    W3_OGG_PATH = addon_prefs.W3_OGG_PATH
    return W3_OGG_PATH

def get_W3_FOLIAGE_PATH(context) -> str:
    addon_prefs = context.preferences.addons[__package__].preferences
    W3_FOLIAGE_PATH = addon_prefs.W3_FOLIAGE_PATH
    return W3_FOLIAGE_PATH

def get_W3_REDCLOTH_PATH(context) -> str:
    addon_prefs = context.preferences.addons[__package__].preferences
    W3_REDCLOTH_PATH = addon_prefs.W3_REDCLOTH_PATH
    return W3_REDCLOTH_PATH

def get_use_fbx_repo(context) -> str:
    addon_prefs = context.preferences.addons[__package__].preferences
    use_fbx_repo = addon_prefs.use_fbx_repo
    return use_fbx_repo

from io_import_w2l import CR2W
from io_import_w2l.CR2W.w3_types import CSkeletalAnimationSetEntry
from io_import_w2l.CR2W.dc_anims import load_lipsync_file
#from io_import_w2l.importers import *
from io_import_w2l.importers import (
                                    import_anims,
                                    import_rig,
                                    import_w2l,
                                    import_mesh,
                                    import_w2w,
                                    import_texarray
                                    )
from io_import_w2l.exporters import (
                                    export_anims
                                    )
from io_import_w2l import constrain_util
from io_import_w2l import file_helpers
from io_import_w2l.cloth_util import setup_w3_material_CR2W


#ui
from io_import_w2l.ui import ui_map
from io_import_w2l.ui.ui_map import (WITCH_OT_w2L,
                                     WITCH_OT_w2w,
                                     WITCH_OT_load_layer,
                                     WITCH_OT_load_layer_group,
                                     WITCH_OT_radish_w2L)
from io_import_w2l.ui import ui_anims
from io_import_w2l.ui import ui_entity
from io_import_w2l.ui import ui_morphs
from io_import_w2l.ui.ui_morphs import (WITCH_OT_morphs)

from io_import_w2l.ui import ui_voice
from io_import_w2l.ui import ui_mimics
from io_import_w2l.ui import ui_anims_list
from io_import_w2l.ui import ui_import_menu
from io_import_w2l.ui.ui_mesh import WITCH_OT_w2mesh, WITCH_OT_apx
from io_import_w2l.ui.ui_utils import WITCH_PT_Base
from io_import_w2l.ui.ui_entity import WITCH_OT_ENTITY_lod_toggle
#from io_import_w2l.ui.ui_entity import WITCH_OT_w2ent_chara

import bpy
from bpy.types import (Panel, Operator)
from bpy.props import StringProperty, BoolProperty
from mathutils import Vector
from bpy_extras.io_utils import ImportHelper, ExportHelper
import addon_utils

bl_info = {
    "name": "Witcher 3 Tools",
    "author": "Dingdio",
    "version": (0, 5),
    "blender": (3, 3, 0),
    "location": "File > Import-Export > Witcher 3 Assets",
    "description": "Tools for Witcher 3",
    "warning": "",
    "doc_url": "https://github.com/dingdio/Witcher3_Blender_Tools",
    "category": "Import-Export"
}

class Witcher3AddonPrefs(bpy.types.AddonPreferences):
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __package__

    uncook_path: StringProperty(
        name="Uncook Path",
        subtype='DIR_PATH',
        default="E:\\w3.modding\\modkit_new\\r4data",#'E:\\w3.modding\\modkit\\r4data',
        description="Path where you uncooked the game files."
    )

    fbx_uncook_path: StringProperty(
        name="Uncook Path FBX (.fbx)",
        subtype='DIR_PATH',
        default='E:\\w3_uncook\\FBXs',
        description="Path where you exported the FBX files."
    )

    tex_uncook_path: StringProperty(
        name="Uncook Path TEXTURES (.tga)",
        subtype='DIR_PATH',
        default='E:\\w3_uncook',#"E:\\w3_uncook_new",#
        description="Path where you exported the tga files."
    )

    tex_mod_uncook_path: StringProperty(
        name="(optional) Uncook Path modded TEXTURES (.tga)",
        subtype='DIR_PATH',
        default='E:\\w3.modding\\modkit\\modZOldWitcherArmour',
        description="(optional) Path where you exported the tga files from a mod."
    )

    W3_FOLIAGE_PATH: StringProperty(
        name="Uncook Path FOLIAGE (.fbx)",
        subtype='DIR_PATH',
        default='E:\\w3_uncook\\FBXs\\FOLIAGE',
        description="Path where you exported the fbx files."
    )

    W3_REDCLOTH_PATH: StringProperty(
        name="Uncook Path REDCLOTH (.apx)",
        subtype='DIR_PATH',
        default='E:\\w3_uncook\\FBXs\\REDCLOTH',
        description="Path where you exported the apx files."
    )

    W3_REDFUR_PATH: StringProperty(
        name="Uncook Path REDFUR (.apx)",
        subtype='DIR_PATH',
        default='E:\\w3_uncook\\FBXs\\REDFUR',
        description="Path where you exported the apx files."
    )

    W3_VOICE_PATH: StringProperty(
        name="Extracted lipsync (.cr2w)",
        subtype='DIR_PATH',
        default='E:\\w3.modding\\radish-tools\\docs.speech\\enpc.w3speech-extracted_GOOD\\enpc.w3speech-extracted',
        description="Path where you extracted w3speech"
    )

    W3_OGG_PATH: StringProperty(
        name="Converted .wem files (.ogg)",
        subtype='DIR_PATH',
        default='F:\\voice_synth\\witcher\\speech\\ogg',
        description="Path with ogg files"
    )

    #keep_lod_meshes: bpy.props.BoolProperty(name="Keep lod meshes", default = False)
    use_fbx_repo: bpy.props.BoolProperty(name="Use FBX repo",
                                        default=False,
                                        description="Enable this to load from the fbx repo when importing meshes, maps etc.")

    #importFacePoses
    def draw(self, context):
        layout = self.layout
        layout.label(text="Witcher 3 Mesh settings:")
        layout.prop(self, "use_fbx_repo")
        layout.label(text="Witcher 3 Tools settings:")
        layout.prop(self, "uncook_path")
        layout.prop(self, "fbx_uncook_path")
        layout.prop(self, "tex_uncook_path")
        layout.prop(self, "W3_FOLIAGE_PATH")
        layout.prop(self, "W3_REDCLOTH_PATH")
        layout.prop(self, "W3_REDFUR_PATH")
        layout.prop(self, "W3_VOICE_PATH")
        layout.prop(self, "W3_OGG_PATH")

class WITCH_OT_w2mi(bpy.types.Operator, ImportHelper):
    """Load Witcher 3 Material Instance"""
    bl_idname = "witcher.import_w2mi"
    bl_label = "Import .w2mi"
    filename_ext = ".w2mi"
    filter_glob: StringProperty(default='*.w2mi', options={'HIDDEN'})
    do_update_mats: BoolProperty(
        name="Material Update",
        default=True,
        description="If enabled, it will replace the material with same name instead of creating a new one"
    )
    def execute(self, context):
        print("importing material instance now!")
        fdir = self.filepath
        if os.path.isdir(fdir):
            self.report({'ERROR'}, "ERROR File Format unrecognized, operation cancelled.")
            return {'CANCELLED'}
        ext = file_helpers.getFilenameType(fdir)
        if ext == ".w2mi":
            bpy.ops.mesh.primitive_plane_add()
            obj = bpy.context.selected_objects[:][0]
            instance_filename = Path(fdir).stem
            materials = []
            material_file_chunks = CR2W.CR2W_reader.load_material(fdir)
            for idx, mat in enumerate(material_file_chunks):
                # if idx > 0:
                #     raise Exception('wut')
                target_mat = False
                if self.do_update_mats:
                    if instance_filename in obj.data.materials:
                        target_mat = obj.data.materials[instance_filename] #None
                    if instance_filename in bpy.data.materials:
                        target_mat = bpy.data.materials[instance_filename] #None
                if not target_mat:
                    target_mat = bpy.data.materials.new(name=instance_filename)

                finished_mat = setup_w3_material_CR2W(get_texture_path(context), target_mat, mat, force_update=True, mat_filename=instance_filename, is_instance_file = False)

                if instance_filename in obj.data.materials and not self.do_update_mats:
                    obj.material_slots[target_mat.name].material = finished_mat
                else:
                    obj.data.materials.append(finished_mat)
        else:
            self.report({'ERROR'}, "ERROR File Format unrecognized, operation cancelled.")
            return {'CANCELLED'}
        return {'FINISHED'}

class WITCH_OT_w2ent(bpy.types.Operator, ImportHelper):
    """Load Witcher 3 Entity File"""
    bl_idname = "witcher.import_w2ent"
    bl_label = "Import .w2ent"
    filename_ext = ".w2ent, flyr"
    def execute(self, context):
        print("importing entity now!")
        fdir = self.filepath
        if os.path.isdir(fdir):
            self.report({'ERROR'}, "ERROR File Format unrecognized, operation cancelled.")
            return {'CANCELLED'}
        ext = file_helpers.getFilenameType(fdir)
        if ext == ".flyr":
            foliage = CR2W.CR2W_reader.load_foliage(fdir)
            import_w2l.btn_import_w2ent(foliage)
        elif ext == ".w2ent":
            entity = CR2W.CR2W_reader.load_entity(fdir)
            import_w2l.btn_import_w2ent(entity)
        else:
            self.report({'ERROR'}, "ERROR File Format unrecognized, operation cancelled.")
            return {'CANCELLED'}
        return {'FINISHED'}

class WITCH_OT_ViewportNormals(bpy.types.Operator):
    bl_description = "Switch normal map nodes to a faster custom node. Get https://github.com/theoldben/BlenderNormalGroups addon to enable button"
    bl_idname = 'witcher.normal_map_group'
    bl_label = "Normal Map nodes to Custom"
    bl_options = {'UNDO'}

    @classmethod
    def poll(self, context):
        (exist, enabled) = addon_utils.check("normal_map_to_group")
        return enabled

    def execute(self, context):
        bpy.ops.node.normal_map_group()
        return {'FINISHED'}

class WITCH_OT_AddConstraints(bpy.types.Operator):
    """Add Constraints"""
    bl_idname = "witcher.add_constraints"
    bl_label = "Add Constraints"
    bl_description = "Object Mode. Create bone constraints based on same bone names or r_weapon/l_weapon bones. Select Armature then Ctrl+Select Armature you want to attach to it"
    action: StringProperty(default="default")
    def execute(self, context):
        scene = context.scene
        action = self.action
        if action == "add_const":
            constrain_util.do_it(1)
        if action == "add_const_ik":
            constrain_util.do_it(2)
        elif action == "attach_r_weapon":
            constrain_util.attach_weapon("r_weapon")
        elif action == "attach_l_weapon":
            constrain_util.attach_weapon("l_weapon")
        return {'FINISHED'}

class WITCH_OT_ImportW2Rig(bpy.types.Operator, ImportHelper):
    """Load Witcher 3 .w2rig file or .w2rig.json"""
    bl_idname = "witcher.import_w2_rig"
    bl_label = "Import .w2rig"
    filename_ext = ".w2rig, .w2rig.json; w3dyny"
    bl_options = {'REGISTER', 'UNDO'}

    filter_glob: StringProperty(default='*.w2rig;*.w2rig.json;*.w3dyng;*.w3dyng.json', options={'HIDDEN'})

    do_fix_tail: BoolProperty(
        name="Connect bones",
        default=False,
        description="If enabled, an attempt will be made to connect tail bones. Currently this will mess up rotation of the bones and prevent applying w2anims but useful for creating IK rigs in Blender"
    )
    def execute(self, context):
        print("importing rig now!")
        fdir = self.filepath
        if os.path.isdir(fdir):
            self.report({'ERROR'}, "ERROR File Format unrecognized, operation cancelled.")
            return {'CANCELLED'}
        ext = file_helpers.getFilenameType(fdir)
        if ext == ".w2rig" or ext == ".json":
            import_rig.start_rig_import(fdir, "default", self.do_fix_tail, context=context)
        elif ext ==".w3fac":
            faceData = import_rig.loadFaceFile(fdir)
            root_bone = import_rig.create_armature(faceData.mimicSkeleton, "yes", context=context)
        return {'FINISHED'}

class WITCH_OT_ExportW2RigJson(bpy.types.Operator, ExportHelper):
    """export W2 rig Json"""
    bl_idname = "witcher.export_w2_rig"
    bl_label = "Export"
    filename_ext = ".json"
    filename = ".w2rig"
    def execute(self, context):
        obj = context.object
        fdir = self.filepath
        ext = file_helpers.getFilenameType(fdir)
        import_rig.export_w3_rig(context, fdir)
        return {'FINISHED'}

class WITCH_OT_ExportW2AnimJson(bpy.types.Operator, ExportHelper):
    """export W2 Anim Json"""
    bl_idname = "witcher.export_w2_anim"
    bl_label = "Export"
    filename_ext = ".json"
    def execute(self, context):
        obj = context.object
        fdir = self.filepath
        ext = file_helpers.getFilenameType(fdir)
        export_anims.export_w3_anim(context, fdir)
        return {'FINISHED'}

class WITCH_OT_load_texarray(bpy.types.Operator, ImportHelper):
    """WITCH_OT_load_texarray"""
    bl_idname = "witcher.load_texarray"
    bl_label = "Load texarray json"
    filename_ext = ".json"
    bl_options = {'REGISTER', 'UNDO'}

    filter_glob: StringProperty(default='*.json', options={'HIDDEN'})
    def execute(self, context):
        fdir = self.filepath
        print("Importing Material")
        if os.path.isdir(fdir):
            self.report({'ERROR'}, "ERROR File Format unrecognized, operation cancelled.")
            return {'CANCELLED'}
        else:
            import_texarray.start_import(fdir)
        return {'FINISHED'}

#----------------------------------------------------------
#   Utilities panel
#----------------------------------------------------------

class WITCH_PT_Utils(WITCH_PT_Base, bpy.types.Panel):
    bl_label = "Utilities"

    def draw(self, context):
        ob = context.object
        coll = context.collection
        scn = context.scene
        layout = self.layout
        box = layout.box()
        if ob:
            box.label(text = "Active Object: %s" % ob.entity_type)
            box.prop(ob, "name")
            if ob.template:
                box.prop(ob, "template")
            if ob.entity_type:
                box.prop(ob, "entity_type")
        else:
            box.label(text = "No active object")

        box = layout.box()
        if coll:
            box.prop(coll, "name")

            #CLayerInfo
            if coll.level_path:
                box.prop(coll, "level_path")
            if coll.layerBuildTag:
                box.prop(coll, "layerBuildTag")
            if coll.level_path:
                row = layout.row()
                row.operator(WITCH_OT_load_layer.bl_idname, text="Load This Level", icon='CUBE')

            #CLayerGroup
            if coll.group_type and coll.group_type == "LayerGroup":
                row = layout.row()
                row.operator(WITCH_OT_load_layer_group.bl_idname, text="Load This LayerGroup", icon='CUBE')
        else:
            box.label(text = "No active collection")

class WITCH_PT_Main(WITCH_PT_Base, bpy.types.Panel):
    bl_idname = "WITCH_PT_Main"
    bl_label = "Witcher 3 Tools"

    def draw(self, context):
        layout:bpy.types.UILayout = self.layout # UILayout
        #Map
        row = layout.row().box()
        row = row.column(align=True)
        row.label(text='Map Import')
        op = row.operator(WITCH_OT_w2L.bl_idname, text="Layer (.w2l)", icon='SPHERE')
        op.filepath = os.path.join(get_uncook_path(context),"levels\\")
        op = row.operator(WITCH_OT_w2w.bl_idname, text="World (.w2w)", icon='WORLD_DATA')
        op.filepath = get_uncook_path(context)+"\\levels\\"
        row.operator(WITCH_OT_load_texarray.bl_idname, text="Texarray (.json)", icon='TEXTURE_DATA')
        row = layout.row().box()
        row = row.column(align=True)
        
        row.label(text='Radish yml Export')
        op = row.operator(WITCH_OT_radish_w2L.bl_idname, text="Layer (.yml)", icon='SPHERE')
        row = layout.row().box()
        row = row.column(align=True)

        #Mesh
        row.label(text='Mesh Import')
        op = row.operator(WITCH_OT_w2mesh.bl_idname, text="Mesh (.w2mesh)", icon='MESH_DATA')
        op.filepath = get_uncook_path(context)
        op = row.operator(WITCH_OT_apx.bl_idname, text="Redcloth (.redcloth)", icon='MESH_DATA')
        op.filepath = get_uncook_path(context)

        #Mesh
        row = layout.row().box()
        row = row.column(align=True)
        row.label(text='Material Import')
        op = row.operator(WITCH_OT_w2mi.bl_idname, text="Instance (.w2mi)", icon='MESH_DATA')
        op.filepath = get_uncook_path(context)+"\\"

        #Entity
        row = layout.row().box()
        row = row.column(align=True)
        row.label(text='Entity Import')
        op = row.operator(WITCH_OT_w2ent.bl_idname, text="Items (.w2ent)", icon='SPHERE')
        op.filepath = os.path.join(get_uncook_path(context),"items\\")
        # op = row.operator(WITCH_OT_w2ent_chara.bl_idname, text="Import .w2ent (Characters)", icon='SPHERE')
        # op.filepath = os.path.join(get_uncook_path(context),"characters\\")

        #Animation
        row = layout.row().box()
        row = row.column(align=True)
        row.label(text='Animation Tools')
        row.operator(WITCH_OT_AddConstraints.bl_idname, text="Add Constraints", icon='CONSTRAINT').action = "add_const"
        row.operator(WITCH_OT_AddConstraints.bl_idname, text="Add Constraints IK", icon='CONSTRAINT').action = "add_const_ik"
        row.operator(WITCH_OT_AddConstraints.bl_idname, text="Attach to r_weapon", icon='CONSTRAINT').action = "attach_r_weapon"
        row.operator(WITCH_OT_AddConstraints.bl_idname, text="Attach to l_weapon", icon='CONSTRAINT').action = "attach_l_weapon"
        row.operator(WITCH_OT_ViewportNormals.bl_idname, text="Faster Viewport Normals", icon='MESH_DATA')

        row = layout.row().box()
        row = row.column(align=True)
        row.label(text='Animation Import')
        op = row.operator(WITCH_OT_ImportW2Rig.bl_idname, text="Rig (.w2rig)", icon='ARMATURE_DATA')
        op.filepath = os.path.join(get_uncook_path(context),"characters\\base_entities\\")

        row = layout.row().box()
        row = row.column(align=True)
        row.label(text='Animation Export')
        row.operator(WITCH_OT_ExportW2RigJson.bl_idname, text="Rig (.w2rig)", icon='ARMATURE_DATA')
        row.operator(WITCH_OT_ExportW2AnimJson.bl_idname, text="Anim (.w2anims)", icon='MESH_DATA')
        # row.operator(WITCH_OT_ExportW2RigJson.bl_idname, text="Rig Json (.w2rig.json)", icon='ARMATURE_DATA')
        # row.operator(WITCH_OT_ExportW2AnimJson.bl_idname, text="Anim Json (.w2anims.json)", icon='MESH_DATA')


        #Morphs
        row = layout.row().box()
        row = row.column(align=True)
        row.label(text='Morphs')
        row.operator(WITCH_OT_morphs.bl_idname, text="Load Face Morphs", icon='SHAPEKEY_DATA')

        #General Settings
        row = layout.row().box()
        column = row.column(align=True)
        column.label(text='General Settings')
        # addon_prefs = context.preferences.addons[__package__].preferences
        # row.prop(addon_prefs, 'keep_lod_meshes')
        addon_prefs = context.preferences.addons[__package__].preferences
        column.prop(addon_prefs, 'use_fbx_repo')
        column = row.column(align=True)
        row_lod = column.row()
        row_lod.operator(WITCH_OT_ENTITY_lod_toggle.bl_idname, text="lod0").action = "_lod0"
        row_lod.operator(WITCH_OT_ENTITY_lod_toggle.bl_idname, text="lod1").action = "_lod1"
        row_lod.operator(WITCH_OT_ENTITY_lod_toggle.bl_idname, text="lod2").action = "_lod2"
        column = row.column(align=True)
        row = column.row()
        row.operator(WITCH_OT_ENTITY_lod_toggle.bl_idname, text="Hide Collision Mesh").action = "_collisionHide"
        row.operator(WITCH_OT_ENTITY_lod_toggle.bl_idname, text="Show Collision Mesh").action = "_collisionShow"

class WITCH_PT_Quick(WITCH_PT_Base, bpy.types.Panel):
    bl_label = "QUICK ANIMATION IMPORT"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        pass

from bpy.utils import (register_class, unregister_class)

_classes = [
    #ent_import
    WITCH_OT_morphs,
    WITCH_OT_w2L,
    WITCH_OT_w2w,
    WITCH_OT_w2mi,
    WITCH_OT_w2ent,
    WITCH_OT_radish_w2L,
    #anims
    WITCH_OT_AddConstraints,
    WITCH_OT_ImportW2Rig,
    WITCH_OT_ExportW2RigJson,
    WITCH_OT_ExportW2AnimJson,
    WITCH_OT_ViewportNormals,
    WITCH_OT_load_layer,
    WITCH_OT_load_layer_group,
    WITCH_OT_load_texarray,

    #panels
    WITCH_PT_Main,
    #WITCH_PT_Utils,
]

def register():
    bpy.utils.register_class(Witcher3AddonPrefs)
    bpy.types.Object.template = StringProperty(
        name = "template"
    )
    bpy.types.Object.entity_type = StringProperty(
        name = "entity_type"
    )
    bpy.types.Collection.level_path = StringProperty(
        name = "level_path"
    )
    bpy.types.Collection.layerBuildTag = StringProperty(
        name = "layerBuildTag"
    )
    bpy.types.Collection.world_path = StringProperty(
        name = "world_path"
    )
    bpy.types.Collection.group_type = StringProperty(
        name = "group_type"
    )
    for cls in _classes:
        register_class(cls)
    ui_entity.register()
    ui_morphs.register()
    ui_import_menu.register()
    #ui_map.register()
    ui_anims.register()
    register_class(WITCH_PT_Utils)
    register_class(WITCH_PT_Quick)
    ui_voice.register()
    ui_mimics.register()
    ui_anims_list.register()

def unregister():
    unregister_class(WITCH_PT_Quick)
    unregister_class(WITCH_PT_Utils)
    bpy.utils.unregister_class(Witcher3AddonPrefs)
    del bpy.types.Object.template
    del bpy.types.Object.entity_type

    del bpy.types.Collection.level_path
    del bpy.types.Collection.layerBuildTag
    del bpy.types.Collection.world_path
    del bpy.types.Collection.group_type
    for cls in _classes:
        unregister_class(cls)
    ui_import_menu.unregister()
    #ui_map.unregister()
    ui_anims.unregister()
    ui_entity.unregister()
    ui_morphs.unregister()
    ui_voice.unregister()
    ui_mimics.unregister()
    ui_anims_list.unregister()
