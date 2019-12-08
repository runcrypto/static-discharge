import nfc
import ndef
import nfc.snep
import struct
import requests
import bitcoin
import bitcoin.rpc
from lightning import LightningRpc
import random
import os
from subprocess import call

NDEF_FILE = "ln.ndef"

def generate_invoice():
    # Generate the invoice
    l1 = LightningRpc("/home/admin/.lightning/lightning-rpc")
    invoice = l1.invoice(10000,"1n1{}".format(random.random()),"static-discharge")
    return invoice['bolt11']

def create_ndef(message,encoding):
    record = ndef.Record('urn:nfc:ext:ln','invoice', bytes(message,encoding))
    print("Record: {}".format(record))
    encoder = ndef.message_encoder()
    encoder.send(None)
    encoder.send(record)
    # A none message must be sent for the last
    message = encoder.send(None)
    return message

def prepare_data():
    # generate Initial invoice
    invoice = generate_invoice()
    print("generated invoice: {} {}".format(len(invoice), invoice))
    # call external command to create text file

    call(["ndeftool", "text", invoice, "save", NDEF_FILE])
    
while True:
    prepare_data()
    os.system("python3 /home/admin/static-discharge/src/nfcpy/examples/tagtool.py --device 'tty:AMA0' emulate " + NDEF_FILE + " tt3")
    os.remove(NDEF_FILE)
