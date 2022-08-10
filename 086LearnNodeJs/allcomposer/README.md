# allcomposer

Crawls PHP composer packages database

# usage

This simple steps will produce local version of the bower graph:

```
git clone https://github.com/anvaka/allcomposer
cd allcomposer
npm install
node index.js
node layout.js
node toBinary.js
```

The ouptut is stored to `./data` folder, and can be consumed by [pm visualization](https://github.com/anvaka/pm)

# license

MIT
