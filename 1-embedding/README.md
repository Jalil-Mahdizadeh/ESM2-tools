# ESM2 Embedding Notebook

`embedding.ipynb` generates ESM2 embeddings for a protein sequence.

## Purpose

The notebook:

1. Checks the PyTorch/CUDA environment.
2. Loads `esm.pretrained.esm2_t33_650M_UR50D()`.
3. Converts the sequence into ESM2 tokens.
4. Extracts layer 33 per-residue representations.
5. Averages residue embeddings into a per-sequence embedding.
6. Optionally displays an ESM2 contact map if matplotlib is available.

Alternative larger ESM2 models are left commented in the notebook:

- `esm2_t36_3B_UR50D`
- `esm2_t48_15B_UR50D`

## Input

The input sequence is defined directly in the notebook as:

- ID: `protein1`
- Length: 142 residues
- Sequence starts with `MVLSPADK...`

Edit the `data = [...]` cell to embed additional sequences.

## Output

This notebook currently prints outputs instead of writing files:

- per-residue embedding tensor with shape `sequence_length x 1280`.
- per-sequence embedding tensor with shape `1280`.
- optional contact-map visualization.

Validated output for the current sequence:

- per-residue embedding shape: `142 x 1280`.
- per-sequence embedding shape: `1280`.

## Run

From this folder:

```powershell
docker run --gpus all -it --rm --entrypoint /bin/bash -v "${PWD}:/workspace" -w /workspace esm2_esmif:cu130
```

Then attach VS Code to the running container, open `/workspace/embedding.ipynb`, select the container Python kernel, and run all cells.

To run from the repository root instead:

```powershell
cd path\to\ESM2
docker run --gpus all -it --rm --entrypoint /bin/bash -v "${PWD}:/workspace" -w /workspace/1-embedding esm2_esmif:cu130
```

## Notes

- The notebook uses CUDA automatically when `torch.cuda.is_available()` is true.
- The output is large because residue embeddings contain one 1280-dimensional vector per residue.
- Add explicit `torch.save`, `numpy.save`, or CSV export cells if persistent embedding files are needed later.
