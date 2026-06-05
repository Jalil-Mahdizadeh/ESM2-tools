# ESMFold Direct Folding

This folder contains two ESMFold workflows:

1. CLI folding with `fold_esmfold.py`.
2. Notebook batch folding with `folding_notebook.ipynb`.

Both workflows use:

- Local tag: `esmfold-full:cu128`
- Docker Hub: https://hub.docker.com/r/951753jalil/esmfold-full

## CLI Workflow

`fold_esmfold.py` folds a raw sequence or FASTA/sequence file and writes one PDB.

### Input

The default CLI example uses `input.fasta`.

The current `input.fasta` contains one FASTA record with two chains separated by `:`, so ESMFold writes chains `A` and `B`.

### Run

From this folder:

```powershell
docker run --rm --gpus all -v "${PWD}:/io" --entrypoint python esmfold-full:cu128 /io/fold_esmfold.py /io/input.fasta -o /io/output.pdb --num-recycles 1 --chunk-size 32
```

### Options

```text
sequence                  Raw sequence, or path to FASTA/sequence file
-o, --output              Output PDB path. Default: folded.pdb
--num-recycles            ESMFold recycles. Default: 1 in this script. Use 4 for higher default ESMFold accuracy.
--chunk-size              Lower values reduce memory use. Default: 32.
--device                  cuda or cpu. Defaults to cuda when available.
--precision               bf16, fp16, or fp32. Default: bf16.
```

Validated CLI output:

- `output.pdb`
- sequence length: 289 residues across chains `A` and `B`
- atom records: 2206

## Notebook Workflow

`folding_notebook.ipynb` batch-folds sequences from a CSV file.

### Input

The notebook reads:

```text
data/1a3n_chainA_samples_t1.00.csv
```

That CSV contains the native sequence plus 10 ESM-IF sampled sequences copied from the inverse-folding workflow.

Notebook settings:

- `num_recycles = 3`
- `chunk_size = 32`
- `precision = "bf16"`

### Output

The notebook writes one PDB per input row:

```text
output/1a3n_native_seq.pdb
output/sample1_t1.00_0.496.pdb
...
output/sample10_t1.00_0.504.pdb
```

Validated notebook output:

- 11 PDB files in `output/`.
- Each file contains a folded single-chain structure for one row in the CSV.

### Run

From this folder:

```powershell
docker run -it --rm --gpus all -v "${PWD}:/workspace/esmfold-notebook" -w /workspace/esmfold-notebook --entrypoint bash esmfold-full:cu128
```

Then attach VS Code to the running container, open `/workspace/esmfold-notebook/folding_notebook.ipynb`, select the container Python kernel, and run all cells.

## Notes

- The CLI uses one recycle by default to reduce time and memory usage.
- The notebook uses three recycles for the batch example.
- If GPU memory is tight, reduce `--chunk-size`, reduce `--num-recycles`, or keep `precision = "bf16"`.
- ESMFold may emit non-fatal warnings from DeepSpeed/OpenFold internals.
