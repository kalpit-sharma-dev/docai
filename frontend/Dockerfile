# PS-05 Frontend Dockerfile (React Native/Expo)
FROM node:18-alpine

# Set environment variables
ENV NODE_ENV=development
ENV EXPO_DEVTOOLS_LISTEN_ADDRESS=0.0.0.0
ENV REACT_NATIVE_PACKAGER_HOSTNAME=localhost

# Install system dependencies
RUN apk add --no-cache \
    git \
    curl \
    bash \
    && rm -rf /var/cache/apk/*

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./
COPY app.json ./
COPY babel.config.js ./
COPY tsconfig.json ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Copy source code
COPY . .

# Create necessary directories
RUN mkdir -p /app/assets /app/logs

# Expose ports
EXPOSE 19000 19001 19002

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:19000 || exit 1

# Start Expo development server
CMD ["npm", "start", "--", "--host", "0.0.0.0"]
