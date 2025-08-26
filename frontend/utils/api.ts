import axios from 'axios';
import * as FileSystem from 'expo-file-system';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export interface PS05Response {
  page: number;
  size: {
    w: number;
    h: number;
  };
  elements: Array<{
    id: string;
    cls: string;
    bbox: [number, number, number, number];
    score: number;
  }>;
  preprocess: {
    deskew_angle: number;
  };
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
  figures?: Array<{
    bbox: [number, number, number, number];
    summary: string;
    confidence: number;
  }>;
  charts?: Array<{
    bbox: [number, number, number, number];
    type: string;
    summary: string;
    confidence: number;
  }>;
  maps?: Array<{
    bbox: [number, number, number, number];
    summary: string;
    confidence: number;
  }>;
}

export interface HealthResponse {
  status: string;
  timestamp: string;
  version: string;
}

export interface InfoResponse {
  name: string;
  version: string;
  description: string;
  supported_languages: string[];
  supported_stages: number[];
}

export class PS05API {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  async healthCheck(): Promise<HealthResponse> {
    try {
      const response = await axios.get(`${this.baseURL}/health`);
      return response.data;
    } catch (error) {
      throw new Error(`Health check failed: ${error}`);
    }
  }

  async getInfo(): Promise<InfoResponse> {
    try {
      const response = await axios.get(`${this.baseURL}/info`);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to get system info: ${error}`);
    }
  }

  async processDocument(
    imageUri: string,
    stage: number = 3
  ): Promise<PS05Response> {
    try {
      // Create form data
      const formData = new FormData();
      const fileInfo = await FileSystem.getInfoAsync(imageUri);
      
      if (!fileInfo.exists) {
        throw new Error('Image file does not exist');
      }

      // Get file extension
      const extension = imageUri.split('.').pop() || 'jpg';
      const mimeType = `image/${extension}`;

      formData.append('file', {
        uri: imageUri,
        type: mimeType,
        name: `document.${extension}`,
      } as unknown as Blob);

      const response = await axios.post(
        `${this.baseURL}/infer?stage=${stage}`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          timeout: 30000, // 30 seconds timeout
        }
      );

      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        if (error.response) {
          throw new Error(`Server error: ${error.response.data?.detail || error.response.statusText}`);
        } else if (error.request) {
          throw new Error('Network error: Unable to connect to server');
        }
      }
      throw new Error(`Document processing failed: ${error}`);
    }
  }

  async processBatch(
    imageUris: string[],
    stage: number = 3
  ): Promise<PS05Response[]> {
    const results: PS05Response[] = [];
    
    for (const imageUri of imageUris) {
      try {
        const result = await this.processDocument(imageUri, stage);
        results.push(result);
      } catch (error) {
        console.error(`Failed to process ${imageUri}:`, error);
        // Continue with other images
      }
    }
    
    return results;
  }
}

export const ps05API = new PS05API();
export default ps05API;
