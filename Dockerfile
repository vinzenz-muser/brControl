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
COPY entrypoint.sh .
RUN chmod u+x entrypoint.sh

WORKDIR /admin
COPY admin/. .
COPY --from=build-stage /dashboard/dist /admin/static/dash

WORKDIR /migrations
copy migrations/. .

ENV FLASK_APP=admin

WORKDIR /
ENTRYPOINT ["./entrypoint.sh"]
