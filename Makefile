# This will install or upgrade an install
# Note: This doesn't work on github actions (ubuntu); it needs to run under sudo there
install-cdk:
	npm install -g aws-cdk@latest


# commands to get DVC setup
# totally untested if you can run this as-is
#setup-dvc:
#	cd infrastructure && terraform init && terraform plan && terraform apply


# env just for development that has pretty much everything so I don't need to maintain 3 local envs
# SYSTEM_VERSION_COMPAT=1 is a workaround for python modules that don't install correctly on Big Sur
setup-development-pipenv:
	rm -rf Pipfile
	SYSTEM_VERSION_COMPAT=1 pipenv --python 3.8
	SYSTEM_VERSION_COMPAT=1 pipenv install --skip-lock -r training/requirements.txt
	SYSTEM_VERSION_COMPAT=1 pipenv install --skip-lock -r serving/app/requirements.txt
	# pipenv can't handle the -e . syntax but pip can
	SYSTEM_VERSION_COMPAT=1 cd serving/deployment && pipenv run pip install -r requirements.txt --upgrade

# run this inside the virtual environment if local
train:
	dvc repro train

# run this inside the virtual environment if local
# it isn't wrapped with pipenv b/c you sometimes run this locally (pipenv) and sometimes on the server (not pipenv)
test-service:
	PYTHONPATH=. python3.8 serving/tests/test_service.py

# check if an env var is set. You can use this by adding dependencies like require-variable-AWS-REGION
require-variable-%: GUARDS
	@ if [ -z '${${*}}' ]; then echo 'Environment variable $* not set.' && exit 1; fi

# check if a command is available. You can use this by adding dependencies like require-command-pipenv
require-command-%: GUARDS
	$(if $(shell command -v ${*} 2> /dev/null),,$(error Please install `${*}`))

# rules that should be run every time regardless of whether the rule name is a file that exists
.PHONY: GUARDS

# empty rules to bridge wildcard rules that shouldn't cache over to .PHONY
GUARDS:
