from .setup_logging import *
log = logging.getLogger(__name__)

import os
from pathlib import Path

from .common_blender import repo_file
from .CR2W_file import read_CR2W
from .CR2W_types import Entity_Type_List, getCR2W
from .read_json_w3 import readCSkeletonData
from . import w3_types

class JsonChunk(object):
    """docstring for JsonChunk."""
    def __init__(self):
        super(JsonChunk, self).__init__()
        self.chunkIndex = 0
        self.type = 0
        #![JsonIgnore]
        #self.refChunk = 0

class ModelEnt(object):
    """docstring for ModelEnt."""
    def __init__(self, templateFilename, ns):
        super(ModelEnt, self).__init__()
        self.templateFilename = templateFilename
        self.ns = ns
        self.chunks = []
        #self.animation_face_object = False

class EntityAppearance(object):
    """docstring for EntityAppearance."""
    def __init__(self):
        super(EntityAppearance, self).__init__()
        self.name = ""
        self.includedTemplates = []#new List<ModelEnt>()

class CMeshComponent(JsonChunk):
    """docstring for CMeshComponent."""
    def __init__(self, mesh, name=""):
        super(CMeshComponent, self).__init__()
        self.mesh = mesh
        self.name = name

class CStaticMeshComponent(JsonChunk):
    """docstring for CStaticMeshComponent."""
    def __init__(self, mesh):
        super(CStaticMeshComponent, self).__init__()
        self.mesh = mesh

class CClothComponent(JsonChunk):
    """docstring for CClothComponent."""
    def __init__(self, resource):
        super(CClothComponent, self).__init__()
        self.resource = resource

class CMorphedMeshComponent(JsonChunk):
    """docstring for CMorphedMeshComponent."""
    def __init__(self, morphTarget:str, morphSource:str, morphComponentId:str):
        super(CMorphedMeshComponent, self).__init__()
        self.morphTarget = morphTarget
        self.morphSource = morphSource
        #self.morphControlTextures = morphSource
        self.morphComponentId = morphComponentId

class CMimicComponent(JsonChunk):
    """docstring for CMimicComponent."""
    def __init__(self, name:str, mimicFace:str):
        super(CMimicComponent, self).__init__()
        self.name = name
        self.mimicFace = mimicFace

class CAnimatedComponent(JsonChunk):
    """docstring for CAnimatedComponent."""
    def __init__(self, name:str, skeleton:str):
        super(CAnimatedComponent, self).__init__()
        self.name = name
        self.skeleton = skeleton

class CAnimDangleComponent(JsonChunk):
    """docstring for CAnimDangleComponent."""
    def __init__(self, name:str, constraint:int):
        super(CAnimDangleComponent, self).__init__()
        self.name = name
        self.constraint = constraint

class CAnimDangleBufferComponent(JsonChunk):
    """docstring for CAnimDangleBufferComponent."""
    def __init__(self, name:str, skeleton:str):
        super(CAnimDangleBufferComponent, self).__init__()
        self.name = name
        self.skeleton = skeleton

class SkinningAttachment(JsonChunk):
    """docstring for SkinningAttachment."""
    def __init__(self, parent:int, child:int):
        super(SkinningAttachment, self).__init__()
        self.parent = parent
        self.child = child

class CMeshSkinningAttachment(SkinningAttachment):
    """docstring for CMeshSkinningAttachment."""
    def __init__(self, parent:int, child:int):
        super(CMeshSkinningAttachment, self).__init__(parent, child)

class CAnimatedAttachment(SkinningAttachment):
    """docstring for CAnimatedAttachment."""
    def __init__(self, parent:int, child:int):
        super(CAnimatedAttachment, self).__init__(parent, child)

class CHardAttachment(SkinningAttachment):
    """docstring for CHardAttachment."""
    def __init__(self, parent:int , child:int , parentSlot:int , parentSlotName:str):
        super(CHardAttachment, self).__init__(parent, child)
        self.parentSlotName = parentSlotName
        self.parentSlot = parentSlot

class CAnimDangleConstraint_Breast(JsonChunk):
    """docstring for CAnimDangleConstraint_Breast."""
    def __init__(self, skeleton):
        super(CAnimDangleConstraint_Breast, self).__init__()
        self.skeleton = skeleton

class CAnimDangleConstraint_Collar(JsonChunk):
    """docstring for CAnimDangleConstraint_Collar."""
    def __init__(self, skeleton):
        super(CAnimDangleConstraint_Collar, self).__init__()
        self.skeleton = skeleton

class CAnimDangleConstraint_Pusher(JsonChunk):
    """docstring for CAnimDangleConstraint_Pusher."""
    def __init__(self, skeleton):
        super(CAnimDangleConstraint_Pusher, self).__init__()
        self.skeleton = skeleton

class CAnimDangleConstraint_Hinge(JsonChunk):
    """docstring for CAnimDangleConstraint_Hinge."""
    def __init__(self, skeleton):
        super(CAnimDangleConstraint_Hinge, self).__init__()
        self.skeleton = skeleton

class CAnimDangleConstraint_Hood(JsonChunk):
    """docstring for CAnimDangleConstraint_Hood."""
    def __init__(self, skeleton):
        super(CAnimDangleConstraint_Hood, self).__init__()
        self.skeleton = skeleton

class CAnimDangleConstraint_Dress(JsonChunk):
    """docstring for CAnimDangleConstraint_Dress."""
    def __init__(self, skeleton):
        super(CAnimDangleConstraint_Dress, self).__init__()
        self.skeleton = skeleton

class CAnimDangleConstraint_Dyng(JsonChunk):
    """docstring for CAnimDangleConstraint_Dyng."""
    def __init__(self, dyng):
        super(CAnimDangleConstraint_Dyng, self).__init__()
        self.dyng = dyng

class CSkeletonBoneSlot(JsonChunk):
    """docstring for CSkeletonBoneSlot."""
    def __init__(self, boneIndex:int):
        super(CSkeletonBoneSlot, self).__init__()
        self.boneIndex = boneIndex

entity_type_dict = {
    "CMeshComponent": CMeshComponent,
    "CClothComponent": CClothComponent,
    "CFurComponent": CMeshComponent,
    "CMorphedMeshComponent": CMorphedMeshComponent,
    "CMimicComponent": CMimicComponent,
    "CMeshSkinningAttachment": CMeshSkinningAttachment,
    "CAnimatedAttachment": CAnimatedAttachment,
    "CAnimDangleBufferComponent": CAnimDangleBufferComponent,
    "CAnimDangleComponent": CAnimDangleComponent,
    "CStaticMeshComponent": CStaticMeshComponent,
    "CAnimatedComponent": CAnimatedComponent,
    "CHardAttachment": CHardAttachment,
    "CSkeletonBoneSlot": CSkeletonBoneSlot
}

CAnimDangleConstraint_types = {
    "CAnimDangleConstraint_Dyng": CAnimDangleConstraint_Dyng,
    "CAnimDangleConstraint_Breast": CAnimDangleConstraint_Breast,
    "CAnimDangleConstraint_Collar": CAnimDangleConstraint_Collar,
    "CAnimDangleConstraint_Dress": CAnimDangleConstraint_Dress,
    "CAnimDangleConstraint_Hood": CAnimDangleConstraint_Hood,
    "CAnimDangleConstraint_Hinge": CAnimDangleConstraint_Hinge,
    "CAnimDangleConstraint_Pusher": CAnimDangleConstraint_Pusher,
}

def ReadMeshCEntityTemplate(templateFilename: str) -> ModelEnt:
    new_mesh = ModelEnt(templateFilename, Path(templateFilename).stem)
    fileNameFull = repo_file(templateFilename)
    entity = read_CR2W(fileNameFull)
    previous_chunk = False
    for chunk in entity.CHUNKS.CHUNKS:
        if (chunk.Type == "CMeshComponent"):
            mesh = chunk.GetVariableByName("mesh").ToString()
            name = chunk.GetVariableByName("name").ToString()
            new_mesh.chunks.append(CMeshComponent(mesh, name))

        elif (chunk.Type == "CClothComponent"):
            if chunk.GetVariableByName("resource"): #! sometimes there are no resource in files??
                cloth = chunk.GetVariableByName("resource").ToString()
                new_mesh.chunks.append(CClothComponent(cloth))
                #new_mesh.chunks[-1].refChunk = chunk.cr2w
                new_mesh.chunks[-1].type = chunk.Type
                new_mesh.chunks[-1].chunkIndex = chunk.ChunkIndex

        elif (chunk.Type == "CFurComponent"):
            if (chunk.GetVariableByName("mesh")):
                mesh = chunk.GetVariableByName("mesh").ToString()
                new_mesh.chunks.append(CMeshComponent(mesh))
                #new_mesh.chunks[-1].refChunk = chunk.cr2w
                new_mesh.chunks[-1].type = chunk.Type
                new_mesh.chunks[-1].chunkIndex = chunk.ChunkIndex

        elif (chunk.Type == "CMorphedMeshComponent"):
            morphTarget = chunk.GetVariableByName("morphTarget").ToString()
            morphSource = chunk.GetVariableByName("morphSource").ToString()
            morphComponentId = chunk.GetVariableByName("morphComponentId").ToString()
            new_mesh.chunks.append(CMorphedMeshComponent(morphTarget, morphSource, morphComponentId))

        elif (chunk.Type == "CMimicComponent"):
            name = chunk.GetVariableByName("name").ToString()
            mimicFace = chunk.GetVariableByName("mimicFace").ToString()
            new_mesh.chunks.append(CMimicComponent(name, mimicFace))
            #TODO GetFACE needed?
            #new_mesh.animation_face_object = GetFace(mimicFace)

        elif (chunk.Type == "CMeshSkinningAttachment"):
            parent = chunk.GetVariableByName("parent").Value-1
            child = chunk.GetVariableByName("child").Value-1
            new_mesh.chunks.append(CMeshSkinningAttachment(parent, child))

        elif (chunk.Type == "CAnimatedAttachment"):
            parent = chunk.GetVariableByName("parent").Value-1
            child = chunk.GetVariableByName("child").Value-1
            new_mesh.chunks.append(CAnimatedAttachment(parent, child))

        elif (chunk.Type == "CAnimDangleBufferComponent"):
            name = chunk.GetVariableByName("name").ToString()
            skeleton = chunk.GetVariableByName("skeleton").ToString()
            new_mesh.chunks.append(CAnimDangleBufferComponent(name, skeleton))

        elif (chunk.Type == "CAnimDangleComponent"):
            name = chunk.GetVariableByName("name").ToString()
            constraint = chunk.GetVariableByName("constraint").Value-1
            new_mesh.chunks.append(CAnimDangleComponent(name, constraint))

        elif (chunk.Type == "CAnimDangleConstraint_Dyng"):
            dyng = chunk.GetVariableByName("dyng").ToString()
            new_mesh.chunks.append(CAnimDangleConstraint_Dyng(dyng))

        elif (chunk.Type in CAnimDangleConstraint_types):
            skeleton = chunk.GetVariableByName("skeleton").ToString()
            new_mesh.chunks.append(CAnimDangleConstraint_types[chunk.Type](skeleton))
        elif (chunk.Type == "CHardAttachment"): #TODO NormalBlend Stuff
            if (chunk.GetVariableByName("parentSlot")):
                parent = chunk.GetVariableByName("parent").Value-1
                child = chunk.GetVariableByName("child").Value-1
                parentSlot = chunk.GetVariableByName("parentSlot").Value-1
                parentSlotName = chunk.GetVariableByName("parentSlotName").ToString()
                new_mesh.chunks.append(CHardAttachment(parent, child, parentSlot, parentSlotName))
        if new_mesh.chunks and previous_chunk != new_mesh.chunks[-1]:
            if chunk.Type in {**entity_type_dict, **CAnimDangleConstraint_types}:
                #new_mesh.chunks[-1].refChunk = chunk.cr2w
                new_mesh.chunks[-1].type = chunk.Type
                new_mesh.chunks[-1].chunkIndex = chunk.ChunkIndex
        if new_mesh.chunks:
            previous_chunk = new_mesh.chunks[-1]
    return new_mesh


def create_CEntity(file):
    hasCMovingPhysicalAgentComponent = False
    CHUNKS = file.CHUNKS.CHUNKS
    this_Entity = w3_types.Entity()
    this_Entity.name = Path(file.fileName).stem
    this_Entity.appearances = []
    this_Entity.coloringEntries = []
    
    new_mesh = ModelEnt("staticMeshes", "staticMeshes")
    this_Entity.CAnimAnimsetsParam = []
    this_Entity.CAnimMimicParam = []
    for chunk in CHUNKS:
        if(chunk.Type == "CEntityTemplate" and chunk.GetVariableByName("appearances")):
            appearances = chunk.GetVariableByName("appearances").More
            for appearance in appearances:
                name = appearance.GetVariableByName("name").ToString()
                currentApp = EntityAppearance()
                currentApp.name = name
                if appearance.GetVariableByName("includedTemplates"):
                    includedTemplates = appearance.GetVariableByName("includedTemplates").ToArray()
                    for entryTemplate in includedTemplates:
                        entry = entryTemplate.DepotPath
                        currentApp.includedTemplates.append(ReadMeshCEntityTemplate(entry))
                else:
                    #some "invisible" appearances have no entities attached
                    log.warning("Entity has no includedTemplates")
                    #GetFace(@"characters\models\geralt\head\model\h_01_mg__geralt.w3fac")
                this_Entity.appearances.append(currentApp)
                #print(appearance.elementName)
                
            coloringEntries = chunk.GetVariableByName("coloringEntries")
            if coloringEntries:
                for coloringEntry in coloringEntries.More:
                    colorShift1 = coloringEntry.GetVariableByName('colorShift1')
                    if colorShift1:
                        colorShift1 = w3_types.CColorShift(colorShift1.GetVariableByName('hue').Value if colorShift1.GetVariableByName('hue') else 0,
                                                           colorShift1.GetVariableByName('saturation').Value if colorShift1.GetVariableByName('saturation') else 0,
                                                           colorShift1.GetVariableByName('luminance').Value if colorShift1.GetVariableByName('luminance') else 0)
                    colorShift2 = coloringEntry.GetVariableByName('colorShift2')
                    if colorShift2:
                        colorShift2 =  w3_types.CColorShift(colorShift2.GetVariableByName('hue').Value if colorShift2.GetVariableByName('hue') else 0,
                                                           colorShift2.GetVariableByName('saturation').Value if colorShift2.GetVariableByName('saturation') else 0,
                                                           colorShift2.GetVariableByName('luminance').Value if colorShift2.GetVariableByName('luminance') else 0)
                    this_Entity.coloringEntries.append(
                        w3_types.SEntityTemplateColoringEntry(
                            coloringEntry.GetVariableByName('appearance').ToString(),
                            coloringEntry.GetVariableByName('componentName').ToString(),
                            colorShift1,
                            colorShift2))
                        # { 'name': "MimicSets",
                        #   'animationSets':list(map(lambda x: x.DepotPath, chunk.GetVariableByName("animationSets").ToArray()))
                        # })

        elif chunk.Type in Entity_Type_List: #entity is
            if hasattr(chunk, 'Components'):
            #for staticChunkPtr in chunk.GetVariableByName("components").ToArray():
                for chunk_idx in chunk.Components:
                    staticChunk = CHUNKS[chunk_idx-1] #staticChunkPtr.Reference
                    if (staticChunk.Type == "CStaticMeshComponent"):
                        mesh = staticChunk.GetVariableByName("mesh").ToString()
                        new_mesh.chunks.append(CStaticMeshComponent(mesh))
                        #new_mesh.chunks[-1].refChunk = staticChunk.cr2w
                        new_mesh.chunks[-1].type = staticChunk.Type
                        new_mesh.chunks[-1].chunkIndex = staticChunk.ChunkIndex

                    elif (staticChunk.Type == "CMeshComponent"):
                        mesh = staticChunk.GetVariableByName("mesh").ToString()
                        new_mesh.chunks.append(CMeshComponent(mesh))
                        #new_mesh.chunks[-1].refChunk = staticChunk.cr2w
                        new_mesh.chunks[-1].type = staticChunk.Type
                        new_mesh.chunks[-1].chunkIndex = staticChunk.ChunkIndex

                    elif (staticChunk.Type == "CMeshComponent"):
                        mesh = staticChunk.GetVariableByName("mesh").ToString()
                        new_mesh.chunks.append(CMeshComponent(mesh))
                        #new_mesh.chunks[-1].refChunk = staticChunk.cr2w
                        new_mesh.chunks[-1].type = staticChunk.Type
                        new_mesh.chunks[-1].chunkIndex = staticChunk.ChunkIndex

                    elif (staticChunk.Type == "CFurComponent"):
                        mesh = staticChunk.GetVariableByName("mesh").ToString()
                        new_mesh.chunks.append(CMeshComponent(mesh))
                        #new_mesh.chunks[-1].refChunk = staticChunk.cr2w
                        new_mesh.chunks[-1].type = staticChunk.Type
                        new_mesh.chunks[-1].chunkIndex = staticChunk.ChunkIndex

                    elif (staticChunk.Type == "CAnimatedComponent"):
                        name = staticChunk.GetVariableByName("name").ToString()
                        skeleton = staticChunk.GetVariableByName("skeleton").ToString()
                        new_mesh.chunks.append(CAnimatedComponent(name, skeleton))
                        #new_mesh.chunks[-1].refChunk = staticChunk.cr2w
                        new_mesh.chunks[-1].type = staticChunk.Type
                        new_mesh.chunks[-1].chunkIndex = staticChunk.ChunkIndex
                            

        elif (chunk.Type == "CHardAttachment"):
            if (chunk.GetVariableByName("parentSlot")):
                parent = chunk.GetVariableByName("parent").Value-1
                child = chunk.GetVariableByName("child").Value-1
                parentSlot = chunk.GetVariableByName("parentSlot").Value-1
                parentSlotName = chunk.GetVariableByName("parentSlotName").ToString()
                new_mesh.chunks.append(CHardAttachment(parent, child, parentSlot, parentSlotName))
                #new_mesh.chunks[-1].refChunk = chunk.cr2w;
                new_mesh.chunks[-1].type = chunk.Type
                new_mesh.chunks[-1].chunkIndex = chunk.ChunkIndex
        elif (chunk.Type == "CMeshSkinningAttachment"):
            parent = chunk.GetVariableByName("parent").Value-1
            child = chunk.GetVariableByName("child").Value-1
            new_mesh.chunks.append(CMeshSkinningAttachment(parent, child))
            new_mesh.chunks[-1].type = chunk.Type
            new_mesh.chunks[-1].chunkIndex = chunk.ChunkIndex

        elif (chunk.Type == "CSkeletonBoneSlot"):
            boneIndex = chunk.GetVariableByName("boneIndex").Value #val?
            new_mesh.chunks.append(CSkeletonBoneSlot(boneIndex))
            #new_mesh.chunks[-1].refChunk = chunk.cr2w;
            new_mesh.chunks[-1].type = chunk.Type
            new_mesh.chunks[-1].chunkIndex = chunk.ChunkIndex
        elif(chunk.name == "CMovingPhysicalAgentComponent" and chunk.GetVariableByName("skeleton")):
            name = chunk.GetVariableByName("name").ToString()
            skeleton = chunk.GetVariableByName("skeleton").ToString()
            new_mesh.chunks.append(w3_types.CMovingPhysicalAgentComponent(skeleton, name))
            #new_mesh.chunks[-1].refChunk = chunk.cr2w
            new_mesh.chunks[-1].type = chunk.Type
            new_mesh.chunks[-1].chunkIndex = chunk.ChunkIndex
            hasCMovingPhysicalAgentComponent = True;
            this_Entity.MovingPhysicalAgentComponent= new_mesh.chunks[-1]
        elif(chunk.name == "CAnimAnimsetsParam"):
            this_Entity.CAnimAnimsetsParam.append({ 'name': chunk.GetVariableByName("name").ToString(),
                                            'animationSets':list(map(lambda x: x.DepotPath, chunk.GetVariableByName("animationSets").ToArray()))
                                           })
        elif(chunk.name == "CAnimMimicParam"):
            this_Entity.CAnimMimicParam.append({ 'name': "MimicSets",
                                            'animationSets':list(map(lambda x: x.DepotPath, chunk.GetVariableByName("animationSets").ToArray()))
                                           })

    
    
    if not hasCMovingPhysicalAgentComponent:
        for ent in new_mesh.chunks:
            if ent.type == "CAnimatedComponent":
                this_Entity.MovingPhysicalAgentComponent = ent
                break
    this_Entity.staticMeshes = new_mesh
    return this_Entity

def load_bin_entity(fileName) -> w3_types.Entity:
    with open(fileName,"rb") as f:
        theFile = getCR2W(f)
        f.close()
        CEntity = create_CEntity(theFile)
    return CEntity