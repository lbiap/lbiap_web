# -*- coding: utf-8 -*-

import os
import re

# -------- Helper functions -----------

def filterTextLines( text, filter_re_ls ):
	filteredText = ""
	for line in text.splitlines():
		errorCount = 0
		for filter_re in filter_re_ls:
			if re.match( filter_re, line ):
				errorCount += 1
		if errorCount == 0:
			filteredText += line + os.linesep
	return filteredText.strip()


def getFileInfo( relativePath ):
	fullPath = os.path.abspath( relativePath )
	fileName = os.path.basename( relativePath )
	folderPath = re.sub( f"{fileName}$", "", fullPath )
	fileInfo_d = { 
		"fileName": fileName,
		"folderPath": folderPath
		}
	return fileInfo_d


def regexReplaceIt( column, target, replacement ):
	"""
	Takes a Pandas column and replaces the target string with the replacement
	"""
	return [ re.sub( target, replacement, i) for i in column ]

# -------------------------------------

# ------ Helper Lists --------------

# Make a punctuation list
punct = ",./<>?;':\"[]{}\|`~!@#$%^&*()-_=+"
punct_ls = list(punct)

# -------------------------------------
