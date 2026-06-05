See README.md in this folder for complete documentation.

Quick container command:

docker run --gpus all -it --rm --entrypoint /bin/bash -v "${PWD}:/workspace" -w /workspace esm2_esmif:cu130
