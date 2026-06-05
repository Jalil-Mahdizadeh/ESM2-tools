See README.md in this folder for complete documentation.

Docker Hub: https://hub.docker.com/r/951753jalil/esmfold-full

CLI:

docker run --rm --gpus all -v "${PWD}:/io" --entrypoint python esmfold-full:cu128 /io/fold_esmfold.py /io/input.fasta -o /io/output.pdb --num-recycles 1 --chunk-size 32

Notebook container:

docker run -it --rm --gpus all -v "${PWD}:/workspace/esmfold-notebook" -w /workspace/esmfold-notebook --entrypoint bash esmfold-full:cu128
