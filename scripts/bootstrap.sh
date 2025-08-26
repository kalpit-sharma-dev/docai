#!/usr/bin/env bash
set -e
echo "Creating data directories..."
mkdir -p data/public/pubLayNet
mkdir -p data/public/docLayNet
mkdir -p data/public/icdar_mlt
mkdir -p data/public/hi_ocr
mkdir -p data/challenge/train_set
mkdir -p outputs/checkpoints
echo "Bootstrap complete. Please populate data directories or add download URLs in src/ingest/*"
