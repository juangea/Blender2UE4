"""
For use with BS_MaterialBaker

Author: Bone-Studio
Programmer: Juan Gea
Version 0.15

Use with the Unreal Engine plugin: 

https://github.com/20tab/UnrealEnginePython

IS NOT COMPATIBLE WITH THE NATIVE PYTHON IMPLEMENTATION OF UE4 4.19 or 4.20!!!!!!!

"""


import unreal_engine as ue


ast_general = ue.get_assets("/Game/BS/MOD/project/room")
ast_tx = ue.get_assets("/Game/BS/TX/project/room")



material_instances = []
textures_arr = []
for ast in ast_general:

	if ast.get_class().get_name() == "MaterialInstanceConstant":
		material_instances.append(ast)
	else:
		ue.log("Not a material instance")
ue.log("DETECT TEXTURES")
for astx in ast_tx:
	if astx.get_class().get_name() == "Texture2D":
		textures_arr.append(astx)
		ue.log(astx.get_name())
	else:
		ue.log("Not a texture")

ue.log("END DETECT TEXTURES")

for mat in material_instances:
	ue.log("MATERIAL")		
	ue.log(mat.get_name())
	ue.log("END MATERIAL")		
	parameter_list = []

	parent_material = mat.Parent
	for expression in parent_material.Expressions:
		try:
			parameter_name = expression.ParameterName
			parameter_list.append(parameter_name)
		except:
			ue.log("NO NAME")	
	tx_toUse = []
	for tx in textures_arr:
		detectedName = tx.get_name().find(mat.get_name())
		if detectedName != -1:
			ue.log("IN")
			tx_toUse.append(tx)
			ue.log(tx.get_name())
			ue.log("END IN")
		else:
			ue.log("FAIL")
			ue.log(tx.get_name())
			ue.log("END FAIL")
	ue.log(tx_toUse)
	for par in parameter_list:
		try:
			tx_par = ""
			if par == "Color_TX":
				for txu in tx_toUse:
					detectedtx = txu.get_name().find("_C")
					if detectedtx != -1:
						tx_par = txu
						mat.set_material_texture_parameter(par, tx_par)
						ue.log("COLOR IN PLACE")
					else:
						ue.log(txu.get_name())
			elif par == "Bump_TX":
				for txu in tx_toUse:
					detectedtx = txu.get_name().find("_B")
					if detectedtx != -1:
						tx_par = txu
						mat.set_material_texture_parameter(par, tx_par)
			elif par == "Roughness_TX":
				for txu in tx_toUse:
					detectedtx = txu.get_name().find("_R")
					if detectedtx != -1:
						tx_par = txu
						mat.set_material_texture_parameter(par, tx_par)
			elif par == "Specular_TX":
				for txu in tx_toUse:
					detectedtx = txu.get_name().find("_S")
					if detectedtx != -1:
						tx_par = txu
						mat.set_material_texture_parameter(par, tx_par)
			elif par == "Normal_TX":
				for txu in tx_toUse:
					detectedtx = txu.get_name().find("_N")
					if detectedtx != -1:
						tx_par = txu
						mat.set_material_texture_parameter(par, tx_par)
			elif par == "Metallic_TX":
				for txu in tx_toUse:
					detectedtx = txu.get_name().find("_M")
					if detectedtx != -1:
						tx_par = txu
						mat.set_material_texture_parameter(par, tx_par)
			else:
				ue.log(mat.get_name())
				ue.log("N_A")
		except:
			ue.log("N_A Exception")








