# -----------------------------------------------------------------------------
# STAGE 1: Build the React Application
# -----------------------------------------------------------------------------
FROM node:18-alpine as build

# Set working directory
WORKDIR /app

# Copy package files first to leverage Docker layer caching
COPY package*.json ./

# Install dependencies
# CHANGED: Using 'npm install' because 'npm ci' requires an existing package-lock.json
RUN npm install

# Copy the rest of the source code
COPY . .

# Build the application for production
RUN npm run build

# -----------------------------------------------------------------------------
# STAGE 2: Serve with Nginx
# -----------------------------------------------------------------------------
FROM nginx:stable-alpine

# Remove default Nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy the build output from Stage 1 to Nginx html directory
# NOTE: If you use Vite, the folder is /app/dist. For Create React App, it is /app/build.
COPY --from=build /app/build /usr/share/nginx/html

# Copy custom Nginx configuration for SPA routing
# This is the internal nginx config for the frontend container, not the main gateway config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]