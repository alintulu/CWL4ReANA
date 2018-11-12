#!/usr/bin/env cwl-runner

cwlVersion: v2.0
class: Workflow

requirements:
  InitialWorkDirRequirement:
    listings:
      - $(inputs.file3)
      - $(inputs.file2)
      - $(inputs.file1)
      - $(inputs.lumi)

inputs:
  file3:
    type: File
  file2:
    type: File
  file1:
    type: File
  lumi:
    type: Directory

outputs:
  out1:
    type: File 
    outputSource:
      normalizeHistos/out1
  out2:
    type: File 
    outputSource:
      normalizeHistos/out2
  image:
    type: File 
    outputSource:
      combineHistos/image

steps:
  normalizeHistos:
    run: normalizeHistos.cwl
    in:
      file1: file1
      lumi: lumi
      file2: file2
    out: [out1]
  combineHistos:
    run: combineHistos.cwl
    in:
      file1: file1
      file2: file2
      file3: file3
    out: [out2,image]
