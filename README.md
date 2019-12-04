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

## COMMANDS DEMO LIST

you need a fresh node and a compiler available locally

```
source .envrc
aecli account spend ~/.config/aeternity/genesis.json $MERCHANT_ADDRESS 500ae
aecli account spend ~/.config/aeternity/genesis.json $ALICE_ADDRESS 500ae
aecli account spend ~/.config/aeternity/genesis.json $BOB_ADDRESS 500ae
aecli inspect $MERCHANT_ADDRESS
export ACCOUNT_KEYSTORE_PATH=MERCHANT
./sell_names.py deploy
aecli inspect $ALICE_ADDRESS
aecli inspect $BOB_ADDRESS
aecli inspect $CONTRACT_ADDRESS
export ACCOUNT_KEYSTORE_PATH=ALICE
./sell_names.py claim $AE_NAME
aecli inspect $AE_NAME
./sell_names.py sell $AE_NAME 100ae
export ACCOUNT_KEYSTORE_PATH=BOB
./sell_names.py sales
./sell_names.py buy $AE_NAME 100ae
aecli inspect $AE_NAME
./sell_names.py sales
aecli inspect $ALICE_ADDRESS
aecli inspect $BOB_ADDRESS
aecli inspect $CONTRACT_ADDRESS
```








