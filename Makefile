

### CONSTANTS ###
ACTIVATE_PATH = "./virtualenv/bin/activate"
VIRTUAL_ENV_PATH = "$(wildcard $(ACTIVATE_PATH))"
CURRENT_PROJECT=$(shell bash -c "git rev-parse --show-toplevel")
PROJECT_NAME=$(shell bash -c "basename $(CURRENT_PROJECT)")

BASH_PROFILE_REQS = 'export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3' 'export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv' 'export WORKON_HOME=$$HOME/.virtualenvs' 'export PROJECT_HOME=$(CURRENT_PROJECT)' 'source /usr/local/bin/virtualenvwrapper.sh' 'export CRAZY_TIME=/this/shouldnt/work'

### VARIABLES ###
req_count = 0


# ### FUNCTIONS ###
bash_check = $(shell bash -c "tr '=' '\n' | sed -n '/.*/p;1q'")

# ### TARGETS ###

## First target, runs setup as a dependency, then creates virtual environment with requirements.txt deps included
init: environment_vars
	@source ~/.bash_profile; \
	clear; \
	rmvirtualenv $(PROJECT_NAME); \
	mkvirtualenv -a $(CURRENT_PROJECT) -r $(CURRENT_PROJECT)/requirements.txt $(PROJECT_NAME);
	@echo -------------------------------------------------
	@echo ALL DONE!
	@echo -------------------------------------------------
	@echo 
	@echo type the following into terminal to start work:
	@echo
	@echo "$${BOLD}workon <project_name>$${DEFAULT}"


## Checks to make sure virtualenv is installed
venvinstall:
	@echo Checking for virtual environment installs....
	@sleep 1
	@pip3 install virtualenv > /dev/null

## Installs virtualenvwrapper to make use of mkvirtualenv and workon
venvwrapperinstall: venvinstall
	@pip3 install virtualenvwrapper > /dev/null


## See the below echo line
environment_vars: venvwrapperinstall check_git_hooks
	@echo Adding required environment variables to your bash profile located at ~/.bash_profile
	@sleep 3
	@touch ~/.bash_profile
	@for prefix in $(BASH_PROFILE_REQS); do \
		var=$$(grep -m 1 "$$prefix" < $(HOME)/.bash_profile); \
		if [ -z "$$var" ]; then \
			echo $$prefix >> $(HOME)/.bash_profile; \
		fi \
	done

## Checks for any git hooks to the current project that are located in /utils/git_hooks
check_git_hooks:
	@for filename in ./utils/git_hooks; do \
		FILE="$$(basename $${filename})"; \
		DIR="$(CURRENT_PROJECT)/.git/hooks/$${FILE}"; \
		if [ -f $${DIR} ] ; then \
			cp $(CURRENT_PROJECT)/utils/git_hooks/pre-commit $(CURRENT_PROJECT)/.git/hooks/; \
			chmod 755 $(CURRENT_PROJECT)/.git/hooks/pre-commit; \
		fi \
	done

save:
	@pip3 freeze > $(CURRENT_PROJECT)/requirements.txt

update:
	@pip3 install -r $(CURRENT_PROJECT)/requirements.txt