# --------------> The build image
FROM node:20 AS builder
WORKDIR /usr/src/app
# Set node options
# ENV NODE_OPTIONS="--openssl-legacy-provider"
# Install required packages
RUN apt-get update && apt-get install -y --no-install-recommends dumb-init
# Copy package.json and package-lock.json
COPY package*.json /usr/src/app/
# Installs all node packages
RUN npm install --force --silent
# Copies everything over to Docker environment
COPY . ./
# Build the app for production to the build folder
RUN npm run build

# --------------> The production image
FROM node:20-alpine
# Install serve
RUN npm install -g serve
# Copies React to the container directory
WORKDIR /usr/src/app/
# Copies static resources from builder stage
COPY --from=builder /usr/src/app/build build
# Expose port
EXPOSE 3000
# Containers run nginx with global directives and daemon off
CMD [ "serve", "-s", "build" ]
