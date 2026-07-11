FROM node:24-alpine AS development-dependencies-env
COPY . /app
WORKDIR /app
# --legacy-peer-deps: react-qr-reader@3.0.0-beta-1 pins React 16/17 as a peer,
# which conflicts with this project's React 19.
RUN npm ci --legacy-peer-deps

FROM node:24-alpine AS production-dependencies-env
COPY ./package.json package-lock.json /app/
WORKDIR /app
RUN npm ci --omit=dev --legacy-peer-deps

FROM node:24-alpine AS build-env
COPY . /app/
COPY --from=development-dependencies-env /app/node_modules /app/node_modules
WORKDIR /app
RUN npm run build

FROM node:24-alpine
COPY ./package.json package-lock.json /app/
COPY --from=production-dependencies-env /app/node_modules /app/node_modules
COPY --from=build-env /app/build /app/build
WORKDIR /app
CMD ["npm", "run", "start"]
