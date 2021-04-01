
##################################

##################################

# BUILD - build images locally using s2i

.PHONY: build
build:
	./scripts/build.sh

##################################

# PUSH - push images to repository

.PHONY: push
push:
	./scripts/push.sh

##################################
