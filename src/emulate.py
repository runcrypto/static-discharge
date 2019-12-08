import nfc
import struct
import requests
import bitcoin
import bitcoin.rpc
from lightning import LightningRpc
import random

ndef_data_area = bytearray(64 * 16)
ndef_data_area[0] = 0x10  # NDEF mapping version '1.0'
ndef_data_area[1] = 12    # Number of blocks that may be read at once
ndef_data_area[2] = 8     # Number of blocks that may be written at once
ndef_data_area[4] = 63    # Number of blocks available for NDEF data
ndef_data_area[10] = 1    # NDEF read and write operations are allowed
ndef_data_area[14:16] = struct.pack('>H', sum(ndef_data_area[0:14]))  # Checksum

def ndef_read(block_number, rb, re):
    if block_number < len(ndef_data_area) / 16:
        first, last = block_number*16, (block_number+1)*16
        block_data = ndef_data_area[first:last]
        return block_data

def ndef_write(block_number, block_data, wb, we):
    global ndef_data_area
    if block_number < len(ndef_data_area) / 16:
        first, last = block_number*16, (block_number+1)*16
        ndef_data_area[first:last] = block_data
        return True

def on_startup(target):
    idm, pmm, sys = '03FEFFE011223344', '01E0000000FFFF00', '12FC'
    target.sensf_res = bytearray.fromhex('01' + idm + pmm + sys)
    target.brty = "212F"
    return target

def on_connect(tag):
    print("tag activated")
    tag.add_service(0x0009, ndef_read, ndef_write)
    tag.add_service(0x000B, ndef_read, lambda: False)
    return True

def generate_invoice():
    l1 = LightningRpc("/home/admin/.lightning/lightning-rpc")
    invoice = l1.invoice(500,"lb1{}".format(random.random()),"testpay")
    print("generated invoice: {}".format(invoice['bolt11']))

# generate Initial invoice
generate_invoice()

# start card emulation
with nfc.ContactlessFrontend('tty:AMA0') as clf:
    while clf.connect(card={'on-startup': on_startup, 'on-connect': on_connect}):
        print("tag released")
        generate_invoice()
