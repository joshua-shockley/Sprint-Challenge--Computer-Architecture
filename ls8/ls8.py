#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

cpu.load()
# print(f"ram/memory: \n{cpu.ram}\ncpu.reg: \n {cpu.reg})
cpu.run()
