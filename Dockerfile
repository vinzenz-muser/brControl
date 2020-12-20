FROM node:lts-alpine as build-stage
WORKDIR /dashboard
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage

RUN rm /usr/share/nginx/html/*
RUN mkdir /usr/share/nginx/html/dash
COPY --from=build-stage /app/dist /usr/share/nginx/html/dash

CMD ["nginx", "-g", "daemon off;"]
