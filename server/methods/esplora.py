from server import cache
import config
from server.bitcoin_cli import BitcoinCLI
bitcoin_cli = BitcoinCLI()
class Esplora():
    @classmethod
    @cache.memoize(timeout=config.cache)
    def block(self, result):
        return {
            "id": result["hash"],
            "height": result["height"],
            "version": result["version"],
            "timestamp": result["time"],
            "tx_count": len(result["tx"]),
            "size": result["size"],
            "weight": result["size"],
            "merkle_root": result["merkleroot"],
            "previousblockhash": result["previousblockhash"],
            "nonce": result["nonce"],
            "bits": int(result["bits"], 16),
            "difficulty": result["difficulty"]
        }

    @classmethod
    @cache.memoize(timeout=config.cache)
    def transaction(self, result):
        outputs = []
        inputs = []

        status = {"confirmed": False}
        outputs_amount = 0
        inputs_amount = 0
        coinbase = True
        fee = 0

        for vin in result["vin"]:
            # print('vin', vin)
            print('------')
            input_data = {
                "txid": "0" * 64,
                "sequence": vin["sequence"],
                "prevout": None,
                "is_coinbase": True
            }

            if "txinwitness" in vin:
                input_data["witness"] = vin["txinwitness"]

            if "coinbase" not in vin:
                coinbase = False
                if "value" in vin:
                    inputs_amount += vin["value"]

                input_data["txid"] = vin["txid"]
                # tx_detail = {
                #     'amount': 0
                # }
                # if len(vin['txid']) > 60:
                #     tx_detail = bitcoin_cli.get_transaction(vin['txid'])
                # print('tx_detail', tx_detail)
                input_data["vout"] = vin["vout"]
                input_data["is_coinbase"] = False
                input_data["prevout"] = {
                    "scriptpubkey": vin["scriptSig"]["hex"],
                    "scriptpubkey_asm": vin["scriptSig"]["asm"],
                    "scriptpubkey_type": "type",
                    "scriptpubkey_address": "address",
                    "value": 0
                }

            inputs.append(input_data)

        for vout in result["vout"]:
            print('vout', vout)
            outputs_amount += vout["value"]

            output_data = {
                "scriptpubkey": vout["scriptPubKey"]["hex"],
                "scriptpubkey_asm": vout["scriptPubKey"]["asm"],
                "scriptpubkey_type": vout["scriptPubKey"]["type"],
                "value": 0
            }

            if "addresses" in vout["scriptPubKey"]:
                output_data["scriptpubkey_address"] = vout["scriptPubKey"]["addresses"][0]
                output_data["value"] = vout["value"]

            if output_data["scriptpubkey_type"] == "nulldata":
                output_data["scriptpubkey_type"] = "op_return"

            outputs.append(output_data)

        if not coinbase:
            fee = 0 # inputs_amount - outputs_amount

        if "blockhash" in result:
            status["confirmed"] = True
            status["block_height"] = result["height"]
            status["block_hash"] = result["blockhash"]
            status["block_time"] = result["blocktime"]
        # print(result)
        weight = 0# result["weight"] if "weight" in result else result["size"]

        return {
            "txid": result["txid"],
            "version": result["version"],
            "locktime": result["locktime"],
            "size": 0,
            "weight": weight,
            "fee": fee,
            "vin": inputs,
            "vout": outputs,
            "status": status,
            "value": outputs_amount
        }
