import logging
import os
import shutil
import glob
import sys
from multiprocessing.pool import ThreadPool
import subprocess
from pathlib import Path
import time

tp = ThreadPool(None)

src_output = "Shaders\\Source\\"
bytecode_output = "Shaders\\Bytecode\\"
disassembly_output = "Shaders\\Disassembly\\"

fxd = "Utilities\\cmd_Decompiler.exe -D "


def to_hlsl(filename):
	filepath = Path(filename)
	filepath = filepath.with_suffix(".hlsl")
	return bytecode_output + filepath.name


def to_output(filename):
	filepath = Path(filename)
	return disassembly_output + filepath.name


def disassemble_shader(file):
	p = subprocess.Popen(fxd + file, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, err = p.communicate()
	p.wait()
	new_file = to_hlsl(file)
	if not os.path.isfile(new_file):
		err = err.decode('utf-8', errors='ignore')
		logging.warning(err.strip() + "\n")
	else:
		new_file = to_hlsl(file)
		shutil.move(new_file, to_output(new_file))


def compile_materials():
	if Path(disassembly_output).is_dir():
		shutil.rmtree(disassembly_output)
	os.mkdir(disassembly_output)
	files = glob.glob(bytecode_output + "*")
	for file in files:
		tp.apply_async(disassemble_shader, (file,))


logging.basicConfig(filename='shader-disassembly.log', filemode='w', level=logging.DEBUG)

print("Disassembling shaders")

start = time.process_time()
compile_materials()

tp.close()
tp.join()

print("Finished disassembling shaders in " + str(time.process_time() - start) + " seconds")
print("Shader warnings and errors saved to 'shader-disassembly.log")


