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
materials_output = "Shaders\\Materials\\"
bytecode_output = "Shaders\\Bytecode\\"

fxc = "Utilities\\fxc.exe "
args_common = " /nologo /O3 /Op /I " + src_output
args_ps = args_common + " /T ps_5_0 -E main -Fo "
args_vs = args_common + " /T vs_5_0 /E main /Fo "
args_cs = args_common + " /T cs_5_0 /E main /Fo "

compile_ps = True
compile_vs = False
compile_cs = False


def to_dxbc(filename):
	filepath = Path(filename)
	filepath = filepath.with_suffix(".dxbc")
	return bytecode_output + filepath.name


def compile_shader(file, args):
	p = subprocess.Popen(fxc + args + to_dxbc(file) + " " + file, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, err = p.communicate()
	p.wait()
	if err:
		err = err.decode('utf-8', errors='ignore')
		logging.warning(err.strip() + "\n")


def compile_materials():
	if Path(bytecode_output).is_dir():
		shutil.rmtree(bytecode_output)
	os.mkdir(bytecode_output)
	files = glob.glob(materials_output + "*")
	for file in files:
		if "PS+" in file:
			if compile_ps:
				tp.apply_async(compile_shader, (file, args_ps,))
		elif "VS+" in file:
			if compile_vs:
				tp.apply_async(compile_shader, (file, args_vs,))
		elif "CS+" in file:
			if compile_cs:
				tp.apply_async(compile_shader, (file, args_cs,))
		else:
			logging.critical("Invalid Shader")
			sys.exit()


logging.basicConfig(filename='shader-compilation.log', filemode='w', level=logging.DEBUG)

print("Compiling shaders")

start = time.process_time()
compile_materials()

tp.close()
tp.join()

print("Finished compiling shaders in " + str(time.process_time() - start) + " seconds")
print("Shader warnings and errors saved to shader-compilation.log")


