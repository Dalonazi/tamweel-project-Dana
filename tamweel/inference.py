"""Predict features only; apply the frozen policy once to the complete batch."""
import argparse
from pathlib import Path
import sys
import pandas as pd

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT/'scripts'))
from inference import predict


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--model', type=Path, default=PROJECT/'artifacts/final_model')
    args = p.parse_args()
    if args.input.resolve() == args.output.resolve():
        p.error('Input and output must be different files.')
    frame = pd.read_csv(args.input)
    predictions = predict(frame, args.model)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    predictions.to_csv(args.output, index=False)
    print(f'PREDICTIONS_WRITTEN: {len(predictions)} unique application IDs; no labels used.')


if __name__ == '__main__':
    main()
