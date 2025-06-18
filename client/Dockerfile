# Stage 1: Build the React app
FROM node:20-alpine AS build

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the code and build
COPY . .
RUN npm run build

# Stage 2: Serve using nginx
FROM nginx:alpine

# Copy the build output to nginx's public directory
COPY --from=build /app/build /usr/share/nginx/html

# Remove default nginx config and replace with custom if needed
# COPY nginx.conf /etc/nginx/nginx.conf  # Optional

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
