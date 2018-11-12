# Purpose: Create the files needed to run cwltool. The files are input.yml, workflow.cwl as well as the individual workflow files
# Author:  Adelina.eleonora.lintuluoto@cern.ch
# Created: November 7, 2018
# Updated: November 12, 2018

from sets import Set

# Define name of individual workflows as the string __name, separate with a comma
# Define your inputs file as the string __in, separate input files for different workflows with a comma, if input is other type than "File" documment it between two semicolons like <name>:<type>:
# Define output as the string __out, separate with a comma
 
__name = "normalizeHistos,combineHistos"
__in = "file1.root lumi:Directory: file2.root,file1.root file2.root file3.root"
__out = "out1.root,out2.root image.jpg"
__baseCo = "/bin/sh"

def my_split(arr,isName):
  temp = []
  temp2 = arr.split(",")
  if isName:
    return temp2
  else:
    for t in temp2:
      temp.append(t.split(" "))
    return temp

_name = my_split(__name,True)
_in = my_split(__in, False)
_out = my_split(__out, False)

# Check if input name has a type specified
def check_type(string):
  return (string[(len(string)-1):] == ":")

# If check_type() is true, check which type
def return_type(string):
  temp = list(string)
  for j in range(len(temp)):
    if temp[j] is ':':
      return [string[:j],string[(j+1):(len(string)-1)]]

# Find extension of file, i.e. .root, .C
def find_extension(string):
  temp = list(string)
  for j in range(len(temp)-1,-1,-1):
    if temp[j] is '.':
      return [string[:j],string[j:]]
  return None

def reformat(arr, _set, _key_value, _arr, _key_ext):  
  for i in arr:
    temp = ([])
    for j in i:
      if check_type(j):
        key_value = return_type(j)
        key = key_value[0]
	value = key_value[1]
        key_ext = find_extension(key)
        if key_ext is None:
          _set.add(key)
          ext = ""
        else:
          key = key_ext[0]
          ext = key_ext[1]
          _set.add(key)
        if key not in _key_ext:
          _key_ext[key] = ext
        if key not in _key_value:
          _key_value[key] = value
        temp.append(key)
      else:
        key_ext = find_extension(j)
        key = key_ext[0]
        ext = key_ext[1]
        _set.add(key)
        if key not in _key_ext:
	  _key_ext[key] = ext
        if key not in _key_value:
          _key_value[key] = "File"
        temp.append(key)
    _arr.append(temp)
  return [_set, _key_value, _arr, _key_ext]

# Reformat input data
iset = Set([])		# All inputs stated ones
ikey_value = dict([])	# All inputs with key <-> value as <inputname> <-> <type>
iarr = ([])		# Array of arrays, inputs separated by which workflow needs them
ikey_ext = dict([])	# All inputs and their extensions as <inputname(without extension)> <-> <extension>

# Reformat output data
oset = Set([])		# All outputs stated ones
okey_value = dict([])	# All outputs with key <-> value as <inputname> <-> <type>
oarr = ([])		# Array of arrays, outputs separated by which workflow needs them
okey_ext = dict([])	# All outputs and their extensions as <outputname(without extension)> <-> <extension>

reformat(_in, iset, ikey_value, iarr, ikey_ext)
reformat(_out, oset, okey_value, oarr, okey_ext)

########### CREATE INPUT.YML ###########

f = open("input.yml", "w")

for i in iset:
  f.write(i + ":\n  class: " + ikey_value[i] + "\n  path: code/" + i + ikey_ext[i] + "\n")

f.close()

########### CLOSE INPUT.YML ###########

######### CREATE WORKFLOW.CWL ###########

f = open("workflow.cwl", "w")

f.write("#!/usr/bin/env cwl-runner\n\ncwlVersion: v2.0\nclass: Workflow\n\nrequirements:\n  InitialWorkDirRequirement:\n    listings:\n")

# Write out the inputs
for i in iset:
    f.write("      - $(inputs." + i + ")\n")

f.write("\ninputs:\n")
for i in iset:
    f.write("  " + i + ":\n" + "    type: " + ikey_value[i] + "\n")  

# Write out the outputs
f.write("\noutputs:\n")
for o in oarr:
  for i in range(len(o)):
    f.write("  " + o[i] + ":\n" + "    type: " + okey_value[o[i]]  + " \n    outputSource:\n      " + _name[i] + "/" + o[i] + "\n")  

#Create the workflow steps
f.write("\nsteps:\n")
for i in range(len(_name)):
  name = _name[i]

  f.write("  " + name + ":\n    run: " + name + ".cwl\n    in:\n")
  for j in iarr[i]:
    f.write("      " + j + ": " + j + "\n")
  f.write("    out: [")
  for k in range(len(oarr[i])):
    if not (k == len(oarr[i])-1):
      f.write(oarr[i][k] + ",")
    else:
      f.write(oarr[i][k] + "]\n")

f.close()

######### CLOSE WORKFLOW.CWL ###########

###### CREATE INDIVIDUAL WORKFLOWS ########

def create_workflow(name, index):
  n = name + ".cwl" 
  f = open(n, "w")

  f.write("cwlVersion: v1.0\nclass: CommandLineTool\n\nrequirements:\n  InitialWorkDirRequirement: \n    listing:\n")
  
  # Write out the inputs
  for i in iarr[index]:
   f.write("      - $(inputs." + i + ")\n")

  f.write("\ninputs:\n")
  for i in iarr[index]:
    f.write("  " + i + ":\n" + "    type: " + ikey_value[i] + "\n")  

  # Write out base command
  f.write("\nbaseCommand: " + __baseCo + "\n")

  # Write out arguments
  f.write("\narguments:\n  - prefix: -c\n   valueFrom: |\n")
  f.write("      <FILL YOUR COMMAND HERE>\n")

  # Write out outputs
  f.write("\noutputs:\n")
  for o in oarr[index]:
    f.write("  " + o + ":\n    type: " + okey_value[o] + "\n    outputBinding:\n      " + "glob: \"" + o + okey_ext[o] + "\"\n") 

  f.close()

for i in range(len(_name)):
  create_workflow(_name[i],i) 

###### CLOSE INDIVIDUAL WORKFLOWS ########

