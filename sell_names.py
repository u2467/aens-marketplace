#!/usr/bin/env python
import argparse
import json
import requests
import os
from aeternity.node import NodeClient, Config
from aeternity.compiler import CompilerClient
from aeternity.contract_native import ContractNative
from aeternity.signing import Account, is_signature_valid
from aeternity import hashing, identifiers, utils


ACCOUNT_KEYSTORE =  os.environ.get("ACCOUNT_KEYSTORE_PATH", "/home/andrea/.config/aeternity/andrea")
CONTRACT_ID = os.environ.get("CONTRACT_ID", "ct_SjidAc7fm3csjUUdWZXZ2EfBs7XNHDHVnKvMAjvBZuvWVngjU")
CONTRACT_DEPLOY_AMOUNT = os.environ.get("CONTRACT_DEPLOY_AMOUNT", "2AE")
CONTRACT_SRC_URI = os.environ.get("CONTRACT_SRC_LOCATION", "Marketplace.aes")
NODE_URL = os.environ.get('NODE_URL', 'https://testnet.aeternity.io')
NODE_INTERNAL_URL = os.environ.get('NODE_INTERNAL_URL', 'https://testnet.aeternity.io')
COMPILER_URL = os.environ.get('COMPILER_URL', 'https://compiler.aepps.com')


def _get_src():
    if CONTRACT_SRC_URI.startswith("http"):
        return requests.get(CONTRACT_SRC_URI).text
    else:
        with open(CONTRACT_SRC_URI) as fp:
            return fp.read()


def _get_cli(debug=False):
    node_cli = NodeClient(Config(
        external_url=NODE_URL,
        internal_url=NODE_INTERNAL_URL,
        blocking_mode=True,
        debug=debug
    ))
    compiler = CompilerClient(compiler_url=COMPILER_URL)
    return node_cli, compiler


def _get_account():
    password = input(f"Enter the password for account {ACCOUNT_KEYSTORE}:\n")
    return Account.from_keystore(ACCOUNT_KEYSTORE, password)


def _get_contract():
    try:
        owner = _get_account()
        # contract
        contract_id = CONTRACT_ID
        # read contract file
        contract_src = _get_src()
        node_cli, compiler = _get_cli(args.debug)
        # name to sell
        return ContractNative(client=node_cli,
                              compiler=compiler,
                              account=owner,
                              source=contract_src,
                              address=contract_id,
                              use_dry_run=True)
    except Exception as e:
        print(e)

def cmd_claim(args):
    owner = _get_account()
    # read contract file
    node_cli, _ = _get_cli(args.debug)
    # name to sell
    name = args.name
    aens = node_cli.AEName(name)
    tx = aens.full_claim_blocking(owner, owner.get_address())
    print(tx)



def cmd_deploy(args):
    try:
        owner = _get_account()
        initial_amount = CONTRACT_DEPLOY_AMOUNT
        # read contract file
        contract_src = _get_src()
        node_cli, compiler = _get_cli(args.debug)
        contract = ContractNative(client=node_cli,
                                  compiler=compiler,
                                  account=owner,
                                  source=contract_src,
                                  use_dry_run=False,
                                  amount=initial_amount
                                  )
        tx = contract.deploy()
        # print the contract _id
        print(tx)
        print(f"export CONTRACT_ID='{contract.address}'")
    except Exception as e:
        print(e)


def cmd_sell(args):
    try:
        owner = _get_account()
        # contract
        contract_id = CONTRACT_ID
        # read contract file
        contract_src = _get_src()
        node_cli, compiler = _get_cli(args.debug)
        # name to sell
        name = args.name
        price = utils.amount_to_aettos(args.price)
        recipient = args.to if args.to is not None else owner.get_address()

        contract = ContractNative(client=node_cli,
                                  compiler=compiler,
                                  account=owner,
                                  source=contract_src,
                                  address=contract_id,
                                  use_dry_run=False
                                  )

        print(f" ** Contract ID: {contract_id}")
        if owner.get_address() == recipient:
            print(f" ** Sell name {name} from {owner.get_address()} to anybody at {args.price} ({price} aettos)")
        else:
            print(f" ** Sell name {name} from {owner.get_address()} to {recipient} at {args.price} ({price} aettos)")
        # create a signature
        signature = contract_aens_transfer_sig(owner, name, contract_id, node_cli.config.network_id)
        print(f"Signature: {hashing.encode(identifiers.SIGNATURE, signature)}")
        # print(f"Is signature valid {is_signature_valid(owner.get_address(), signature, g_data)}")
        # merchant
        info, result = contract.offer(name, price, recipient, signature)
        print(info)
        print(result)

    except Exception as e:
        print(e)


def contract_aens_transfer_sig(owner, name, contract_id, nid):
    # owner address + name_hash + Contract.address
    o_ = hashing.decode(owner.get_address())
    n_ = hashing.decode(hashing.name_id(name))
    c_ = hashing.decode(contract_id)
    print("Signing:")
    print(f"owner   : {owner.get_address()}")
    print(f"name    : {hashing.name_id(name)}")
    print(f"contract: {contract_id}")
    # concat the bytes from owner+namehash+contract
    sig_data = nid.encode("utf8") + o_ + n_ + c_
    # sign the data
    sig = owner.sign(sig_data)
    return sig


def cmd_check_name(args):
    # contract
    contract_id = CONTRACT_ID
    # read contract file
    contract_src = _get_src()
    node_cli, compiler = _get_cli(args.debug)
    # name to sell
    name = args.name
    # first check the name
    # aens = node_cli.AEName(name)
    contract = ContractNative(client=node_cli,
                              compiler=compiler,
                              source=contract_src,
                              address=contract_id,
                              account=_get_account(),
                              use_dry_run=True
                              )
    info, result = contract.get_sale(name)
    print(f"result {info.return_type}, gas used {info.gas_used}")
    print_sale(name, result)

def cmd_sales(args):
    # contract
    contract_id = CONTRACT_ID
    # read contract file
    contract_src = _get_src()
    node_cli, compiler = _get_cli(args.debug)
    # first check the name
    contract = ContractNative(client=node_cli,
                              compiler=compiler,
                              source=contract_src,
                              address=contract_id,
                              account=_get_account(),
                              use_dry_run=True
                              )
    info, result = contract.export_sales()
    print(f"result {info.return_type}, gas used {info.gas_used}")
    for k,v in result.items():
        print_sale(k, v)

def print_sale(name, sale):
    print(f"Name sale for {name}:")
    print(f"Owner: {sale['owner']}")
    print(f"> price {utils.format_amount(sale['price'])}")
    print(f"> lock h {sale['locked_until']}")
    if sale['owner'] == sale['recipient']:
        print(f"> public sale")
    else:
        print(f"> private sale for {sale['recipient']}")


def cmd_buy(args):
    try:
        owner = _get_account()
        # contract
        contract_id = CONTRACT_ID
        # read contract file
        contract_src = _get_src()
        node_cli, compiler = _get_cli(args.debug)
        # name to sell
        contract = ContractNative(client=node_cli,
                                  compiler=compiler,
                                  account=owner,
                                  source=contract_src,
                                  address=contract_id,
                                  use_dry_run=True)
        # name to sell
        name = args.name
        price = utils.amount_to_aettos(args.price)
        info, result = contract.buy(name, amount=price)
        print(info)
        node_cli.AEName(name).update(owner, ("new_owner", owner.get_address()))

    except Exception as e:
        print(e)


if __name__ == "__main__":
    commands = [
        {
            'name': 'sell',
            'help': 'export the secret/public key of a encrypted keystore as plain text WARNING! THIS IS UNSAFE, USE FOR DEV ONLY',
            'target': cmd_sell,
            'opts': [
                {
                    "names": ["name"],
                    "help": "The name to sell",
                },
                {
                    "names": ["price"],
                    "help": "the price to sell for"
                },
                {
                    "names": ["--to"],
                    "help": "the recipient to to sell the name to",
                    "default": None,
                },
                {
                    "names": ["--debug"],
                    "help": "",
                    "action": "store_true",
                    "default": False
                },
            ]
        },
        {
            'name': 'deploy',
            'help': 'export the secret/public key of a encrypted keystore as plain text WARNING! THIS IS UNSAFE, USE FOR DEV ONLY',
            'target': cmd_deploy,
            'opts': [
                {
                    "names": ["--debug"],
                    "help": "",
                    "action": "store_true",
                    "default": False
                },

            ]
        },
        {
            'name': 'buy',
            'help': 'buy a name',
            'target': cmd_buy,
            'opts': [
                {
                    "names": ["name"],
                    "help": "The name to buy",
                },
                {
                    "names": ["price"],
                    "help": "the price to buy it for"
                },
                {
                    "names": ["--debug"],
                    "help": "",
                    "action": "store_true",
                    "default": False
                },
            ]
        },
        {
            'name': 'check',
            'help': "check the price for a name",
            'target': cmd_check_name,
            'opts': [
                {
                    "names": ["name"],
                    "help": "The name to buy",
                },
                {
                    "names": ["--debug"],
                    "help": "",
                    "action": "store_true",
                    "default": False
                },
            ]
        },
        {
            'name': 'sales',
            'help': "check the price for a name",
            'target': cmd_sales,
            'opts': [
                {
                    "names": ["--debug"],
                    "help": "",
                    "action": "store_true",
                    "default": False
                },
            ]
        },
        {
            'name': 'claim',
            'help': "check the price for a name",
            'target': cmd_claim,
            'opts': [
                {
                    "names": ["name"],
                    "help": "The name to buy",
                },
                {
                    "names": ["--debug"],
                    "help": "",
                    "action": "store_true",
                    "default": False
                },
            ]
        },
    ]
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    subparsers.required = True
    subparsers.dest = 'command'
    # register all the commands
    for c in commands:
        subparser = subparsers.add_parser(c['name'], help=c['help'])
        subparser.set_defaults(func=c['target'])
        # add the sub arguments
        for sa in c.get('opts', []):
            subparser.add_argument(*sa['names'],
                                   help=sa['help'],
                                   action=sa.get('action'),
                                   default=sa.get('default'))

    # parse the arguments
    args = parser.parse_args()
    # call the function
    args.func(args)
