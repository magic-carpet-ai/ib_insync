#!/usr/bin/env python3

import asyncio
import tkinter as tk

from ib_insync import IB, util
from ib_insync.contract import *  # noqa

# specify IB GW/TWS connection parameters
host = 'localhost'      # original '127.0.0.1'
port = 4002             # original 7497
client_id = 2           # original 1


class TkApp:
    """
    Example of integrating with Tkinter.
    """
    def __init__(self):
        # self.ib = IB().connect()
        self.loop = asyncio.get_event_loop()
        self.ib = IB().connect(host, port, client_id)
        self.root = tk.Tk()
        self.root.protocol('WM_DELETE_WINDOW', self._onDeleteWindow)
        self.entry = tk.Entry(self.root, width=50)
        self.entry.insert(0, "Stock('TSLA', 'SMART', 'USD')")
        self.entry.grid()
        self.button = tk.Button(
            self.root, text='Get details', command=self.onButtonClick)
        self.button.grid()
        self.text = tk.Text(self.root)
        self.text.grid()
        self.loop = asyncio.get_event_loop()

    def onButtonClick(self):
        contract = eval(self.entry.get())
        cds = self.ib.reqContractDetails(contract)
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, str(cds))

    def run(self):
        self._onTimeout()
        self.loop.run_forever()

    def _onTimeout(self):
        self.root.update()
        self.loop.call_later(0.03, self._onTimeout)

    def _onDeleteWindow(self):
        self.loop.stop()


if __name__ == '__main__':
    util.patchAsyncio()
    app = TkApp()
    app.run()
