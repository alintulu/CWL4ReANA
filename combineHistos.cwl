cwlVersion: v1.0
class: CommandLineTool

requirements:
  InitialWorkDirRequirement: 
    listing:
      - $(inputs.file1)
      - $(inputs.file2)
      - $(inputs.file3)

inputs:
  file1:
    type: File
  file2:
    type: File
  file3:
    type: File

baseCommand: /bin/sh

arguments:
  - prefix: -c
   valueFrom: |
      <FILL YOUR COMMAND HERE>

outputs:
  out2:
    type: File
    outputBinding:
      glob: "out2.root"
  image:
    type: File
    outputBinding:
      glob: "image.jpg"
