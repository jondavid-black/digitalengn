# Build stage
FROM node:20-slim AS builder
WORKDIR /app
COPY package*.json ./
COPY docsengn/package*.json ./docsengn/
RUN npm install
COPY . .
RUN npm run build -w docsengn

# Production stage
FROM node:20-slim
WORKDIR /app
COPY --from=builder /app/docsengn/package*.json ./
RUN npm install --omit=dev
COPY --from=builder /app/docsengn/build ./build
EXPOSE 3000
ENV NODE_ENV=production
CMD ["node", "build"]
