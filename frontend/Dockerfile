FROM node:16-alpine

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

RUN npm install -g serve

EXPOSE 3000

ENV NODE_ENV production

CMD ["serve", "-s", "build", "-l", "3000"]