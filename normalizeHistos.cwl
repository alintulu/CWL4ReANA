cwlVersion: v1.0
class: CommandLineTool

requirements:
  InitialWorkDirRequirement: 
    listing:
      - $(inputs.file1)
      - $(inputs.lumi)
      - $(inputs.file2)

inputs:
  file1:
    type: File
  lumi:
    type: Directory
  file2:
    type: File

baseCommand: /bin/sh

arguments:
  - prefix: -c
   valueFrom: |
      <FILL YOUR COMMAND HERE>

outputs:
  out1:
    type: File
    outputBinding:
      glob: "out1.root"
