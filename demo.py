#!/usr/bin/env python3
"""
PS-05 Document Understanding System Demo

This script demonstrates the capabilities of the PS-05 system
by processing sample documents and showing the results.
"""

import cv2
import numpy as np
import json
import tempfile
import os
from pathlib import Path

from src.pipeline.infer_page import PS05Pipeline

def create_sample_document():
    """Create a sample document image for demonstration."""
    # Create a white background
    img = np.ones((1200, 800, 3), dtype=np.uint8) * 255
    
    # Add title
    cv2.putText(img, "Sample Document", (50, 100), 
               cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)
    
    # Add subtitle
    cv2.putText(img, "Multilingual Document Understanding", (50, 150), 
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    
    # Add text content
    cv2.putText(img, "This is a sample document for testing", (50, 250), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    cv2.putText(img, "the PS-05 document understanding system.", (50, 280), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    
    # Add Hindi text
    cv2.putText(img, "यह एक नमूना दस्तावेज़ है", (50, 350), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    
    # Add Arabic text
    cv2.putText(img, "هذا مستند عينة", (50, 400), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    
    # Add a simple table-like structure
    cv2.rectangle(img, (50, 500), (750, 700), (0, 0, 0), 2)
    cv2.line(img, (50, 550), (750, 550), (0, 0, 0), 2)
    cv2.line(img, (200, 500), (200, 700), (0, 0, 0), 2)
    cv2.line(img, (400, 500), (400, 700), (0, 0, 0), 2)
    
    cv2.putText(img, "Column 1", (70, 530), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    cv2.putText(img, "Column 2", (220, 530), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    cv2.putText(img, "Column 3", (420, 530), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    
    cv2.putText(img, "Data 1", (70, 580), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    cv2.putText(img, "Data 2", (220, 580), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    cv2.putText(img, "Data 3", (420, 580), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    
    # Add a simple chart-like structure
    cv2.rectangle(img, (50, 750), (350, 1100), (0, 0, 0), 2)
    cv2.putText(img, "Sample Chart", (70, 780), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    
    # Draw some bars
    cv2.rectangle(img, (80, 900), (120, 1050), (255, 0, 0), -1)
    cv2.rectangle(img, (140, 950), (180, 1050), (0, 255, 0), -1)
    cv2.rectangle(img, (200, 850), (240, 1050), (0, 0, 255), -1)
    
    return img

def run_demo():
    """Run the PS-05 system demo."""
    print("🚀 PS-05 Document Understanding System Demo")
    print("=" * 50)
    
    # Create sample document
    print("📄 Creating sample document...")
    sample_img = create_sample_document()
    
    # Save to temporary file
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        cv2.imwrite(tmp.name, sample_img)
        image_path = tmp.name
    
    try:
        # Initialize pipeline
        print("🔧 Initializing PS-05 pipeline...")
        pipeline = PS05Pipeline()
        
        # Stage 1: Layout Detection
        print("\n📊 Stage 1: Layout Detection")
        print("-" * 30)
        result1 = pipeline.process_image(image_path, stage=1)
        
        print(f"✅ Processing time: {result1.get('processing_time', 0):.2f}s")
        print(f"📏 Image size: {result1['size']['w']}x{result1['size']['h']}")
        print(f"🔍 Detected {len(result1['elements'])} layout elements:")
        
        for i, element in enumerate(result1['elements']):
            print(f"  {i+1}. {element['cls']} (confidence: {element['score']:.3f})")
        
        # Stage 2: OCR and Language ID
        print("\n📝 Stage 2: OCR and Language Identification")
        print("-" * 40)
        result2 = pipeline.process_image(image_path, stage=2)
        
        if 'text_lines' in result2:
            print(f"📄 Detected {len(result2['text_lines'])} text lines:")
            for i, line in enumerate(result2['text_lines'][:5]):  # Show first 5
                print(f"  {i+1}. '{line['text']}' ({line['lang']}, confidence: {line['score']:.3f})")
        
        # Stage 3: Natural Language Generation
        print("\n🤖 Stage 3: Natural Language Generation")
        print("-" * 35)
        result3 = pipeline.process_image(image_path, stage=3)
        
        if 'tables' in result3 and result3['tables']:
            print(f"📊 Table analysis: {result3['tables'][0]['summary']}")
        
        if 'charts' in result3 and result3['charts']:
            print(f"📈 Chart analysis: {result3['charts'][0]['summary']}")
        
        # Save results
        output_dir = Path("demo_output")
        output_dir.mkdir(exist_ok=True)
        
        # Save sample image
        cv2.imwrite(str(output_dir / "sample_document.png"), sample_img)
        
        # Save results
        with open(output_dir / "stage1_results.json", 'w') as f:
            json.dump(result1, f, indent=2, ensure_ascii=False)
        
        with open(output_dir / "stage2_results.json", 'w') as f:
            json.dump(result2, f, indent=2, ensure_ascii=False)
        
        with open(output_dir / "stage3_results.json", 'w') as f:
            json.dump(result3, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results saved to {output_dir}/")
        print("📁 Files created:")
        print("  - sample_document.png")
        print("  - stage1_results.json")
        print("  - stage2_results.json")
        print("  - stage3_results.json")
        
        # Performance summary
        print("\n📈 Performance Summary")
        print("-" * 20)
        print(f"Stage 1 time: {result1.get('processing_time', 0):.2f}s")
        print(f"Stage 2 time: {result2.get('processing_time', 0):.2f}s")
        print(f"Stage 3 time: {result3.get('processing_time', 0):.2f}s")
        
        total_time = result3.get('processing_time', 0)
        print(f"Total processing time: {total_time:.2f}s")
        
        if total_time > 0:
            throughput = 1.0 / total_time
            print(f"Throughput: {throughput:.2f} pages/second")
        
        print("\n✅ Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        if os.path.exists(image_path):
            os.remove(image_path)

def show_usage_examples():
    """Show usage examples."""
    print("\n📚 Usage Examples")
    print("=" * 20)
    print("""
# Single image inference
python ps05.py infer --input document.png --output results/ --stage 3

# Batch processing
python ps05.py infer --input data/images/ --output results/ --batch --stage 3

# Model training
python ps05.py train --data data/train/ --output models/ --epochs 100

# Start API server
python ps05.py server --host 0.0.0.0 --port 8000

# API request example
curl -X POST "http://localhost:8000/api/v1/infer?stage=3" \\
     -H "Content-Type: multipart/form-data" \\
     -F "file=@document.png"
    """)

if __name__ == "__main__":
    run_demo()
    show_usage_examples() 