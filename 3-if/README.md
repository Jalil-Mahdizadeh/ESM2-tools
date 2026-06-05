# ESM-IF Inverse Folding Workflow

`inversefold_ESM2.ipynb` uses ESM-IF to sample sequences from a protein backbone and analyze the sampled sequence set.

## Purpose

The notebook:

1. Checks the PyTorch/CUDA and PyTorch Geometric environment.
2. Loads `esm.pretrained.esm_if1_gvp4_t16_142M_UR50()`.
3. Reads a structure from `data/1a3n.pdb`.
4. Extracts coordinates and native sequence for chain `A`.
5. Optionally visualizes the PDB with `py3Dmol`.
6. Samples sequences from the backbone at temperatures `0.50`, `1.00`, and `2.00`.
7. Writes sampled sequence CSV files.
8. Converts each sample CSV to FASTA.
9. Calculates Shannon entropy across sampled sequences.
10. Scores native and sampled sequences with ESM-IF log-likelihood.
11. Demonstrates masked-coordinate scoring and encoder-output extraction.

## Input

The active input is configured in the notebook:

- Structure path: `data/1a3n.pdb`
- Chain: `A`
- Samples per temperature: `10`
- Temperatures: `0.5`, `1`, `2`
- Random seeds: NumPy `42`, PyTorch `42`

`data/alphabeta.pdb` is present as an additional structure file, but the current notebook run uses `data/1a3n.pdb`.

The extracted native sequence has 141 residues and starts with `VLSPADK...`.

## Outputs

Outputs are written to `output/`.

For each temperature (`0.50`, `1.00`, `2.00`):

| File pattern | Description |
| --- | --- |
| `1a3n_chainA_samples_tTEMP.csv` | Native sequence plus sampled sequences and recovery values in the IDs. |
| `1a3n_chainA_samples_tTEMP.fasta` | FASTA conversion of the sample CSV. |
| `1a3n_chainA_samples_tTEMP_shannon.csv` | Per-position entropy across the native/sample sequence table. |
| `1a3n_chainA_samples_tTEMP_LL.csv` | ESM-IF log-likelihood scores for native/sample sequences. |

Validated output counts for each temperature:

- sample CSV: 11 rows.
- FASTA: 11 records.
- entropy CSV: 141 rows.
- LL CSV: 11 rows.

## Run

Docker image:

- Local tag: `esm2_esmif:cu130`
- Docker Hub: https://hub.docker.com/r/951753jalil/esm2-esmif

From this folder:

```powershell
docker run --gpus all -it --rm --entrypoint /bin/bash -v "${PWD}:/workspace" -w /workspace esm2_esmif:cu130
```

Then attach VS Code to the running container, open `/workspace/inversefold_ESM2.ipynb`, select the container Python kernel, and run all cells.

To run from the repository root instead:

```powershell
cd path\to\ESM2
docker run --gpus all -it --rm --entrypoint /bin/bash -v "${PWD}:/workspace" -w /workspace/3-if esm2_esmif:cu130
```

## Notes

- The ESM-IF warning about missing regression weights is expected for contact prediction and does not block sequence sampling or scoring in this notebook.
- Recovery values in sample IDs are the fraction of positions matching the extracted native sequence.
- The entropy CSV row count is 141 because the extracted PDB chain sequence is 141 residues.
- The output CSV at temperature `1.00` is also used as input for the ESMFold notebook under `4-folding/data/`.
