##################################################
### Python Virtual Environment ###################
##################################################

install:
	@( \
		pip install --upgrade pip; \
		pip install --no-cache-dir -r requirements.txt; \
	);
