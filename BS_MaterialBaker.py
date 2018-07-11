"""
BS_MaterialBaker

Author: Bone-Studio
Programmer: Juan Gea
Version 0.15
"""

import bpy

#print(bpy.context.active_object.active_material)
#print(bpy.context.active_object.material_slots)

# TRUE = Bakea al objeto seleccionado
# FALSE = Bakea a un plano cuadrado con coordenadas UV 1,1, para ser utilizado en objetos tileados, puede requerir de ajustes en el tile si la textura de origen no tenia proporciones 1:1


BakePlane = ""
OldActive = ""

matToMod = ""
imagesToSave = []

def dump(obj):
  for attr in dir(obj):
    print("obj.%s = %r" % (attr, getattr(obj, attr)))
    
def createBakePlane():
    OldActive = bpy.context.scene.objects.active
    bpy.ops.mesh.primitive_plane_add(radius=1, view_align=False, enter_editmode=False, location=(0,0,0))
    ob = bpy.context.object
    me = ob.data
    ob.name = 'BS_BakePlane'
    me.name = 'BS_BakePlaneMesh'    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0)
    bpy.ops.object.mode_set(mode='OBJECT')
    BakePlane = bpy.data.objects["BS_BakePlane"]
    bpy.context.scene.objects.active = OldActive
    
def MaterialToBakePlane(tgt_mat):
    print("EN ASIGNAR MATERIAL")
    BakePlane = bpy.data.objects["BS_BakePlane"]
    print(BakePlane)
    if BakePlane.data.materials:
        BakePlane.data.materials[0] = tgt_mat
    else:
        BakePlane.data.materials.append(tgt_mat)    

#START EL PROBLEMA ESTA AQUI--------------------------------------------------------------------------------------------------- 
    
def bake_slot(reconNodes,viewerNode,img_name,resx,rexy,mat,parent_node,parent_input,isNormalMap,format):  
    matNodesF = mat.node_tree.nodes
    matLinksF = mat.node_tree.links
    node_imageTexture = ""
    tgt_image = ""
    bpy.ops.image.new(name=img_name,width=resx,height=rexy)
    tgt_image = bpy.data.images[img_name]
    imagesToSave.append(img_name)
    node_imageTexture = matNodesF.new(type="ShaderNodeTexImage")
    node_imageTexture.image = tgt_image
    node_imageTexture.select = True
    matNodesF.active = node_imageTexture
    bpy.context.scene.render.resolution_x = resx
    bpy.context.scene.render.resolution_y = rexy
    bake_type = ""    
    if isNormalMap == "true":
        bake_type="NORMAL"
    else:
        bake_type="EMIT"
    bpy.ops.object.bake(type=bake_type)        
    if isNormalMap == "true":
        node_imageTexture.color_space = "NONE"
        node_normalNode = matNodesF.new(type="ShaderNodeNormalMap")
        normal_link = matLinksF.new(node_imageTexture.outputs[0], node_normalNode.inputs[1])
        if reconNodes == "true":
            link = matLinksF.new(node_normalNode.outputs[0], parent_node.inputs[parent_input])          
    else:
        if reconNodes == "true":        
            link = matLinksF.new(node_imageTexture.outputs[0], parent_node.inputs[parent_input])
    

#END EL PROBLEMA ESTA AQUI---------------------------------------------------------------------------------------------------

                    
def saveImages(saveFolder,format):
    for img in imagesToSave:
        #print(saveFolder)
        tgt_path = saveFolder+"\\"+img+"."+format
        print(tgt_path)    
        bpy.data.images[img].filepath_raw = tgt_path
        #bpy.data.images[img].file_format = format
        bpy.data.images[img].save()

def MaterialBaker(reconNodes,BakeToObject,bakeResX,bakeResY,saveFolder,format):
    if len(bpy.context.selected_objects) == 1:
        #print("ES UNO")
        BakeMaterial(reconNodes,BakeToObject,bakeResX,bakeResY,saveFolder,format)
    elif len(bpy.context.selected_objects) >= 1:
        for obj in bpy.context.selected_objects:
            bpy.context.scene.objects.active = obj
            BakeMaterial(reconNodes,BakeToObject,bakeResX,bakeResY,saveFolder,format)        
            #print("SON VARIOS")
            #print(bpy.context.scene.objects.active)
    else:
        print("PLEASE SELECT AN OBJECT")
    
def BakeMaterial(reconNodes,BakeToObject,bakeResX,bakeResY,saveFolder,format):
    print("EMPIEZA")
    OldActive = bpy.context.scene.objects.active
    midx = 0
    if BakeToObject == "false":
        createBakePlane()
    try:
        BakePlane = bpy.data.objects["BS_BakePlane"]        
    except:
        print("No hay BakePlane")
    for slot in bpy.context.active_object.material_slots:
        bpy.context.active_object.active_material_index = midx
        print("MATERIALES")
        print("-----------------------------")
        print(slot.material)
        matToMod = slot.material
        matNodes = matToMod.node_tree.nodes
        matLinks = matToMod.node_tree.links
        if BakeToObject == "false":
            MaterialToBakePlane(matToMod)
            bpy.context.scene.objects.active = BakePlane
                           
        #nBaker = matNodes.new("ShaderNodeEmission")
        #nBaker.location = (100,100)
        #nBakerTarget = 
        print("-----------------------------")
        #DETECT OUTPUT NODE
        out_node = ""
        for node in matNodes:
            if node.type == "OUTPUT_MATERIAL":
                out_node = node
                print("FOUND OUTPUT")
                
        #END DETECT OUTPUT NODE
        for node in matNodes:
            print(node.type)
            if node.type == "BSDF_PRINCIPLED":
                print("PRINCIPLED FOUND")
                #print(slot.material.name)
                #dump(slot.material)         
                #print(node.inputs)     
                #print("END PRINCIPLED FOUND")
                idx = 0
                print("CANTIDAD DE INPUTS")
                print(len(node.inputs))
                for ipt in node.inputs:
                    try:
                        print(ipt.name)
                        print(ipt.default_value)
                        value_node = ""
                        #CREA LINK EN LOS VALORES QUE NO TENGAN LINK PARA LOS MAPAS QUE NOS IMPORTAN
                        if ipt.name == "Base Color":
                            if len(ipt.links) == 0 :
                                value_node = matNodes.new(type="ShaderNodeRGB")
                                value_node.outputs[0].default_value = (ipt.default_value[0],ipt.default_value[1],ipt.default_value[2],1.0)
                                value_link = matLinks.new(value_node.outputs[0], node.inputs[idx])
                        elif ipt.name == "Specular":
                            if ipt.default_value != 0:                            
                                if len(ipt.links) == 0 :
                                    value_node = matNodes.new(type="ShaderNodeRGB")
                                    value_node.outputs[0].default_value = (ipt.default_value,ipt.default_value,ipt.default_value,1.0)
                                    value_link = matLinks.new(value_node.outputs[0], node.inputs[idx])
                        elif ipt.name == "Roughness":
                            if len(ipt.links) == 0 :
                                value_node = matNodes.new(type="ShaderNodeRGB")
                                value_node.outputs[0].default_value = (ipt.default_value,ipt.default_value,ipt.default_value,1.0)
                                value_link = matLinks.new(value_node.outputs[0], node.inputs[idx])
                        elif ipt.name == "Metallic":
                            if ipt.default_value != 0:                            
                                if len(ipt.links) == 0 :
                                    value_node = matNodes.new(type="ShaderNodeRGB")
                                    value_node.outputs[0].default_value = (ipt.default_value,ipt.default_value,ipt.default_value,1.0)
                                    value_link = matLinks.new(value_node.outputs[0], node.inputs[idx])                           
                            
                        
                        #SACA LOS BAKES DE TODO LO QUE TENGA LINK
                        for lnk in ipt.links:
                            print("VA UN INPUT")
                            print(ipt.name)
                            print(lnk)
                            print("TERMINA UN INPUT")
                            sufix = ""
                            isNormal = "false"
                            if ipt.name == "Base Color":
                                sufix = "_C"
                            elif ipt.name == "Specular":
                                sufix = "_S"
                            elif ipt.name == "Roughness":
                                sufix = "_R"                                
                            elif ipt.name == "Metallic":
                                sufix = "_M"
                            elif ipt.name == "Normal":
                                sufix = "_N"
                                isNormal = "true"                            
                            else:
                                print("No es un input normal, avisa al developer, hay que implementarlo")
                            target_name = matToMod.name + sufix                                
                            node_viewer = matNodes.new(type='ShaderNodeEmission')
                            old_node = lnk.from_node
                            if isNormal == "false":
                                vw_link = matLinks.new(old_node.outputs[0], node_viewer.inputs[0])
                                out_link = matLinks.new(node_viewer.outputs[0], out_node.inputs[0])   
                            print("BAKING")                            
                            bake_slot(reconNodes,node_viewer,target_name,bakeResX,bakeResY,matToMod,node,idx,isNormal,format)
                            print("BAKED")
                            if reconNodes == "false":
                                reconOldNodes = matLinks.new(old_node.outputs[0], node.inputs[idx])
                            #old_link = matLinks.new(old_node.outputs[0], node.inputs[idx])
                            matNodes.remove(node_viewer)
                            if isNormal == "false":
                                old_princ_link = matLinks.new(node.outputs[0], out_node.inputs[0])
                        idx = idx + 1
                        
                        #break
                    except RuntimeError as ex:
                    	print(ex)
    midx = midx +1
    if BakeToObject == "false":
        bpy.context.scene.objects.active = OldActive
        bpy.data.objects.remove(BakePlane)
    saveImages(saveFolder,format)                           
    """
            else:
                for ipt in node.inputs:
                    try:
                        for lnk in ipt.links:
                            print(ipt)
                            print(ipt.name)
                            print(lnk.from_node)            
                    except:
                        print("except")          
    """
                        
"""
Los parametros son los siguientes, por orden de aparición:
    MaterialBaker([CONECTA LAS NUEVAS TEXTURAS],[A PLANO O NO],[TAMAÑO BAKE X],[TAMAÑO BAKE Y],[CARPETA DE DESTINO DE LAS TEXTURAS],[FORMATO DE IMAGEN])
Ejemplo:
    MaterialBaker("false",1024,1024,"C:\\Blender_Resources\\BS_MaterialBaker\\tx","PNG")

Documentación detallada:
[CONECTA LAS NUEVAS TEXTURAS]
    # "true" = reemplaza los arboles de nodos por las texturas bakeadas
    # "false" = Las texturas bakeadas estarán presentes en el arbol de nodos del material, pero no sustituiran los links existentes
[A PLANO O NO]
    # "true" = Bakea al objeto seleccionado respetando las UV´s originales del objeto
    # "false" = Bakea a un plano cuadrado con coordenadas UV 1,1, para ser utilizado en objetos tileados, puede requerir de ajustes en el tile mediante UV si la textura de origen no tenia proporciones 1:1
    
[TAMAÑO BAKE X]
Tamaño en X de la textura de destino

[TAMAÑO BAKE Y]
Tamaño en Y de la textura de destino

[CARPETA DE DESTINO DE LAS TEXTURAS]
La carpeta de destino de las texturas, es IMPORTANTE poner la DOBLE BARRA con la inclinación correcta

[FORMATO DE IMAGEN]
El formato final de las texturas, "PNG" "EXR" "BMP" "JPG", etc... No estoy seguro de que funcione, de momento "PNG" funciona seguro.

"""


#CON ESTO SE EJECUTA

MaterialBaker("false","false",2048,2048,"X:\\BS_VRArq\\Blender\\FBX\\Textures\\MarDeSoto\\Room03","PNG")
