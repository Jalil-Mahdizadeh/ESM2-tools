See README.md in this folder for complete documentation.

Docker Hub: https://hub.docker.com/r/951753jalil/esm2-esmif

Quick container command:

docker run --gpus all -it --rm --entrypoint /bin/bash -v "${PWD}:/workspace" -w /workspace esm2_esmif:cu130
