# Blender2UE4
A couple of scripts used to bake materials from Cycles (based on principled shader) to textures to be used in UE4 Material Instances


BS_MaterialBaker.py ----------------------------------

This script will bake anything connected to some of the inputs of the Principled shader as textures, in two ways,
the first one is as a normal bake of the object, and the second one is as a squared texture without geometry involved, so the material
could be reused in different objects.

BS_MI_Automator.py ----------------------------------

This script can be used inside Unreal Engine, you have to define the folder were the material instances of the main material are created.
The main material has to be an specific one, check the picture "Material Base", but you can modify the script to use it with wichever
base material you have.

It will collect Material Instances, and textures, if you used the "BS_MaterialBaker.py" script to bake the textures, all the textures will
havce the same names as the corresponding materials and it will assign the correct textures to the correct places.

There are a lot of thing to improve in both scripts, if someone wants to help to improve this, please tell me, I´ll be glad to collaborate
with anyone.

The idea is to have the material pipeline perfectly solved, because the geometry and animation part are solved using the "Capsule" addon for
Blender, so with this we will be able to export materials from Blender and import them in UE4 automatically, and the idea for the future is
to be able to export also light configurations and other things, basically a public and open source datasmith for Blender.

Enjoy it!
