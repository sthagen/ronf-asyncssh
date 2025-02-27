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
from typing import Optional

class MySSHClientSession(asyncssh.SSHClientSession):
    def data_received(self, data: str, datatype: asyncssh.DataType) -> None:
        print(data, end='')

    def connection_lost(self, exc: Optional[Exception]) -> None:
        if exc:
            print('SSH session error: ' + str(exc), file=sys.stderr)

class MySSHClient(asyncssh.SSHClient):
    def connection_made(self, conn: asyncssh.SSHClientConnection) -> None:
        print(f'Connection made to {conn.get_extra_info('peername')[0]}.')

    def auth_completed(self) -> None:
        print('Authentication successful.')

async def run_client() -> None:
    conn, client = await asyncssh.create_connection(MySSHClient, 'localhost')

    async with conn:
        chan, session = await conn.create_session(MySSHClientSession, 'ls abc')
        await chan.wait_closed()

try:
    asyncio.run(run_client())
except (OSError, asyncssh.Error) as exc:
    sys.exit('SSH connection failed: ' + str(exc))
