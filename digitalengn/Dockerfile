# Build stage
FROM node:20-slim AS builder
WORKDIR /app
COPY package*.json ./
COPY digitalengn/package*.json ./digitalengn/
RUN npm install
COPY . .
RUN npm run build -w digitalengn

# Production stage
FROM node:20-slim
WORKDIR /app
COPY --from=builder /app/digitalengn/package*.json ./
RUN npm install --omit=dev
COPY --from=builder /app/digitalengn/build ./build
EXPOSE 3000
ENV NODE_ENV=production
CMD ["node", "build"]
