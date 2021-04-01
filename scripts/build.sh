#!/usr/bin/env bash
printf "\n\n######## ai image build ########\n"

IMAGE_REPOSITORY=${IMAGE_REPOSITORY:-quay.io/redhatdemo/2021-ai:latest}


s2i build -c . registry.access.redhat.com/ubi8/python-38 ${IMAGE_REPOSITORY}