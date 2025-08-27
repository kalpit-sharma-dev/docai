# PS-05 Dataset EDA Report
==================================================

## File Format Analysis
- Total files: 8000
- Image files: 4000
- Annotation files: 4000
- Document files: 0

### Format Distribution:
- .json: 4000 files
- .png: 4000 files

## Image Properties Analysis
- Images analyzed: 100

### Dimensions:
- Width range: 612 - 612 pixels
- Height range: 792 - 792 pixels
- Average width: 612 pixels
- Average height: 792 pixels

### Rotation Analysis:
- Rotation range: 33.94° - 47.88°
- Average rotation: 43.92°
- Rotation std: 1.90°

## Annotation Analysis
- Total annotations: 1049

### Class Distribution:
- Class 1: 732 annotations
- Class 2: 238 annotations
- Class 5: 43 annotations
- Class 4: 36 annotations

### Quality Issues:
- Missing bbox: 0
- Invalid bbox: 0
- Missing class: 0

## Recommendations
1. **Deskewing**: Implement robust deskewing for rotated images
2. **Multi-format Support**: Add support for PDF, DOC, PPT formats
3. **Data Augmentation**: Use rotation, scaling, noise for training
4. **Quality Control**: Validate annotation quality and consistency
5. **Format Conversion**: Convert all inputs to image format for processing