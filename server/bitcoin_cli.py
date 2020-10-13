from bitcoinrpc.authproxy import AuthServiceProxy
import config

class BitcoinCLI:

    def __init__(self):
        self.rpc_connection = AuthServiceProxy(config.endpoint)

    def get_best_block_hash(self):
        return self.rpc_connection.getbestblockhash()

    def get_block_count(self):
        return self.rpc_connection.getblockcount()

    def get_best_block(self):
        return self.rpc_connection.getblock(self.rpc_connection.getbestblockhash())

    def get_block_hash(self, height):
        return self.rpc_connection.getblockhash(height)

    def get_block(self, hash):
        return self.rpc_connection.getblock(hash)
    def get_transaction(self, hash):
        return self.rpc_connection.gettransaction(hash)

    def get_txn_list_from_block(self, hash):
        block = self.get_block(hash)

        if 'tx' in block:
            return block['tx']
        else:
            raise KeyError('Block {0} has no attribute tx'.format(hash))

    def get_raw_transaction(self, tx_id):
        out = self.rpc_connection.getrawtransaction(tx_id, 1)
        return out
    def decoderawtransaction(self, tx_id):
        out = self.rpc_connection.decoderawtransaction(raw)
        return out

    def get_tx_outputs(self, tx_id):
        tx = self.rpc_connection.getrawtransaction(tx_id, 1)
        outputs = [float(i['value']) for i in tx['vout']]
        return outputs

    def get_tx_details(self, tx_id):
        tx = self.rpc_connection.getrawtransaction(tx_id, 1)
        outputs = [float(i['value']) for i in tx['vout']]
        return outputs