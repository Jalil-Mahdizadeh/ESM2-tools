#!/usr/bin/env python3
import argparse
import pathlib
import sys
import time

import esm
import torch


def read_sequence(value: str) -> str:
    path = pathlib.Path(value)
    if path.exists():
        text = path.read_text()
    else:
        text = value

    records = []
    current = []
    saw_header = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith(">"):
            saw_header = True
            if current:
                records.append("".join(current))
                current = []
            continue
        current.append(line)
    if current:
        records.append("".join(current))

    if saw_header:
        sequence = ":".join(records)
    else:
        sequence = "".join(text.split())

    sequence = sequence.upper().replace("-", "")
    if not sequence:
        raise ValueError("empty protein sequence")
    return sequence


def main() -> int:
    parser = argparse.ArgumentParser(description="Fold a protein sequence with ESMFold.")
    parser.add_argument("sequence", help="Raw sequence, or path to a FASTA/sequence file")
    parser.add_argument("-o", "--output", default="folded.pdb", help="Output PDB path")
    parser.add_argument("--num-recycles", type=int, default=1, help="Use 4 for default ESMFold accuracy; 1 uses less time/memory")
    parser.add_argument("--chunk-size", type=int, default=32, help="Lower values use less memory")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu", choices=["cuda", "cpu"])
    parser.add_argument("--precision", default="bf16", choices=["bf16", "fp16", "fp32"], help="Use bf16 on this 8 GB Blackwell GPU")
    args = parser.parse_args()

    sequence = read_sequence(args.sequence)
    output_path = pathlib.Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if args.device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested, but torch.cuda.is_available() is false")

    print(f"sequence length: {len(sequence.replace(':', ''))}", file=sys.stderr)
    print(f"device: {args.device}; precision: {args.precision}; chunk_size: {args.chunk_size}; recycles: {args.num_recycles}", file=sys.stderr)

    start = time.time()
    model = esm.pretrained.esmfold_v1().eval()
    if args.device == "cuda":
        if args.precision == "bf16":
            model = model.bfloat16()
        elif args.precision == "fp16":
            model = model.half()
    model = model.to(args.device)
    model.set_chunk_size(args.chunk_size)
    print(f"model loaded in {time.time() - start:.1f}s", file=sys.stderr)

    with torch.no_grad():
        result = model.infer(sequence, num_recycles=args.num_recycles)

    # NumPy cannot export BF16 tensors; cast floating outputs before PDB conversion.
    result = {
        key: value.float() if torch.is_tensor(value) and torch.is_floating_point(value) else value
        for key, value in result.items()
    }
    pdb = model.output_to_pdb(result)[0]
    output_path.write_text(pdb)
    print(f"wrote {output_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
