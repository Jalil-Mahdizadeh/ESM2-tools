# ESM2, ESM-IF, and ESMFold Protein Workflows

This folder contains four GPU workflows for protein language model analysis:

1. `1-embedding`: generate ESM2 per-residue and per-sequence embeddings.
2. `2-mutagenesis`: run ESM2 masked-position mutagenesis, calculate Shannon entropy, and write a ChimeraX `.defattr` file.
3. `3-if`: run inverse folding with ESM-IF, then export sampled sequences, FASTA alignments, entropy tables, and log-likelihood tables.
4. `4-folding`: run direct folding with ESMFold in CLI mode and notebook batch mode.

The workflows are intentionally notebook-centered except for the ESMFold CLI helper. Generated outputs are kept in the repository tree because they are part of the intended deliverable.

## Docker Images

Use Docker Desktop with NVIDIA GPU support enabled.

| Workflow | Local image tag used here | Docker Hub source |
| --- | --- | --- |
| ESM2 embedding, ESM2 mutagenesis, ESM-IF | `esm2_esmif:cu130` | `951753jalil/esm2-esmif` |
| ESMFold CLI and notebook | `esmfold-full:cu128` | `951753jalil/esmfold-full` |

If the local tags are missing, pull and tag the images:

```powershell
docker pull 951753jalil/esm2-esmif:cu130
docker tag 951753jalil/esm2-esmif:cu130 esm2_esmif:cu130

docker pull 951753jalil/esmfold-full:cu128
docker tag 951753jalil/esmfold-full:cu128 esmfold-full:cu128
```

Quick GPU checks:

```powershell
docker run --rm --gpus all --entrypoint python esm2_esmif:cu130 -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.version.cuda)"
docker run --rm --gpus all --entrypoint python esmfold-full:cu128 -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.version.cuda)"
```

Validated locally on 2026-06-05 with:

- `esm2_esmif:cu130`: PyTorch `2.10.0+cu130`, CUDA `13.0`.
- `esmfold-full:cu128`: PyTorch `2.7.1+cu128`, CUDA `12.8`.
- GPU: NVIDIA RTX PRO 2000 Blackwell Generation Laptop GPU, 8151 MiB.

## Running Notebooks

The images include Python and `ipykernel`; they do not need a browser-hosted Jupyter server for the documented workflow. Start the container, attach VS Code to the running container, open the mounted folder, and select the container Python kernel for the notebook.

For the ESM2 and ESM-IF notebooks:

```powershell
cd path\to\ESM2
docker run --gpus all -it --rm --entrypoint /bin/bash -v "${PWD}:/workspace" -w /workspace esm2_esmif:cu130
```

For the ESMFold notebook:

```powershell
cd path\to\ESM2\4-folding
docker run -it --rm --gpus all -v "${PWD}:/workspace/esmfold-notebook" -w /workspace/esmfold-notebook --entrypoint bash esmfold-full:cu128
```

Then in VS Code:

1. Attach to the running container.
2. Open the mounted folder (`/workspace` or `/workspace/esmfold-notebook`).
3. Open the notebook.
4. Select the container Python kernel.
5. Run cells from top to bottom.

## Workflow Summary

| Folder | Entry point | Main input | Main outputs |
| --- | --- | --- | --- |
| `1-embedding` | `embedding.ipynb` | Hard-coded hemoglobin-like sequence in the notebook | Console tensor output and contact-map display |
| `2-mutagenesis` | `mutagenesis.ipynb` | Hard-coded 142-residue sequence in the notebook | `output/Hemo_AA_probabilities.csv`, `output/Hemo_shannon_entropy.defattr` |
| `3-if` | `inversefold_ESM2.ipynb` | `data/1a3n.pdb`, chain `A` | Sample CSV/FASTA files, entropy CSV files, LL CSV files in `output/` |
| `4-folding` CLI | `fold_esmfold.py` | `input.fasta` | `output.pdb` |
| `4-folding` notebook | `folding_notebook.ipynb` | `data/1a3n_chainA_samples_t1.00.csv` | 11 PDB files in `output/` |

## Current Validation Results

The existing workflows were run separately in their intended Docker images. No extra test inputs were invented.

### `1-embedding`

- Notebook executed successfully in `esm2_esmif:cu130`.
- Loaded `esm.pretrained.esm2_t33_650M_UR50D()`.
- Generated per-residue embeddings with shape `142 x 1280`.
- Generated per-sequence embedding with shape `1280`.

### `2-mutagenesis`

- Notebook executed successfully in `esm2_esmif:cu130`.
- Regenerated `2-mutagenesis/output/Hemo_AA_probabilities.csv`.
- Regenerated `2-mutagenesis/output/Hemo_shannon_entropy.defattr`.
- Output counts:
  - amino-acid probability CSV: 142 rows, 22 columns.
  - ChimeraX entropy `.defattr`: 142 residue entries.

### `3-if`

- Notebook executed successfully in `esm2_esmif:cu130`.
- Loaded `esm_if1_gvp4_t16_142M_UR50`.
- Extracted native chain A sequence from `data/1a3n.pdb`.
- Sampled 10 sequences each at temperatures `0.50`, `1.00`, and `2.00`.
- Regenerated all CSV, FASTA, entropy, and LL outputs.
- Output counts for each temperature:
  - sample CSV: 11 rows, including native sequence plus 10 sampled sequences.
  - FASTA: 11 records.
  - entropy CSV: 141 rows.
  - LL CSV: 11 rows.

The inverse-folding backbone sequence has 141 residues because chain A extracted from `1a3n.pdb` starts with `VLS...`. The ESM2 mutagenesis notebook uses a separate 142-residue sequence starting with `MVLS...`.

### `4-folding`

- CLI executed successfully in `esmfold-full:cu128`.
- Regenerated `4-folding/output.pdb` from `4-folding/input.fasta`.
- `output.pdb` contains 2206 atom records, 289 residues, and chains `A` and `B`.
- Notebook executed successfully in `esmfold-full:cu128`.
- Regenerated 11 PDB files in `4-folding/output/` from `data/1a3n_chainA_samples_t1.00.csv`.
- The notebook PDB files each contain one folded chain from the native/sample sequence table.

## Troubleshooting

- If Docker reports no GPU-capable device, check Docker Desktop WSL2 integration, NVIDIA drivers, and the NVIDIA Container Toolkit setup.
- The ESM-IF warning about missing regression weights is expected for contact prediction and does not block the inverse-folding sampling/scoring used here.
- ESMFold may emit `FutureWarning` messages from DeepSpeed/OpenFold internals; these warnings were non-fatal during validation.
- If ESMFold runs out of memory, reduce `--chunk-size`, reduce `--num-recycles`, or keep `--precision bf16`.

## Version-Control Notes

- Output directories are intentionally kept.
- No cleanup step is required before pushing if you want to include the generated artifacts.
- If this folder is not already a Git repository, initialize Git or place it inside the intended repository before committing.
