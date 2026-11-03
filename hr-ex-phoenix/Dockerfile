FROM docker.mci.dev/node:24-slim AS build
WORKDIR /app
RUN printf 'Acquire::http { Proxy "http://apt-cacher.mci.dev:27246/"; }\nAcquire::https { Proxy "http://apt-cacher.mci.dev:27246/"; }\n' \
    > /etc/apt/apt.conf.d/01apt-proxy.conf \
    && apt-get update \
    && apt-get install -y --no-install-recommends python3 \
    && rm -rf /var/lib/apt/lists/*
RUN npm config set registry https://repo.mci.dev/artifactory/api/npm/npm
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM docker.mci.dev/nginx:1.27-alpine AS runner
WORKDIR /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist ./

EXPOSE 5173
CMD ["nginx", "-g", "daemon off;"]
