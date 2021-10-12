#!/usr/bin/env python3.6
#
# Copyright (c) 2013-2018 by Ron Frederick <ronf@timeheart.net> and others.
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
from functools import partial

def connection_requested(conn, orig_host, orig_port):
    if orig_host in ('127.0.0.1', '::1'):
        return conn.forward_connection('localhost', 80)
    else:
        raise asyncssh.ChannelOpenError(
            asyncssh.OPEN_ADMINISTRATIVELY_PROHIBITED,
            'Connections only allowed from localhost')

async def run_client():
    async with asyncssh.connect('localhost') as conn:
        listener = await conn.create_server(
            partial(connection_requested, conn), '', 8080)
        await listener.wait_closed()

try:
    asyncio.get_event_loop().run_until_complete(run_client())
except (OSError, asyncssh.Error) as exc:
    sys.exit('SSH connection failed: ' + str(exc))
