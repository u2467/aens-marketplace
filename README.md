AENS Marketplace
================

A marketplace to buy and sell names on the Aeternity blockchain


For the demo it is assumed that you have Python v3.7 or above installed 
and configured and docker as well.

Install the python dependencies:

```
pip installl -r requirements.txt
```

start a local node:

```
docker-compose up -d
```

load the environment variables:

```
source .envrc
```

execute the demo steps

```
./run.sh
```

### Cleanup 

It is recommended to stop the node instance and clean the resources after running the demo:

```
docker-compose down -v
```

## See it in action


[![asciicast](https://asciinema.org/a/288926.svg)](https://asciinema.org/a/288926)



