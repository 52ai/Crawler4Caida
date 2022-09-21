#!/bin/sh
rm -rf ./dist
npm run build
cd ./dist
git init
git add .
git commit -m 'push to gh-pages'
## Change the line below to deploy to your gh-pages
git push --force git@github.com:anvaka/map-of-reddit.git main:gh-pages
cd ../
