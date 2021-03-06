#!/usr/bin/env python

import sys
import os
import subprocess
import math
import hashlib
import copy

import C_TO_LOGIC
import VHDL
import SW_LIB
import SYN

#MODELSIM_PATH="/media/1TB/Programs/Linux/Modelsim/modelsim_ase/bin/vsim"
MODELSIM_PATH="/media/1TB/Programs/Linux/Modelsim18.0.0.219/modelsim_ase/bin/vsim"

def DO_OPTIONAL_DEBUG(do_debug=False, latency=0):
	# DO DEBUG PROJECT?
	if not do_debug:
		return

	# #######################################################################################################
	
	# Get all vhd files in syn output
	vhd_files = []
	for root, dirs, filenames in os.walk(SYN.SYN_OUTPUT_DIRECTORY):
		for f in filenames:
			if f.endswith(".vhd"):
				#print "f",f
				fullpath = os.path.join(root, f)
				abs_path = os.path.abspath(fullpath)
				#print "fullpath",fullpath
				#f
				if ( (root == SYN.SYN_OUTPUT_DIRECTORY + "/main") and
				   f.startswith("main_") and f.endswith("CLK.vhd") ):
					clks = int(f.replace("main_","").replace("CLK.vhd",""))
					if clks==latency:
						print "Using top:",abs_path
						vhd_files.append(abs_path)
				else:
					vhd_files.append(abs_path)
			
		
			
	# Create modelsim script (do?)
	# /media/1TB/Programs/Linux/Modelsim/modelsim_ase/bin/vsim
	#top_entity_name = top_dir.strip("/").strip("]").replace("]","_").replace("[","_").replace("/","_").replace(".","_") # .main_BIN_OP_SL_main_c_7_top"
	
	proj_name = "debug_proj"
	proj_dir = SYN.SYN_OUTPUT_DIRECTORY + "/"
	text = ""
	text += '''
	project new {''' + proj_dir + '''} ''' + proj_name + '''
	'''
	# Add all files
	for vhd_file in vhd_files:
		text += '''
	project addfile {''' + vhd_file + '''}
'''
	
	# Compile
	text += '''
	project calculateorder
	project compileall
	vlib work
	vmap work work
	'''
	# Do vsim too?
	# vsim work.main_bin_op_sl_main_c_7_top
	
	if do_debug:
		do_filename = proj_name + ".do"
		do_filepath = proj_dir + do_filename
		f=open(do_filepath,"w")
		f.write(text)
		f.close()
		
		# Run modelsim
		bash_cmd = (
			MODELSIM_PATH + " " + "-do 'source {" + do_filepath + "}' " )
			
			
		log_text = SYN.GET_SHELL_CMD_OUTPUT(bash_cmd)
		print log_text
		sys.exit(0)
	
