#!/usr/bin/env python3

def importFile(file):
  data = ""
  for line in open(file):
    data += line
  return data