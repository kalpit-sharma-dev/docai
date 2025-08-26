"""Instruction-tuning skeleton for table/chart/map -> NL summarization.
This script demonstrates generating synthetic (intermediate -> NL) pairs and a training loop stub.
"""

import json, os
from pathlib import Path

def generate_synthetic_pairs(num=1000, out='data/synth_pairs.jsonl'):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w') as f:
        for i in range(num):
            # simple synthetic intermediate representation
            interm = {'type':'table','rows': [['A','B'],['C','D']], 'meta': {'rows':2,'cols':2}}
            nl = 'A  B; C  D. Table with 2 rows and 2 columns.'
            obj = {'input': interm, 'output': nl}
            f.write(json.dumps(obj) + '\n')
    print('Wrote', out)

def train_loop(data_path='data/synth_pairs.jsonl'):
    # placeholder training loop: load pairs, fine-tune a seq2seq model (e.g., T5) with LoRA/PEFT
    print('Train loop placeholder. Open data at', data_path)

if __name__ == '__main__':
    generate_synthetic_pairs(200)
    train_loop()
