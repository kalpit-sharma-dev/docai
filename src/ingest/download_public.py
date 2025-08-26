"""Dataset downloader / connector stubs.
Fill in download/mirroring commands (gsutil / aws s3 / http) for your environment.
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'data' / 'public'

def download_pubLayNet(target_dir=DATA/'pubLayNet'):
    target_dir.mkdir(parents=True, exist_ok=True)
    print('PUBLAYNET downloader placeholder. Please paste your mirror commands (gsutil/rsync).')

def download_docLayNet(target_dir=DATA/'docLayNet'):
    target_dir.mkdir(parents=True, exist_ok=True)
    print('DOCLAYNET downloader placeholder. Please paste your mirror commands (gsutil/rsync).')

def download_icdar_mlt(target_dir=DATA/'icdar_mlt'):
    target_dir.mkdir(parents=True, exist_ok=True)
    print('ICDAR-MLT downloader placeholder. Please paste your mirror commands.')

def download_hi_ocr(target_dir=DATA/'hi_ocr'):
    target_dir.mkdir(parents=True, exist_ok=True)
    print('HI-OCR downloader placeholder. Please paste your mirror commands.')

if __name__ == '__main__':
    print('Run specific functions to mirror datasets to local disk.')
