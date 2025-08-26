import { MD3LightTheme, MD3DarkTheme } from 'react-native-paper';

export const theme = {
  ...MD3LightTheme,
  colors: {
    ...MD3LightTheme.colors,
    primary: '#2196F3',
    secondary: '#FF9800',
    accent: '#4CAF50',
    background: '#F5F5F5',
    surface: '#FFFFFF',
    error: '#F44336',
    text: '#212121',
    onSurface: '#212121',
    disabled: '#BDBDBD',
    placeholder: '#757575',
    backdrop: 'rgba(0, 0, 0, 0.5)',
  },
  roundness: 8,
};

export const darkTheme = {
  ...MD3DarkTheme,
  colors: {
    ...MD3DarkTheme.colors,
    primary: '#90CAF9',
    secondary: '#FFB74D',
    accent: '#81C784',
    background: '#121212',
    surface: '#1E1E1E',
    error: '#EF5350',
    text: '#FFFFFF',
    onSurface: '#FFFFFF',
    disabled: '#757575',
    placeholder: '#BDBDBD',
    backdrop: 'rgba(0, 0, 0, 0.7)',
  },
  roundness: 8,
}; 