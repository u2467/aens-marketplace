AENS Marketplace
================

A marketplace to buy and sell names on the Aeternity blockchain


## Installation

```
pip installl -r requirements.txt
```

## env vars

```
export ACCOUNT_KEYSTORE="account.json"
export CONTRACT_SRC_LOCATION="Marketplace.aes" # can also be an url
export NODE_URL="http://localhost:3013" 
export NODE_INTERNAL_URL="http://localhost:3113" # for dry-run calls 
export COMPILER_URL="https://localhost:3080" 
export CONTRACT_ID="ct_J3zwj9vQnyEdYNijeUxeeSJdHpUNRojRsSdjPdbxugRy86R1R" # to be changed with the results od deploy
export CONTRACT_DEPLOY_AMOUNT="2AE"
```

## Usage

>  It is recommended to use a local node with fast mining since claiming a name take some time (~9m on mainnet / testnet)

Create a [new account](https://aepp-sdk-python.readthedocs.io/en/latest/intro/tutorial05-cli.html#example-usage)

./sell_names.py claim 



