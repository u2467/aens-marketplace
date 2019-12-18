echo "Merchant address: $MERCHANT_ADDRESS"
echo "Alice address:    $ALICE_ADDRESS"
echo "Bob address:      $BOB_ADDRESS"
echo "Name being sold:  $AE_NAME"
echo "\nCheck the Merchant balance\n"
echo "aecli inspect $MERCHANT_ADDRESS"
aecli inspect $MERCHANT_ADDRESS
export ACCOUNT_KEYSTORE_PATH=MERCHANT

echo "\nDeploy the Marketplace contract\n"
echo "./sell_names deploy"
./sell_names.py deploy
echo "aecli inspect $ALICE_ADDRESS"

echo "\nCheck Alice, Bob and the contract account balances\n"
aecli inspect $ALICE_ADDRESS
echo "aecli inspect $BOB_ADDRESS"
aecli inspect $BOB_ADDRESS
echo "aecli inspect $CONTRACT_ADDRESS"
aecli inspect $CONTRACT_ADDRESS

echo "\nLet Alice claim the name $AE_NAME\n"
echo "export ACCOUNT_KEYSTORE_PATH=ALICE"
export ACCOUNT_KEYSTORE_PATH=ALICE
echo "./sell_names.py claim $AE_NAME"
./sell_names.py claim $AE_NAME
echo "aecli inspect $AE_NAME"
aecli inspect $AE_NAME

echo "\nLet Alice put the name on sale\n"
echo "./sell_names.py sell $AE_NAME 100ae"
./sell_names.py sell $AE_NAME 100ae

echo "\nNow Bob will list the available names for sale\n"
echo "export ACCOUNT_KEYSTORE_PATH=BOB"
export ACCOUNT_KEYSTORE_PATH=BOB
echo "./sell_names.py sales"
./sell_names.py sales

echo "\nAnd will buy the name that Alice put on sale\n"
echo "./sell_names.py buy $AE_NAME 100ae"
./sell_names.py buy $AE_NAME 100ae
echo "aecli inspect $AE_NAME"
aecli inspect $AE_NAME

echo "\nThe name is not on sale anymore\n"
echo "./sell_names.py sales"
./sell_names.py sales

echo "\nAnd lets check how the balances have changed\n"
echo "aecli inspect $ALICE_ADDRESS"
aecli inspect $ALICE_ADDRESS
echo "aecli inspect $BOB_ADDRESS"
aecli inspect $BOB_ADDRESS
echo "aecli inspect $CONTRACT_ADDRESS"
aecli inspect $CONTRACT_ADDRESS



