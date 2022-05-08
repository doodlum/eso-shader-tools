import os
import subprocess
import shutil
import glob
import xml.etree.ElementTree as ET
from pathlib import Path

temp_output = ".temp\\"
src_output = "Shaders\\Source\\"


def extract_shaders():
    extractor = "Utilities\\EsoExtractData\\EsoExtractData.exe"
    if Path(temp_output).is_dir():
        shutil.rmtree(temp_output)
    if Path(src_output).is_dir():
        shutil.rmtree(src_output)
    subprocess.run(extractor + " --fileext fxh " + "..\\game.mnf " + temp_output, capture_output=True)
    subprocess.run(extractor + " --fileext hlsl " + "..\\game.mnf " + temp_output, capture_output=True)
    subprocess.run(extractor + " --filename materialdefinitions.xml " + "..\\game.mnf " + temp_output, capture_output=True)
    subprocess.run(extractor + " --filename zoshadertechniques.xml " + "..\\game.mnf " + temp_output, capture_output=True)
    shutil.rmtree(temp_output + "shaders\\glsl")
    shutil.copytree(temp_output + "\\shaders", src_output)


def rename_materials():
    tree = ET.parse(src_output + "\\materialdefinitions.xml")
    root = tree.getroot()
    for ShaderName in root.iter('ShaderName'):
        name = ShaderName.get('value') + ".hlsl"
        os.rename(src_output + name, src_output + name)


def rename_includes():
    includes = []
    files = glob.glob(src_output + "*.*")
    for file in files:
        with open(file, "r") as fi:
            for ln in fi:
                if ln.startswith("#include"):
                    included_file = ln.split()[1]
                    if included_file not in includes:
                        includes.append(included_file.replace("\"", ""))
    includes.remove("HLSL_to_PSSL.h")
    for included_file in includes:
        os.rename(src_output + included_file, src_output + included_file)
    os.rename(src_output + "ZoShaderTechniques.xml", src_output + "ZoShaderTechniques.xml")
    os.rename(src_output + "MaterialDefinitions.xml", src_output + "MaterialDefinitions.xml")


print("Extracting files from game.mnf")
extract_shaders()
print("Renaming files to uppercase")
rename_materials()
rename_includes()
print("Cleaning up")
shutil.rmtree(temp_output)
