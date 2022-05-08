import os
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

src_output = "Shaders\\Source\\"
materials_output = "Shaders\\Materials\\"


def generate_materials(shader, flags_hex, flags_string):
    file = open(materials_output + shader + "+" + str(flags_hex) + ".hlsl", 'w')
    for flag in flags_string.split(','):
        file.write("#define FX_DEF_" + flag + "\n")
    file.write("#include \"" + shader + ".hlsl\"")


def find_materials():
    if Path(materials_output).is_dir():
        shutil.rmtree(materials_output)
    os.mkdir(materials_output)
    tree = ET.parse(src_output + "\\MaterialDefinitions.xml")
    root = tree.getroot()
    for ShaderName in root.iter("ShaderName"):
        for Flag in ShaderName.findall("Flag"):
            flags_string = Flag.get("value")
            generate_materials(ShaderName.get("value"), hex(int(Flag.get("hex"), 16)), flags_string)


print("Generating materials")
find_materials()
