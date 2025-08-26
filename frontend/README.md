# PS-05 Document AI Frontend

A React Native/Expo mobile application for the PS-05 Intelligent Multilingual Document Understanding system.

## Features

- **Document Processing**: Upload and process documents through camera, gallery, or file picker
- **Real-time Analysis**: View processing results with detailed breakdowns
- **Multilingual Support**: Support for 6 languages (English, Hindi, Urdu, Arabic, Nepali, Persian)
- **Stage-based Processing**: Choose between 3 processing stages
- **History Management**: View and manage processing history
- **Settings Configuration**: Customize app behavior and server settings
- **Results Visualization**: Interactive results display with tabbed navigation

## Screens

### Home Screen
- System status monitoring
- Quick access to document processing
- Feature overview
- System information display

### Document Screen
- Multiple input methods (camera, gallery, file picker)
- Processing stage selection
- Real-time progress tracking
- Processing options configuration

### Results Screen
- Tabbed results display (Overview, Layout, Text, Tables, Charts, Figures, Raw Data)
- Interactive element visualization
- Share functionality
- Detailed analysis breakdown

### History Screen
- Processing history with search and filters
- Statistics dashboard
- Export and management features
- Quick access to previous results

### Settings Screen
- Server configuration
- Processing options
- Appearance settings
- Data management

## Installation

1. **Install Dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start Development Server**
   ```bash
   npm start
   ```

3. **Run on Device/Simulator**
   ```bash
   # iOS
   npm run ios
   
   # Android
   npm run android
   
   # Web
   npm run web
   ```

## Configuration

### Server Settings
Update the API base URL in `utils/api.ts`:
```typescript
const API_BASE_URL = 'http://your-server:8000/api/v1';
```

### Environment Variables
Create a `.env` file for environment-specific configuration:
```env
API_BASE_URL=http://localhost:8000
DEBUG_MODE=true
```

## Project Structure

```
frontend/
├── App.tsx                 # Main app component
├── app.json               # Expo configuration
├── package.json           # Dependencies
├── tsconfig.json          # TypeScript configuration
├── babel.config.js        # Babel configuration
├── components/            # Reusable UI components
│   └── DocCard.tsx        # Document card component
├── screens/               # Screen components
│   ├── HomeScreen.tsx     # Home screen
│   ├── DocumentScreen.tsx # Document processing
│   ├── ResultsScreen.tsx  # Results display
│   ├── SettingsScreen.tsx # Settings
│   └── HistoryScreen.tsx  # History management
├── navigation/            # Navigation configuration
│   └── AppNavigator.tsx   # Main navigation
├── utils/                 # Utility functions
│   ├── api.ts            # API service
│   └── theme.ts          # Theme configuration
└── assets/               # Static assets
    ├── icon.png          # App icon
    ├── splash.png        # Splash screen
    └── adaptive-icon.png # Android adaptive icon
```

## API Integration

The frontend communicates with the PS-05 backend through REST API endpoints:

### Endpoints
- `GET /api/v1/health` - Health check
- `GET /api/v1/info` - System information
- `POST /api/v1/infer` - Document processing

### Response Format
```typescript
interface PS05Response {
  page: number;
  size: { w: number; h: number };
  elements: Array<{
    id: string;
    cls: string;
    bbox: [number, number, number, number];
    score: number;
  }>;
  preprocess: { deskew_angle: number };
  processing_time: number;
  text_lines?: Array<{
    id: string;
    bbox: [number, number, number, number];
    text: string;
    lang: string;
    score: number;
    lang_confidence: number;
  }>;
  tables?: Array<{
    bbox: [number, number, number, number];
    summary: string;
    confidence: number;
  }>;
  // ... other fields
}
```

## Development

### Code Style
- Use TypeScript for type safety
- Follow React Native best practices
- Use React Native Paper for UI components
- Implement proper error handling

### Testing
```bash
npm test
```

### Linting
```bash
npm run lint
```

## Deployment

### Building for Production

1. **Configure app.json** with production settings
2. **Build the app**:
   ```bash
   # iOS
   expo build:ios
   
   # Android
   expo build:android
   ```

### App Store Deployment
1. Configure app store credentials
2. Submit build to App Store Connect
3. Configure TestFlight for beta testing

## Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Check server URL in settings
   - Verify backend is running
   - Check network connectivity

2. **Image Upload Issues**
   - Verify camera/gallery permissions
   - Check file size limits
   - Ensure supported image formats

3. **Performance Issues**
   - Optimize image quality settings
   - Reduce processing stage complexity
   - Check device memory usage

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the troubleshooting guide 