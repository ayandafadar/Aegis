# ── Stage 1: Build ──
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY demo-app/ ./demo-app/

# ── Stage 2: Production ──
FROM node:20-alpine
WORKDIR /app

# Non-root user for security
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/demo-app ./demo-app
COPY --from=build /app/package.json ./package.json

# Expose default port
EXPOSE 3000

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget -q --spider http://localhost:3000/ || exit 1

CMD ["node", "demo-app/server.js"]
