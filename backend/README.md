# PS-05 Document AI Backend

A powerful, scalable backend service for intelligent multilingual document understanding and analysis.

## Features

- **Multilingual OCR**: Support for English, Hindi, Urdu, Arabic, Nepali, and Persian
- **Layout Detection**: Automatic detection of text, titles, lists, tables, and figures
- **Language Identification**: Automatic language detection with confidence scores
- **Natural Language Generation**: Intelligent summaries for tables, charts, and figures
- **Three Processing Stages**: Configurable processing levels for different use cases
- **RESTful API**: Clean, well-documented API endpoints
- **Async Processing**: Background processing for large documents
- **Batch Processing**: Process multiple documents simultaneously
- **File Management**: Secure file upload, validation, and storage
- **Database Integration**: SQLite (development) and PostgreSQL (production) support

## Processing Stages

### Stage 1: Layout Detection
- Detect document layout elements
- Generate bounding boxes
- Calculate confidence scores
- Element classification (text, title, list, table, figure)

### Stage 2: OCR + Language ID
- Extract text from detected elements
- Automatic language identification
- Multilingual text recognition
- Confidence scoring for OCR and language detection

### Stage 3: Full Analysis
- Table structure analysis
- Chart detection and description
- Figure identification and summarization
- Map analysis and description
- Natural language summaries

## API Endpoints

### Core Endpoints
- `POST /api/v1/upload` - Upload and process document
- `POST /api/v1/upload/async` - Upload for async processing
- `GET /api/v1/status/{document_id}` - Check processing status
- `GET /api/v1/documents` - List all documents
- `DELETE /api/v1/documents/{document_id}` - Delete document

### Batch Processing
- `POST /api/v1/batch` - Process multiple documents

### System Information
- `GET /api/v1/health` - Health check
- `GET /api/v1/info` - System information
- `GET /api/v1/metrics` - Performance metrics
- `GET /api/v1/languages` - Supported languages
- `GET /api/v1/stages` - Processing stage information

### Storage Management
- `GET /api/v1/storage/stats` - Storage statistics
- `POST /api/v1/storage/backup` - Create backup
- `POST /api/v1/storage/restore` - Restore from backup

## Installation

### Prerequisites
- Python 3.11+
- OpenCV dependencies
- Tesseract OCR (optional)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

### Docker Installation

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Or build and run manually**
   ```bash
   docker build -t ps05-backend .
   docker run -p 8000:8000 ps05-backend
   ```

## Configuration

### Environment Variables
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `DEBUG`: Debug mode (default: false)
- `DATABASE_URL`: Database connection string
- `UPLOAD_DIR`: File upload directory
- `MODEL_CACHE_DIR`: AI model cache directory
- `MAX_FILE_SIZE`: Maximum file size in bytes
- `SUPPORTED_LANGUAGES`: Comma-separated language codes

### Configuration File
Edit `app/config/settings.py` to modify default settings.

## Usage Examples

### Upload and Process Document

```python
import requests

# Upload document
with open('document.jpg', 'rb') as f:
    files = {'file': f}
    data = {
        'stage': 3,  # Full analysis
        'high_quality': True,
        'language_hint': 'en'
    }
    
    response = requests.post(
        'http://localhost:8000/api/v1/upload',
        files=files,
        data=data
    )
    
    result = response.json()
    print(f"Document ID: {result['document_id']}")
    print(f"Status: {result['status']}")
```

### Check Processing Status

```python
import requests

document_id = "your-document-id"
response = requests.get(f'http://localhost:8000/api/v1/status/{document_id}')
result = response.json()

if result['status'] == 'completed':
    print("Processing completed!")
    print(f"Elements detected: {len(result['result']['elements'])}")
    if result['result']['text_lines']:
        print(f"Text lines: {len(result['result']['text_lines'])}")
```

### Batch Processing

```python
import requests

batch_request = {
    "documents": ["doc1.jpg", "doc2.jpg", "doc3.jpg"],
    "stage": 2,
    "priority": 5
}

response = requests.post(
    'http://localhost:8000/api/v1/batch',
    json=batch_request
)

result = response.json()
print(f"Batch ID: {result['batch_id']}")
print(f"Total documents: {result['total_documents']}")
```

## Development

### Project Structure
```
backend/
├── app/
│   ├── controllers/     # API controllers
│   ├── models/         # Database models and schemas
│   ├── services/       # Business logic services
│   ├── database/       # Database configuration
│   └── config/         # Settings and configuration
├── tests/              # Test files
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── docker-compose.yml # Docker Compose setup
└── run.py            # Application runner
```

### Running Tests
```bash
pytest tests/
```

### Code Quality
```bash
# Linting
flake8 app/
black app/

# Type checking
mypy app/
```

## Deployment

### Production Considerations
- Use PostgreSQL instead of SQLite
- Enable Redis for caching and job queues
- Set up proper logging and monitoring
- Configure CORS origins appropriately
- Use environment variables for sensitive configuration
- Set up SSL/TLS certificates
- Configure proper file storage (S3, etc.)

### Environment Variables for Production
```bash
export DEBUG=false
export DATABASE_URL=postgresql://user:pass@host:port/db
export REDIS_URL=redis://host:port
export SECRET_KEY=your-secure-secret-key
export MAX_FILE_SIZE=104857600  # 100MB
```

### Docker Production
```bash
# Build production image
docker build -t ps05-backend:prod .

# Run with production settings
docker run -d \
  -p 8000:8000 \
  -e DEBUG=false \
  -e DATABASE_URL=postgresql://... \
  ps05-backend:prod
```

## Performance

### Optimization Tips
- Use appropriate processing stage for your needs
- Enable high-quality processing only when necessary
- Use async processing for large documents
- Implement proper caching strategies
- Monitor system resources

### Benchmarks
- **Stage 1 (Layout)**: ~2-5 seconds per document
- **Stage 2 (OCR)**: ~5-15 seconds per document
- **Stage 3 (Full)**: ~10-30 seconds per document
- **Batch Processing**: Scales with available resources

## Troubleshooting

### Common Issues

1. **OpenCV Installation Problems**
   ```bash
   # Install system dependencies first
   sudo apt-get install libgl1-mesa-glx libglib2.0-0
   ```

2. **EasyOCR Model Download Issues**
   - Check internet connection
   - Verify model cache directory permissions
   - Clear model cache if corrupted

3. **Memory Issues**
   - Reduce batch size
   - Use lower quality processing
   - Monitor system memory usage

4. **Database Connection Issues**
   - Verify database URL
   - Check database permissions
   - Ensure database is running

### Logs
Check application logs for detailed error information:
```bash
# If running with Docker
docker logs ps05-document-ai-backend

# If running locally
tail -f logs/app.log
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the API documentation at `/docs` endpoint

## Acknowledgments

- EasyOCR for multilingual OCR capabilities
- OpenCV for computer vision processing
- FastAPI for the modern web framework
- SQLAlchemy for database ORM
