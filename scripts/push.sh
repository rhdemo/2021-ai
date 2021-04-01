#!/usr/bin/env bash
printf "\n\n######## ai image push ########\n"

IMAGE_REPOSITORY=${IMAGE_REPOSITORY:-quay.io/redhatdemo/2021-ai:latest}

echo "Pushing ${IMAGE_REPOSITORY}"
docker push ${IMAGE_REPOSITORY}