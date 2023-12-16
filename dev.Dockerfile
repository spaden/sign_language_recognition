FROM node:alpine AS development

ENV NODE_ENV development


WORKDIR /my-app


COPY ./package*.json /react-app


RUN npm install


COPY . .


CMD ["npm","start]

