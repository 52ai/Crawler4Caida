## OpenGalaxy

## Project Briefing

Open Galaxy has built a magnificent open source galaxy through visualization technology, including all repositories and developers in GitHub platform. On the web page, users can use the keyboard to shuttle freely through the whole galaxy, witness the various connections of open source projects, as if they were in the vast universe and deeply feel the grandeur of open source.

## Project Background

In the whole GitHub open source community, millions of developers and projects have already formed a kind of social network through various behaviors. Visualization technology can make this network more clearly show us.

Therefore, we have made some improvements based on the open source project anvaka/pm, calculated the correlation degree between the project and developers through some algorithms, and then laid out the nodes through some gravitational layout algorithms.

Due to the large order of magnitude, ordinary databases are difficult to meet our computing requirements, so we chose Nebula graph to help us build such a huge network.

## Project Value

Visualization is not simply to present elements, but to mine hidden or not so easy to find relationships and attributes through good design. Open galaxy not only has good visual design, but also has deep interaction with users, allowing users to explore freely. For a community or enterprise, such visualization technology plays a very good role in publicity or community analysis.

## Project Design

The OpenGalaxy is a comprehensive project which uses graph database, graph algorithm and graph visualization tools for developers to explore the oepn source world.

* Project architecture

![architecture](http://gar2020.opensource-service.cn/umlrenderer/github/X-lab2017/open-galaxy?path=about/arch.uml)

* Design of the main modules
  * For repo influence calculation, we use scala script on Spark to calculate the PageRank value of all repos during 2021 and import into Nebula graph database.
  * For repo data service, we use Node.js online server to query repo detail data like most related repos and developers network on GitHub from Nebula Graph database directly.
  * For offline graph service, we export repo data from Nebula Graph database by Node.js client and use ngraph lib to calculate the galaxy 3d layout and store the result onto online static storage service.
  * For OpenGalaxy, we use galaxy layout data and pm to generate our OpenGalaxy and customize to add our own data like repo details panel. The repo detail panel will query data from repo data service which will query data directly from Nebula Graph database.

* Internal and external dependencies
  * Data infra: [Clickhouse](https://github.com/ClickHouse/ClickHouse).
  * Spark data process: [Spark & Pregel](https://github.com/apache/spark).
  * Offline data service: [Nebula Node.js client](https://github.com/vesoft-inc/nebula-node), [ngraph layout lib](https://github.com/anvaka/ngraph.offline.layout),
  * Repo Data service: [Nebula Node.js client](https://github.com/vesoft-inc/nebula-node), [egg.js](https://github.com/eggjs/egg).
  * OpenGalaxy: [ngraph pm](https://github.com/anvaka/pm).

## Project Testing

Our project will be automatically deployed at [OpenGalaxy website](https://open-galaxy.x-lab.info/).

We also add a CI procedure on our repo to build the site for every pull request on this repo, the site for pull request will be deployed at https://open-galaxy.x-lab.info/$pull_number, like for [PR#3](https://github.com/X-lab2017/open-galaxy/pull/3) the test URL is https://open-galaxy.x-lab.info/3/.
