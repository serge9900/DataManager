MY_PATH=$(shell pwd)
export SOURCE_FILES := $(MY_PATH)/Manager.py

.PHONY: app 
app :
	@echo "Building..."
	@python3 $(SOURCE_FILES)
 
 
 
 
 
 
 
 
 
 
