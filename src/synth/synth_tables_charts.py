"""Synthetic table and chart image generator (simple) for weak supervision."""
from PIL import Image, ImageDraw, ImageFont
import random, os, json, textwrap

def gen_simple_table(cols=3, rows=4, cell_w=200, cell_h=60):
    w = cols * cell_w + 20
    h = rows * cell_h + 20
    img = Image.new('RGB', (w,h), (255,255,255))
    d = ImageDraw.Draw(img)
    # draw grid
    for i in range(rows+1):
        y = 10 + i*cell_h
        d.line([(10,y),(10+cols*cell_w,y)], fill=(0,0,0))
    for j in range(cols+1):
        x = 10 + j*cell_w
        d.line([(x,10),(x,10+rows*cell_h)], fill=(0,0,0))
    # fill sample text
    font = ImageFont.load_default()
    for r in range(rows):
        for c in range(cols):
            tx = f'R{r+1}C{c+1}'
            x = 10 + c*cell_w + 10
            y = 10 + r*cell_h + 10
            d.text((x,y), tx, font=font, fill=(0,0,0))
    meta = {'type':'table','cols':cols,'rows':rows}
    return img, meta

def gen_simple_bar_chart(series=2, bars=5, w=600, h=400):
    img = Image.new('RGB', (w,h), (255,255,255))
    d = ImageDraw.Draw(img)
    margin = 50
    max_h = h - 2*margin
    spacing = (w - 2*margin) / bars
    for i in range(bars):
        for s in range(series):
            val = random.randint(10,90)
            bar_w = spacing * 0.6 / series
            x0 = margin + i*spacing + s*bar_w
            x1 = x0 + bar_w
            y1 = h - margin
            y0 = y1 - (val/100.0)*max_h
            d.rectangle([x0,y0,x1,y1], outline='black', fill='gray')
    meta = {'type':'bar','series':series,'bars':bars}
    return img, meta

if __name__ == '__main__':
    os.makedirs('debug', exist_ok=True)
    timg, meta = gen_simple_table()
    timg.save('debug/synth_table.png')
    bimg, bmeta = gen_simple_bar_chart()
    bimg.save('debug/synth_barchart.png')
    print('Saved debug examples. Metas:', meta, bmeta)
