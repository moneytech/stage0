import subprocess
import ctypes
import re

subprocess.call("./bin/dis foo | sponge z_disassembled", shell=True)

vm = ctypes.CDLL('./libvm.so')

vm.initialize_lilith()
vm.load_lilith(ctypes.create_string_buffer("foo".encode('ascii')))

# vm.get_byte.argtype = ctypes.c_uint
# vm.get_byte.restype = ctypes.c_ubyte

# print("Memory 0-19 values:")
# for i in range(0, 20):
# 	print(vm.get_byte(i))

vm.get_memory.argtype = ctypes.c_uint
vm.get_memory.restype = ctypes.c_char_p

hexlookup = { 0 : '0', 1 : '1', 2 : '2', 3 : '3', 4 : '4', 5 : '5', 6 : '6', 7 : '7', 8 : '8', 9 : '9', 10 : 'A', 11 : 'B', 12 : 'C', 13 : 'D', 14 : 'E', 15 : 'F' }

def formatByte(a):
	first = a >> 4
	second = a % 16
	return str(hexlookup[first]+hexlookup[second])

def formatAddress(a):
	first = a >> 24
	second = (a % 16777216) >> 16
	third = (a % 65536) >> 8
	fourth = a % 256
	myreturn = formatByte(first) + formatByte(second) + formatByte(third) + formatByte(fourth)
	return myreturn[:-1] + "x"

def formatRegister(a):
	first = a >> 24
	second = (a % 16777216) >> 16
	third = (a % 65536) >> 8
	fourth = a % 256
	return formatByte(first) + formatByte(second) + formatByte(third) + formatByte(fourth)

def get_header():
	return """
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta charset="utf-8" />
	<title>Knight CPU Debugger</title>
	<link rel="stylesheet" type="text/css" href="static/style.css" />
	<script type="text/javascript" src="static/jquery-1.8.3.js"> </script>
	<script type="text/javascript" src="static/script.js"></script>
</head>
<body>
	<div>
		<a href="index.html#RUN"><button type="button">RUN</button></a>
		<a href="index.html#STEP"><button type="button">STEP</button></a>
		<a href="index.html#STOP"><button type="button">STOP</button></a>
		<a href="index.html#PAUSE"><button type="button">PAUSE</button></a>
		<a href="index.html#RESET"><button type="button">RESET</button></a>
		<a href="index.html#DEBUG"><button type="button">DEBUG</button></a>
	</div>
	<div>
	<div style="height:230px; width:60%; float:left; overflow-y: scroll;">
	<table class="Memory">
		<thead>
			<tr>
				<th>Index</th>
				<th>0</th>
				<th>1</th>
				<th>2</th>
				<th>3</th>
				<th>4</th>
				<th>5</th>
				<th>6</th>
				<th>7</th>
				<th>8</th>
				<th>8</th>
				<th>A</th>
				<th>B</th>
				<th>C</th>
				<th>D</th>
				<th>E</th>
				<th>F</th>
			</tr>
		</thead>
		<tbody>"""

def get_spacer1():
	return """		</tbody>
	</table>
	</div>
	<div>
"""

def get_registers(index):
	vm.get_register.argtype = ctypes.c_uint
	vm.get_register.restype = ctypes.c_uint

# R0 = vm.get_register(3)
# print("Register R0 value:")
# print(R0)

	temp = """	<table class="Registers">
		<thead>
			<tr>
				<th>Register</th>
				<th>Value</th>
			</tr>
		</thead>
		<tbody>"""

	for i in range(0,8):
		temp = temp + """<tr"><td>R""" + str(index + i) + "</td><td>" + formatRegister(vm.get_register(index + i)) + "</td></tr>\n"

	return temp + """		</tbody>
	</table> """

def get_spacer2():
	return """
	</div>
	</div>
	<div style="position:absolute; left:10px; top:280px; overflow-y: scroll; height:200px; width:60%;"> """

def get_disassembled():
	f = open('z_disassembled', "r")

	temp = """<table class="Debug"><tbody>"""
	i = 0
	for line in f:
		pieces = re.split(r'\t+', line)
		temp = temp + "<tr><td>" + formatRegister(i) + "</td><td>" + pieces[0] + "</td><td>" + pieces[1] + "</td></tr>\n"
		i = i + 4

	return temp + "</tbody></table>"

def get_footer():
	return """
	</div>
</body>
</html>
"""

print(get_header())
print( (vm.get_memory(0)).decode('utf-8'))
print(get_spacer1())
print(get_registers(0))
print(get_registers(8))
print(get_spacer2())
print(get_disassembled())
print(get_footer())