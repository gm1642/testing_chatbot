# Use the official Node.js image as base
FROM node:16-alpine

# Set working directory inside the container
WORKDIR /app

# Install dependencies
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

# Copy the rest of the application code
COPY . .

# Build the Next.js application
RUN yarn build

# Expose the port Next.js is running on
EXPOSE 3000

# Run the Next.js application
CMD ["yarn", "start"]
