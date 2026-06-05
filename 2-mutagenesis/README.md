# ESM2 Mutagenesis and Shannon Entropy

`mutagenesis.ipynb` uses ESM2 masked-token probabilities to estimate amino-acid preferences at each position in a protein sequence.

## Purpose

The notebook:

1. Checks the PyTorch/CUDA environment.
2. Loads `esm.pretrained.esm2_t33_650M_UR50D()`.
3. Masks each residue position one at a time.
4. Predicts amino-acid probabilities for the 20 standard amino acids.
5. Normalizes probabilities over those 20 amino acids.
6. Calculates per-position Shannon entropy.
7. Writes a probability CSV and a ChimeraX `.defattr` entropy file.
8. Plots entropy by residue position.

## Input

The current input is defined directly in the notebook:

- ID: `protein1`
- Display/output name: `Hemo`
- Chain identifier for ChimeraX residue attributes: `A`
- Length: 142 residues
- Sequence starts with `MVLSPADK...`

The folder also contains structure files under `data/`, but the current mutagenesis notebook uses the sequence hard-coded in the notebook rather than reading those PDB files.

## Outputs

Outputs are written to `output/`:

| File | Description |
| --- | --- |
| `Hemo_AA_probabilities.csv` | One row per residue with original residue plus normalized probabilities for `A,C,D,E,F,G,H,I,K,L,M,N,P,Q,R,S,T,V,W,Y`. |
| `Hemo_shannon_entropy.defattr` | ChimeraX residue attribute file with `entropy` values for chain `A`. |

Validated output counts:

- `Hemo_AA_probabilities.csv`: 142 rows, 22 columns.
- `Hemo_shannon_entropy.defattr`: 142 residue entries.

## Run

From this folder:

```powershell
docker run --gpus all -it --rm --entrypoint /bin/bash -v "${PWD}:/workspace" -w /workspace esm2_esmif:cu130
```

Then attach VS Code to the running container, open `/workspace/mutagenesis.ipynb`, select the container Python kernel, and run all cells.

To run from the repository root instead:

```powershell
cd path\to\ESM2
docker run --gpus all -it --rm --entrypoint /bin/bash -v "${PWD}:/workspace" -w /workspace/2-mutagenesis esm2_esmif:cu130
```

## ChimeraX Defattr

The `.defattr` file is written in ChimeraX residue-attribute format:

```text
attribute: entropy
recipient: residues

	/A:1	0.5497271628607883
```

Load it in ChimeraX to color or query residues by entropy.

## Notes

- The notebook masks and evaluates every position separately, so runtime scales roughly linearly with sequence length.
- The probability CSV values are normalized over the 20 standard amino acids, excluding special ESM tokens.
- If a different sequence is used, update both `data`, `chain`, and `pname` in the notebook as needed.
