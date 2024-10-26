#!/usr/bin/env python3.7
#
# Copyright (c) 2013-2024 by Ron Frederick <ronf@timeheart.net> and others.
#
# This program and the accompanying materials are made available under
# the terms of the Eclipse Public License v2.0 which accompanies this
# distribution and is available at:
#
#     http://www.eclipse.org/legal/epl-2.0/
#
# This program may also be made available under the following secondary
# licenses when the conditions for such availability set forth in the
# Eclipse Public License v2.0 are satisfied:
#
#    GNU General Public License, Version 2.0, or any later versions of
#    that license
#
# SPDX-License-Identifier: EPL-2.0 OR GPL-2.0-or-later
#
# Contributors:
#     Ron Frederick - initial implementation, API, and documentation

import asyncio, asyncssh, sys

class MySSHTCPSession(asyncssh.SSHTCPSession):
    def connection_made(self, chan: asyncssh.SSHTCPChannel) -> None:
        self._chan = chan

    def data_received(self, data: bytes, datatype: asyncssh.DataType):
        self._chan.write(data)

def connection_requested(orig_host: str,
                         orig_port: int) -> asyncssh.SSHTCPSession:
    print(f'Connection received from {orig_host}, port {orig_port}')
    return MySSHTCPSession()

async def run_client() -> None:
    async with asyncssh.connect('localhost') as conn:
        server = await conn.create_server(connection_requested, '', 8888,
                                          encoding='utf-8')

        if server:
            await server.wait_closed()
        else:
            print('Listener couldn\'t be opened.', file=sys.stderr)

try:
    asyncio.run(run_client())
except (OSError, asyncssh.Error) as exc:
    sys.exit('SSH connection failed: ' + str(exc))
