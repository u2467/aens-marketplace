echo "aecli inspect $MERCHANT_ADDRESS"
aecli inspect $MERCHANT_ADDRESS
export ACCOUNT_KEYSTORE_PATH=MERCHANT
echo "./sell_names deploy"
./sell_names.py deploy
echo "aecli inspect $ALICE_ADDRESS"
aecli inspect $ALICE_ADDRESS
echo "aecli inspect $BOB_ADDRESS"
aecli inspect $BOB_ADDRESS
echo "aecli inspect $CONTRACT_ADDRESS"
aecli inspect $CONTRACT_ADDRESS
echo "export ACCOUNT_KEYSTORE_PATH=ALICE"
export ACCOUNT_KEYSTORE_PATH=ALICE
echo "./sell_names.py claim $AE_NAME"
./sell_names.py claim $AE_NAME
echo "aecli inspect $AE_NAME"
aecli inspect $AE_NAME
echo "./sell_names.py sell $AE_NAME 100ae"
./sell_names.py sell $AE_NAME 100ae
echo "export ACCOUNT_KEYSTORE_PATH=BOB"
export ACCOUNT_KEYSTORE_PATH=BOB
echo "./sell_names.py sales"
./sell_names.py sales
echo "./sell_names.py buy $AE_NAME 100ae"
./sell_names.py buy $AE_NAME 100ae
echo "aecli inspect $AE_NAME"
aecli inspect $AE_NAME
echo "./sell_names.py sales"
./sell_names.py sales
echo "aecli inspect $ALICE_ADDRESS"
aecli inspect $ALICE_ADDRESS
echo "aecli inspect $BOB_ADDRESS"
aecli inspect $BOB_ADDRESS
echo "aecli inspect $CONTRACT_ADDRESS"
aecli inspect $CONTRACT_ADDRESS



