# ESO-Shader-Tools

##  Requirements

ESOExtractData https://en.uesp.net/wiki/Online_Mod:EsoExtractData  
Must be extracted into .\Utilities\ESOExtractData\

Jellyfish https://github.com/jamesturk/jellyfish



###   Shader Extraction
Extracts all ESO shaders and renames them to original referenced camel case


###   Generate Materials
Generates unique .hlsl files for each permutation (useful for finding issues)

###   Compile  Materials
Compiles all shaders to DXBC bytecode

###   Disassemble Materials
Disassembles compiled bytecode to 3DMigito disassembly  

###   Generate Mappings
Finds matches against game shadercache with a high level of accuracy  
Multi-threaded and matches reflection data to significantly reduce processing time  
TODO: Save to file

Requires running 3DMigito with ```export_hlsl=1```

