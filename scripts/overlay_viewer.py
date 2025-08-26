import argparse
from pathlib import Path
import json
import cv2
import numpy as np

COLOR_MAP = {
    "Background": (200, 200, 200),
    "Text": (255, 153, 0),
    "Title": (0, 153, 255),
    "List": (76, 175, 80),
    "Table": (156, 39, 176),
    "Figure": (244, 67, 54),
}


def draw_bbox(img, bbox, color, label=None):
    x, y, w, h = map(int, bbox)
    cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
    if label:
        cv2.rectangle(img, (x, y - 20), (x + min(220, w), y), color, -1)
        cv2.putText(img, label, (x + 4, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)


def overlay(image_path: Path, json_path: Path, stage: int, out_path: Path):
    img = cv2.imread(str(image_path))
    if img is None:
        raise RuntimeError(f"Failed to read image: {image_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Stage 1: elements
    for el in data.get("elements", []):
        cls = el.get("cls", "Text")
        color = COLOR_MAP.get(cls, (0, 255, 255))
        score = el.get("score", 0)
        label = f"{cls} {score:.2f}"
        draw_bbox(img, el.get("bbox", [0, 0, 0, 0]), color, label)

    # Stage 2: text lines
    if stage >= 2:
        for tl in data.get("text_lines", []):
            draw_bbox(img, tl.get("bbox", [0, 0, 0, 0]), (0, 255, 255), tl.get("lang", ""))

    # Stage 3: tables/figures/charts/maps
    if stage >= 3:
        for key, color in ("tables", (102, 0, 204)), ("figures", (0, 0, 255)), ("charts", (0, 102, 204)), ("maps", (0, 204, 102)):
            for item in data.get(key, []):
                label = key[:-1].capitalize()
                if key == "charts":
                    label = f"Chart:{item.get('type', 'unk')}"
                draw_bbox(img, item.get("bbox", [0, 0, 0, 0]), color, label)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out_path), img)
    return out_path


def main():
    ap = argparse.ArgumentParser(description="Overlay viewer for PS-05 outputs")
    ap.add_argument("--image", required=True)
    ap.add_argument("--json", required=True)
    ap.add_argument("--stage", type=int, default=3, choices=[1, 2, 3])
    ap.add_argument("--out", required=True, help="Output overlay image path")
    args = ap.parse_args()

    out = overlay(Path(args.image), Path(args.json), args.stage, Path(args.out))
    print(f"Overlay written: {out}")


if __name__ == "__main__":
    main() 