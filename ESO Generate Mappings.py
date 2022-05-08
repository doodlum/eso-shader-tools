import logging
import glob
import time
import jellyfish
import concurrent.futures

# very slow
find_best_guesses = False

disassembly_output = "Shaders\\Disassembly\\"
shadercache_output = "..\\ShaderCache\\"


def get_reflection_info(file):
	reflection_string = ""
	reader = open(file, "r")
	reader.readline()
	line = reader.readline()
	while line and "// 3Dmigoto declarations" not in line:
		reflection_string += line
		line = reader.readline()
	return reflection_string


def get_similarity(file_a, file_b):
	src_bytes = open(file_a, "rb").read()
	dst_bytes = open(file_b, "rb").read()
	return jellyfish.jaro_similarity(str(src_bytes), str(dst_bytes))


def find_best_guess(target_file):
	files = glob.glob(disassembly_output + "*")
	best_similarity = 0.00
	best_file = "NOT FOUND"
	for file in files:
		similarity = get_similarity(file, target_file)
		if similarity > best_similarity:
			best_similarity = similarity
			best_file = file
	return target_file + " best guess to " + best_file + " with " + str(best_similarity) + " similarity"


def find_best_match(target_file):
	files = glob.glob(disassembly_output + "*")
	best_similarity = 0.00
	best_file = "NOT FOUND"
	for file in files:
		if get_reflection_info(file) == get_reflection_info(target_file):
			similarity = get_similarity(file, target_file)
			if similarity > best_similarity:
				best_similarity = similarity
				best_file = file

	if best_file == "NOT FOUND" and find_best_guesses:
		return find_best_guess(target_file)
	else:
		return target_file + " best match to " + best_file + " with " + str(best_similarity) + " similarity"


def search_future(fut):
	logging.info(fut.result())


def search_cache():
	files = glob.glob(shadercache_output + "*")
	with concurrent.futures.ProcessPoolExecutor() as executor:
		for target_file in files:
			executor.submit(find_best_match, target_file).add_done_callback(search_future)


def main():
	logging.basicConfig(filename='shader-mapping.log', filemode='w', level=logging.DEBUG)
	logging.getLogger().addHandler(logging.StreamHandler())

	print("Disassembling shaders")

	start = time.process_time()
	search_cache()

	print("Finished disassembling shaders in " + str(time.process_time() - start) + " seconds")
	print("Shader warnings and errors saved to 'shader-disassembly.log")


if __name__ == '__main__':
	main()

