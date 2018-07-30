# olxscrapper
Scrap OLX 

First you need to install docker/docker toolbox
Then execute 
```
docker build -t olxscrapper .

docker run --name olx --privileged -p 4000:4000 -d -it olxscrapper

sh start.sh
```
