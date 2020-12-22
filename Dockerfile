FROM node:lts-alpine as build-stage
WORKDIR /dashboard
COPY dashboard/package*.json ./
RUN npm install
COPY /dashboard/. .
RUN npm run build

# production stage
FROM python:3-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /
COPY config.py .

WORKDIR /admin
COPY admin/. .
COPY --from=build-stage /dashboard/dist /admin/static/dash

WORKDIR /
CMD ["waitress-serve", "admin:app"]
