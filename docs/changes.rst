.. currentmodule:: asyncssh

Change Log
==========

Release 2.7.2 (15 Sep 2021)
---------------------------

* Fixed a regression related to server host key selection when attempting
  to use a leading '+' to add algorithms to the front of the default list.

* Fixed logging to properly handle SFTPName objects with string filenames.

* Fixed SSH_EXT_INFO to only be sent after the first key exchange.


Release 2.7.1 (6 Sep 2021)
--------------------------

* Added an option to allow encrypted keys to be ignored when no passphrase
  is set. This behavior previously happened by default when loading keys
  from default locations, but now this option to load_keypairs() can be
  specified when loading any set of keys.

* Changed loading of default keys to automatically skip key types which
  aren't supported due to missing dependencies.

* Added the ability to specify "default" for server_host_key_algs, as
  a way for a client to request that its full set of default algorithms
  be advertised to the server, rather than just the algorithms matching
  keys in the client's known hosts list. Thanks go to Manfred Kaiser
  for suggesting this improvement.

* Added support for tilde-expansion in the config file "include"
  directive. Thanks go to Zack Cerza for reporting this and suggesting
  a fix.

* Improved interoperatbility of AsyncSSH SOCKS listener by sending a zero
  address rather than an empty hostname in the SOCKS CONNECT response.
  Thanks go to Github user juouy for reporting this and suggesting a fix.

* Fixed a couple of issues related to sending SSH_EXT_INFO messages.

* Fixed an issue with using SSHAcceptor as an async context manager.
  Thanks go to Paulo Costa for reporing this.

* Fixed an issue where a tunnel wasn't always cleaned up properly when
  creating a remote listener.

* Improved handling of connection drops, avoiding exceptions from being
  raised in some cases when the transport is abruptly closed.

* Made AsyncSSH SFTP support more tolerant of file permission values with
  undefined bits set. Thanks go to GitHub user ccwufu for reporting this.

* Added some missing key exchange algorithms in the AsyncSSH documentation.
  Thanks go to Jeremy Norris for noticing and reporting this.

* Added support for running AsyncSSH unit tests on systems with OpenSSL
  3.0 installed. Thanks go to Ken Dreyer for raising this issue and
  pointing out the new OpenSSL "provider" support for legacy algorithms.

Release 2.7.0 (19 Jun 2021)
---------------------------

* Added support for the ProxyCommand config file option and a
  corresponding proxy_command argument in the SSH connection options,
  allowing a subprocess to be used to make the connection to the SSH
  server. When the config option is used, it should be fully compatible
  with OpenSSH percent expansion in the command to run.

* Added support for accessing terminal information as properties in the
  SSHServerProcess class. As part of this change, both the environment
  and terminal modes are now available as read-only mappings. Thanks
  again to velavokr for suggesitng this and submitting a PR with a
  proposed version of the change.

* Fixed terminal information passed to pty_requested() callback to
  properly reflect requested terminal type, size, and modes. Thanks go
  to velavokr for reporting this issue and proposing a fix.

* Fixed an edge case where a connection object might not be cleaned up
  properly if the connection request was cancelled before it was fully
  established.

* Fixed an issue where some unit tests weren't properly closing
  connection objects before exiting.

Release 2.6.0 (1 May 2021)
--------------------------

* Added support for the HostKeyAlias client config option and a
  corresponding host_key_alias option, allowing known_hosts lookups
  and host certificate validation to be done against a different
  hoetname than what is used to make the connection. Thanks go to
  Pritam Baral for contributing this feature!

* Added the capability to specify client channel options as connection
  options, allowing them to be set in a connect() call or as values in
  SSHClientConnectionOptions. These values will act as defaults for
  any sessions opened on the connection but can still be overridden
  via arguments in the create_session() call.

* Added support for dynamically updating SSH options set up in a
  listen() or listen_reverse() call. A new SSHAcceptor class is now
  returned by these calls which has an update() method which takes
  the same keyword arguments as SSHClientConnectionOptions or
  SSHServerConnectionOptions, allowing you to update any of the
  options on an existing listener except those involved in setting
  up the listening sockets themselves. Updates will apply to future
  connections accepted by that listener.

* Added support for a number of algorithms supported by the ssh.com
  Tectia SSH client/server:

    Key exchange:

      | diffie-hellman-group14-sha256\@ssh.com (enabled by default)

      | diffie-hellman-group14-sha224\@ssh.com (available but not default)
      | diffie-hellman-group15-sha256\@ssh.com
      | diffie-hellman-group15-sha384\@ssh.com
      | diffie-hellman-group16-sha384\@ssh.com
      | diffie-hellman-group16-sha512\@ssh.com
      | diffie-hellman-group18-sha512\@ssh.com

    HMAC:

      | hmac-sha256-2\@ssh.com     (all enabled by default)
      | hmac-sha224\@ssh.com
      | hmac-sha256\@ssh.com
      | hmac-sha384\@ssh.com
      | hmac-sha512\@ssh.com

    RSA public key algorithms:

      | ssh-rsa-sha224\@ssh.com    (all enabled by default)
      | ssh-rsa-sha256\@ssh.com
      | ssh-rsa-sha384\@ssh.com
      | ssh-rsa-sha512\@ssh.com

    Encryption:

      | seed-cbc\@ssh.com          (available but not default)

* Added a new 'ignore-failure' value to the x11_forwarding argument in
  create_session(). When specified, AsyncSSH will attempt to set up X11
  forwarding but ignore failures, behaving as if forwarding was never
  requested instead of raising a ConnectionOpenError.

* Extended support for replacing certificates in an SSHKeyPair, allowing
  alternate certificates to be used with SSH agent and PKCS11 keys. This
  provides a way to use X.509 certificates with an SSH agent key or
  OpenSSH certificates with a PKCS11 key.

* Extended the config file parser to support '=' as a delimiter between
  keywords and arguments. While this syntax appears to be rarely used,
  it is supported by OpenSSH.

* Updated Fido2 support to use version 0.9.1 of the fido2 package,
  which included some changes that were not backward compatible with
  0.8.1.

* Fixed problem with setting config options with percent substitutions
  to 'none'. Percent subsitution should not be performed in this case.
  Thanks go to Yuqing Miao for finding and reporting this issue!

* Fixed return type of filenames in SFTPClient scandir() and readlink()
  when the argument passed in is a Path value. Previously, the return
  value in this case was bytes, but that was only meant to apply when the
  input argument was passed as bytes.

* Fixed a race condition related to closing a channel before it is fully
  open, preventing a client from potentially hanging forever if a
  session was closed while the client was still attempting to request a
  PTY or make other requests as part of opening the session.

* Fixed a potential race condition related to making parallel calls to
  SFTPClient makedirs() which try to create the same directory or a
  common parent directory.

* Fixed RFC 4716 parser to allow colons in header values.

* Improved error message when AsyncSSH is unable to get the local
  username on a client. Thanks go to Matthew Plachter for reporting
  this issue.

Release 2.5.0 (23 Dec 2020)
---------------------------

* Added support for limiting which identities in an SSH agent will be
  used when making a connection, via a new "agent_identities" config
  option. This change also adds compatibility with the OpenSSL config
  file option "IdentitiesOnly".

* Added support for including Subject Key Identifier and Authority Key
  Identifier extensions in generated X.509 certificates to better comply
  with RFC 5280.

* Added support for makedirs() and rmtree() methods in the AsyncSSH
  SFTP client, as well as a new scandir() method which returns an async
  iterator to more efficiently process very large directories. Thanks
  go to Joseph Ernest for suggesting these improvements.

* Significantly reworked AsyncSSH line editor support to improve its
  performance by several orders of magnitude on long input lines, and
  added a configurable maximum line length when the editor is in use to
  avoid potential denial-of-service attacks. This limit defaults to
  1024 bytes, but with the improvements it can reasonably handle lines
  which are megabytes in size if needed.

* Changed AsyncSSH to allow SSH agent identities to still be used when
  an explicit list of client keys is specified, for better compatibility
  with OpenSSH. The previous behavior can still be achieved by explicitly
  setting the agent_path option to None when setting client_keys.

* Changed AsyncSSH to enforce a limit of 1024 characters on usernames
  when acting as a server to avoid a potential denial-of-service issue
  related to SASLprep username normalization.

* Changed SCP implementation to explicitly yield to other coroutines
  when sending a large file to better share an event loop.

* Fixed a few potential race conditions related to cleanup of objects
  during connection close. Thanks go to Thomas Léveil for reporting one
  of these places and suggesting a fix.

* Re-applied a previous fix which was unintentionally lost to allow
  Pageant to be used by default on Windows.

Release 2.4.2 (11 Sep 2020)
---------------------------

* Fixed a potential race condition when receiving EOF right after a
  channel is opened. Thanks go to Alex Shafer for reporting this and
  helping to track down the root cause.

* Fixed a couple of issues related to the error_handler and
  progress_handler callbacks in AsyncSSH SFTP/SCP. Thanks go to
  geraldnj for noticing and reporting these.

* Fixed a couple of issues related to using pathlib objects with
  AsyncSSH SCP.

Release 2.4.1 (5 Sep 2020)
--------------------------

* Fixed SCP server to send back an exit status when closing the SSH
  channel, since the OpenSSH scp client returns this status to the
  shell which executed it. Thanks go to girtsf for catching this.

* Fixed listeners created by forward_local_port(), forward_local_path(),
  and forward_socks() to automatically close when the SSH connection
  closes, unblocking any wait_closed() calls which are in progress.
  Thanks go to rmawatson for catching this.

* Fixed a potential exception that could trigger when the SSH
  connection is closed while authentication is in progress.

* Fixed tunnel connect code to properly clean up an implicitly created
  tunnel when a failure occurs in trying to open a connection over
  that tunnel.

Release 2.4.0 (29 Aug 2020)
---------------------------

* Added support for accessing keys through a PKCS#11 provider, allowing
  keys on PIV security tokens to be used directly by AsyncSSH without
  the need to run an SSH agent. X.509 certificates can also be retrieved
  from the security token and used with SSH servers which support that.

* Added support for using Ed25519 and Ed448 keys in X.509 certificates,
  and the corresponding SSH certificate and signature algorithms.
  Certificates can use these keys as either subject keys or signing keys,
  and certificates can be generated by either AsyncSSH or by OpenSSL
  version 1.1.1 or later.

* Added support for feed_data() and feed_eof() methods in SSHReader,
  mirroring methods of the same name in asyncio's StreamReader to
  improve interoperability between the two APIs. Thanks go to Mikhail
  Terekhov for suggesting this and providing an example implementation.

* Updated unit tests to test interoperability with OpenSSL 1.1.1 when
  reading and writing Ed25519 and Ed448 public and private key files.
  Previously, due to lack of support in OpenSSL, AsyncSSH could only
  test against OpenSSH, and only in OpenSSH key formats. With OpenSSL
  1.1.1, testing is now also done using PKCS#8 format.

* Fixed config file parser to properly ignore all comment lines, even
  if the lines contain unbalanced quotes.

* Removed a note about the lack of a timeout parameter in the AsyncSSH
  connect() method, now that it supports a login_timeout argument.
  Thanks go to Tomasz Drożdż for catching this.

Release 2.3.0 (12 Jul 2020)
---------------------------

* Added initial support for reading configuration from OpenSSH-compatible
  config files, when present. Both client and server configuration files
  are supported, but not all config options are supported. See the
  AsyncSSH documentation for the latest list of what client and server
  options are supported, as well as what match conditions and percent
  substitutions are understood.

* Added support for the concept of only a subset of supported algorithms
  being enabled by default, and for the ability to use wildcards when
  specifying algorithm names. Also, OpenSSH's syntax of prefixing the
  list with '^', '+', or '-' is supported for incrementally adjusting
  the list of algorithms starting from the default set.

* Added support for specifying a preferred list of client authentication
  methods, in order of preference. Previously, the order of preference
  was hard-coded into AsyncSSH.

* Added the ability to use AsyncSSH's "password" argument on servers
  which are using keyboard-interactive authentication to prompt for a
  "passcode". Previously, this was only supported when the prompt was
  for a "password".

* Added support for providing separate lists of private keys and
  certificates, rather than requiring them to be specifying together as
  a tuple. When this new option is used, AsyncSSH will automatically
  associate the private keys with their corresponding certificates if
  matching certificates are present in the list.

* Added support for the "known_hosts" argument to accept a list of known
  host files, rather than just a single file. Known hosts can also be
  specified using the GlobalKnownHostFile and UserKnownHostFile config
  file options, each of which can take multiple filenames.

* Added new "request_tty" option to provide finer grained control over
  whether AsyncSSH will request a TTY when opening new sessions. The
  default is to still tie this to whether a "term_type" is specified,
  but now that can be overridden. Supported options of "yes", "no",
  "force", and "auto" match the values supported by OpenSSH.

* Added new "rdns_lookup" option to control whether the server does a
  reverse DNS of client addresses to allow matching of clients based
  on hostname in authorized keys and config files. When this option
  is disabled (the default), matches can only be based on client IP.

* Added new "send_env" argument when opening a session to forward local
  environment variables using their existing values, augmenting the
  "env" argument that lets you specify remote environment variables to
  set and their corresponding values.

* Added new "tcp_keepalive" option to control whether TCP-level
  keepalives are enabled or not on SSH connections. Previously, TCP
  keepalives were enabled unconditionally and this is still the default,
  but the new option provides a way to disable them.

* Added support for sending and parsing client EXT_INFO messages, and
  for sending the "global-requests-ok" option in these messages when
  AsyncSSH is acting as a client.

* Added support for expansion of '~' home directory expansion when
  specifying arguments which contain filenames.

* Added support for time intervals and byte counts to optionally be
  specified as string values with units, allowing for values such as
  "1.5h" or "1h30m" instead of having to specify that as 5400 seconds.
  Similarly, a byte count of "1g" can be passed to indicate 1 gigabyte,
  rather than specifying 1073741824 bytes.

* Enhanced logging to report lists of sent and received algorithms when
  no matching algorithm is found. Thanks go to Jeremy Schulman for
  suggesting this.

* Fixed an interoperability issue with PKIXSSH when attempting to use
  X.509 certificates with a signature algorithm of "x509v3-rsa2048-sha256".

* Fixed an issue with some links not working in the ReadTheDocs sidebar.
  Thanks go to Christoph Giese for reporting this issue.

* Fixed keepalive handler to avoid leaking a timer object in some cases.
  Thanks go to Tom van Neerijnen for reporting this issue.

Release 2.2.1 (18 Apr 2020)
---------------------------

* Added optional timeout parameter to SSHClientProcess.wait() and
  SSHClientConnection.run() methods.

* Created subclasses for SFTPError exceptions, allowing applications
  to more easily have distinct exception handling for different errors.

* Fixed an issue in SFTP parallel I/O related to handling low-level
  connection failures. Thanks go to Mikhail Terekhov for reporting
  this issue.

* Fixed an issue with SFTP file copy where a local file could sometimes
  be left open if an attempt to close a remote file failed.

* Fixed an issue in the handling of boolean return values when
  SSHServer.server_requested() returns a coroutine. Thanks go to
  Tom van Neerijnen for contributing this fix.

* Fixed an issue with passing tuples to the SFTP copy functions. Thanks
  go to Marc Gagné for reporting this and doing the initial analysis.

Release 2.2.0 (29 Feb 2020)
---------------------------

* Added support for U2F/FIDO2 security keys, with the following capabilities:

  * ECDSA (NISTP256) and Ed25519 key algorithms
  * Key generation, including control over the application and user the
    key is associated with and whether touch is required when using the key
  * Certificate generation, both as a key being signed and a CA key
  * Resident keys, allowing security keys to be used on multiple machines
    without any information being stored outside of the key
  * Access to and management of keys loaded in an OpenSSH ssh-agent
  * Support for both user and host keys and certificates
  * Support for "no-touch-required" option in authorized_keys files
  * Support for "no-touch-required" option in OpenSSH certificates
  * Compatibility with security key support added in OpenSSH version 8.2

* Added login timeout client option and limits on the length and number
  of banner lines AsyncSSH will accept prior to the SSH version header.

* Improved load_keypairs() to read public key files, confirming that they
  are consistent with their associated private key when they are present.

* Fixed issues in the SCP server related to handling filenames with spaces.

* Fixed an issue with resuming reading after readuntil() returns an
  incomplete read.

* Fixed a potential issue related to asyncio not reporting sockname/peername
  when a connection is closed immediately after it is opened.

* Made SSHConnection a subclass of asyncio.Protocol to please type checkers.

Release 2.1.0 (30 Nov 2019)
---------------------------

* Added support in the SSHProcess redirect mechanism to accept asyncio
  StreamReader and StreamWriter objects, allowing asyncio streams to
  be plugged in as stdin/stdout/stderr in an SSHProcess.

* Added support for key handlers in the AsyncSSH line editor to trigger
  signals being delivered when certain "hot keys" are hit while reading
  input.

* Improved cleanup of unreturned connection objects when an error occurs
  or the connection request is canceled or times out.

* Improved cleanup of SSH agent client objects to avoid triggering a false
  positive warning in Python 3.8.

* Added an example to the documentation for how to create reverse-direction
  SSH client and server connections.

* Made check of session objects against None explicit to avoid confusion
  on user-defined sessions that implement __len__ or __bool__. Thanks go
  to Lars-Dominik Braun for contributing this improvement!

Release 2.0.1 (2 Nov 2019)
--------------------------

* Some API changes which should have been included in the 2.0.0 release
  were missed. This release corrects that, but means that additional
  changes may be needed in applications moving to 2.0.1. This should
  hopefully be the last of such changes, but if any other issues are
  discovered, additional changes will be limited to 2.0.x patch releases
  and the API will stabilize again in the AsyncSSH 2.1 release. See the
  next bullet for details about the additional incompatible change.

* To be consistent with other connect and listen functions, all methods
  on SSHClientConnection which previously returned None on listen
  failures have been changed to raise an exception instead. A new
  ChannelListenError exception will now be raised when an SSH server
  returns failure on a request to open a remote listener. This change
  affects the following SSHClientConnection methods: create_server,
  create_unix_server, start_server, start_unix_server,
  forward_remote_port, and forward_remote_path.

* Restored the ability for SSHListener objects to be used as async
  context managers. This previously worked in AsyncSSH 1.x and was
  unintentionally broken in AsyncSSH 2.0.0.

* Added support for a number of additional functions to be called from
  within an "async with" statement. These functions already returned
  objects capable of being async context managers, but were not decorated
  to allow them to be directly called from within "async with". This
  change applies to the top level functions create_server, listen, and
  listen_reverse and the SSHClientConnection methods create_server,
  create_unix_server, start_server, start_unix_server, forward_local_port,
  forward_local_path, forward_remote_port, forward_remote_path,
  listen_ssh, and listen_reverse_ssh,

* Fixed a couple of issues in loading OpenSSH-format certificates which
  were missing a trailing newline.

* Changed load_certificates() to allow multiple certificates to be loaded
  from a single byte string argument, making it more consistent with
  how load_certificates() works when reading from a file.

Release 2.0.0 (26 Oct 2019)
---------------------------

* NEW MAJOR VERSION: See below for potentially incompatible changes.

* Updated AsyncSSH to use the modern async/await syntax internally,
  now requiring Python 3.6 or later. Those wishing to use AsyncSSH on
  Python 3.4 or 3.5 should stick to the AsyncSSH 1.x releases.

* Changed first argument of SFTPServer constructor from an
  SSHServerConnection (conn) to an SSHServerChannel (chan) to allow
  custom SFTP server implementations to access environment variables
  set on the channel that SFTP is run over. Applications which subclass
  the SFTPServer class and implement an __init__ method will need to be
  updated to account for this change and pass the new argument through
  to the SFTPServer parent class. If the subclass has no __init__ and
  just uses the connection, channel, and env properties of SFTPServer
  to access this information, no changes should be required.

* Removed deprecated "session_encoding" and "session_errors" arguments
  from create_server() and listen() functions. These arguments were
  renamed to "encoding" and "errors" back in version 1.16.0 to be
  consistent with other AsyncSSH APIs.

* Removed get_environment(), get_command(), and get_subsystem() methods
  on SSHServerProcess class. This information was made available as
  "env", "command", and "subsystem" properties of SSHServerProcess in
  AsyncSSH 1.11.0.

* Removed optional loop argument from all public AsyncSSH APIs,
  consistent with the deprecation of this argument in the asyncio
  package in Python 3.8. Calls will now always use the event loop
  which is active at the time of the call.

* Removed support for non-async context managers on AsyncSSH connections
  and processes and SFTP client connections and file objects. Callers
  should use "async with" to invoke the async the context managers on
  these objects.

* Added support for SSHAgentClient being an async context manager. To
  be consistent with other connect calls, connect_agent() will now
  raise an exception when no agent is found or a connection failure
  occurs, rather than logging a warning and returning None. Callers
  should catch OSError or ChannelOpenError exceptions rather than
  looking for a return value of None when calling this function.

* Added set_input() and clear_input() methods on SSHLineEditorChannel
  to change the value of the current input line when line editing is
  enabled.

* Added is_closing() method to the SSHChannel, SSHProcess, SSHWriter,
  and SSHSubprocessTransport classes. mirroring the asyncio
  BaseTransport and StreamWriter methods added in Python 3.7.

* Added wait_closed() async method to the SSHWriter class, mirroring
  the asyncio StreamWriter method added in Python 3.7.

Release 1.18.0 (23 Aug 2019)
----------------------------

* Added support for GSSAPI ECDH and Edwards DH key exchange algorithms.

* Fixed gssapi-with-mic authentication to work with GSS key exchanges,
  in cases where gssapi-keyex is not supported.

* Made connect_ssh and connect_reverse_ssh methods into async context
  managers, simplifying the syntax needed to use them to create tunneled
  SSH connections.

* Fixed a couple of issues with known hosts matching on tunneled SSH
  connections.

* Improved flexibility of key/certificate parser automatic format
  detection to properly recognize PEM even when other arbitrary text
  is present at the beginning of the file. With this change, the
  parser can also now handle mixing of multiple key formats in a
  single file.

* Added support for OpenSSL "TRUSTED" PEM certificates. For now, no
  enforcement is done of the additional trust restrictions, but such
  certificates can be loaded and used by AsyncSSH without converting
  them back to regular PEM format.

* Fixed some additional SFTP and SCP issues related to parsing of
  Windows paths with drive letters and paths with multiple colons.

* Made AsyncSSH tolerant of a client which sends multiple service
  requests for the "ssh-userauth" service. This is needed by the
  Paramiko client when it tries more than one form of authentication
  on a connection.

Release 1.17.1 (23 Jul 2019)
----------------------------

* Improved construction of file paths in SFTP to better handle native
  Windows source paths containing backslashes or drive letters.

* Improved SFTP parallel I/O for large reads and file copies to better
  handle the case where a read returns less data than what was requested
  when not at the end of the file, allowing AsyncSSH to get back the
  right result even if the requested block size is larger than the
  SFTP server can handle.

* Fixed an issue where the requested SFTP block_size wasn't used in the
  get, copy, mget, and mcopy functions if it was larger than the
  default size of 16 KB.

* Fixed a problem where the list of client keys provided in an
  SSHClientConnectionOptions object wasn't always preserved properly
  across the opening of multiple SSH connections.

* Changed SSH agent client code to avoid printing a warning on Windows
  when unable to connect to the SSH agent using the default path. A
  warning will be printed if the agent_path or SSH_AUTH_SOCK is
  explicitly set, but AsyncSSH will remain quiet if no agent path is
  set and no SSH agent is running.

* Made AsyncSSH tolerant of unexpected authentication success/failure
  messages sent after authentication completes. AsyncSSH previously
  treated this as a protocol error and dropped the connection, while
  most other SSH implementations ignored these messages and allowed
  the connection to continue.

* Made AsyncSSH tolerant of SFTP status responses which are missing
  error message and language tag fields, improving interoperability
  with servers that omit these fields. When missing, AsyncSSH treats
  these fields as if they were set to empty strings.

Release 1.17.0 (31 May 2019)
----------------------------

* Added support for "reverse direction" SSH connections, useful to
  support applications like NETCONF Call Home, described in RFC 8071.

* Added support for the PyCA implementation of Chacha20-Poly1305,
  eliminating the dependency on libnacl/libsodium to provide this
  functionality, as long as OpenSSL 1.1.1b or later is installed.

* Restored libnacl support for Curve25519/Ed25519 on systems which
  have an older version of OpenSSL that doesn't have that support.
  This fallback also applies to Chacha20-Poly1305.

* Fixed Pageant support on Windows to use the Pageant agent by default
  when it is available and client keys are not explicitly configured.

* Disabled the use of RSA SHA-2 signatures when using the Pageant
  or Windows 10 OpenSSH agent on Windows, since neither of those
  support the signature flags options to request them.

* Fixed a regression where a callable was no longer usable in the
  sftp_factory argument of create_server.

Release 1.16.1 (30 Mar 2019)
----------------------------

* Added channel, connection, and env properties to SFTPServer instances,
  so connection and channel information can be used to influence the
  SFTP server's behavior. Previously, connection information was made
  avaiable through the constructor, but channel and environment
  information was not. Now, all of these are available as properties
  on the SFTPServer instance without the need to explicitly store anything
  in a custom constructor.

* Optimized SFTP glob matching when the glob pattern contains directory
  names without glob characters in them. Thanks go to Mikhail Terekhov
  for contributing this improvement!

* Added support for PurePath in a few places that were missed when this
  support was originally added. Once again, thanks go to Mikhail Terehkov
  for these fixes.

* Fixed bug in SFTP parallel I/O file reader where it sometimes returned
  EOF prematurely. Thanks go to David G for reporting this problem and
  providing a reproducible test case.

* Fixed test failures seen on Fedora Rawhide. Thanks go to Georg Sauthof
  for reporting this issue and providing a test environment to help debug
  it.

* Updated Ed25519/448 and Curve25519/448 tests to only run when these
  algorithms are available. Thanks go to Ondřej Súkup for reporting
  this issue and providing a suggested fix.

Release 1.16.0 (2 Mar 2019)
---------------------------

* Added support for Ed448 host/client keys and certificates and
  rewrote Ed25519 support to use the PyCA implementation, reducing
  the dependency on libnacl and libsodium to only be needed to
  support the chacha20-poly1305 cipher.

* Added support for PKCS#8 format Ed25519 and Ed448 private and
  public keys (in addition to the OpenSSH format previously
  supported).

* Added support for multiple delimiters in SSHReader's readuntil()
  function, causing it to return data as soon as any of the
  specified delimiters are matched.

* Added the ability to register custom key handlers in the line
  editor which can modify the input line, extending the built-in
  editing functionality.

* Added SSHSubprocessProtocol and SSHSubprocessTransport classes
  to provide compatibility with asyncio.SubprocessProtocol and
  asyncio.SubprocessTransport. Code which is designed to call
  BaseEventLoop.subprocess_shell() or BaseEventLoop.subprocess_exec()
  can be easily adapted to work against a remote process by calling
  SSHClientConnection.create_subprocess().

* Added support for sending keepalive messages when the SSH
  connection is idle, with an option to automatically disconnect
  the connection if the remote system doesn't respond to these
  keepalives.

* Changed AsyncSSH to ignore errors when loading unsupported key
  types from the default file locations.

* Changed the reuse_port option to only be available on Python
  releases which support it (3.4.4 and later).

* Fixed an issue where MSG_IGNORE packets could sometimes be sent
  between MSG_NEWKEYS and MSG_EXT_INFO, which caused some SSH
  implementations to fail to properly parse the MSG_EXT_INFO.

* Fixed a couple of errors in the handling of disconnects occurring
  prior to authentication completing.

* Renamed "session_encoding" and "session_errors" arguments in
  asyncssh.create_server() to "encoding" and "errors", to match
  the names used for these arguments in other AsyncSSH APIs. The
  old names are still supported for now, but they are marked as
  deprecated and will be removed in a future release.

Release 1.15.1 (21 Jan 2019)
----------------------------

* Added callback-based host validation in SSHClient, allowing callers
  to decide programmatically whether to trust server host keys and
  certificates rather than having to provide a list of trusted values
  in advance.

* Changed SSH client code to only load the default known hosts file if
  if exists. Previously an error was returned if a known_hosts value
  wasn't specified and the default known_hosts file didn't exist. For
  host validate to work in this case, verification callbacks must be
  implemented or other forms of validation such as X.509 trusted CAs
  or GSS-based key exchange must be used.

* Fixed known hosts validation to completely disable certificate checks
  when known_hosts is set to None. Previously, key checking was disabled
  in this case but other checks for certificate expiration and hostname
  mismatch were still performed, causing connections to fail even when
  checking was supposed to be disabled.

* Switched curve25519 key exchange to use the PyCA implementation,
  avoiding a dependency on libnacl/libsodium. For now, support for
  Ed25519 keys still requires these libraries.

* Added get_fingerprint() method to return a fingerprint of an SSHKey.


Release 1.15.0 (26 Nov 2018)
----------------------------

* Added the ability to pass keyword arguments provided in the scp()
  command through to asyncssh.connect() calls it makes, allowing
  things like custom credentials to be specified.

* Added support for a reuse_port argument in create_server(). If
  set, this will be passed to the asyncio loop.create_server() call
  which creates listening sockets.

* Added support for "soft" EOF when line editing in enabled so that
  EOF can be signalled multiple times on a channel. When Ctrl-D is
  received on a channel with line editing enabled, EOF is returned
  to the application but the channel remains open and capable of
  accepting more input, allowing an interactive shell to process
  the EOF for one command but still accept input for subsequent
  commands.

* Added support for the Windows 10 OpenSSH ssh-agent. Thanks go to
  SamP20 for providing an initial proof of concept and a suggested
  implementation.

* Reworked scoped link-local IPv6 address normalization to work
  better on Linux systems.

* Fixed a problem preserving directory structure in recursive scp().

* Fixed SFTP chmod tests to avoid attempting to set the sticky bit on
  a plain file, as this caused test failures on FreeBSD.

* Updated note in SSHClientChannel's send_signal() documentation to
  reflect that OpenSSH 7.9 and later should now support processing
  of signal messages.

Release 1.14.0 (8 Sep 2018)
---------------------------

* Changed license from EPL 1.0 to EPL 2.0 with GPL 2.0 or later as an
  available secondary license.

* Added support for automatically parallelizing large reads and write
  made using the SFTPClientFile class, similar to what was already
  available in the get/put/copy methods of SFTPClient.

* Added support for get_extra_info() in SSH process classes, returning
  information associated with the channel the process is tied to.

* Added new set_extra_info() method on SSH connection and channel
  classes, allowing applications to store additional information on
  these objects.

* Added handlers for OpenSSH keepalive global & channel requests to
  avoid messages about unknown requests in the debug log. These requests
  are still logged, but at debug level 2 instead of 1 and they are not
  labeled as unknown.

* Fixed race condition when closing sockets associated with forwarded
  connections.

* Improved error handling during connection close in SFTPClient.

* Worked around issues with integer overflow on systems with a
  32-bit time_t value when dates beyond 2038 are used in X.509
  certificates.

* Added guards around some imports and tests which were causing
  problems on Fedora 27.

* Changed debug level for reporting PTY modes from 1 to 2 to reduce
  noise in the logs.

* Improved SFTP debug log output when sending EOF responses.

Release 1.13.3 (23 Jul 2018)
----------------------------

* Added support for setting the Unicode error handling strategy in
  conjunction with setting an encoding when creating new SSH sessions,
  streams, and processes. This strategy can also be set when specifying
  a session encoding in create_server(), and when providing an encoding
  in the get_comment() and set_comment() functions on private/public
  keys and certificates.

* Changed handling of Unicode in channels to use incrmeental codec,
  similar to what was previously done in process redirection.

* Added Python 3.7 to the list of classifiers in setup.py, now that it
  has been released.

* Updated Travis CI configuration to add Python 3.7 builds, and moved
  Linux builds on never versions of Python up to xenial.

* Added missing coroutine decorator in test_channel.

Release 1.13.2 (3 Jul 2018)
---------------------------

* Added support for accessing client host keys via the OpenSSH
  ssh-keysign program when doing host-based authentication. If
  ssh-keysign is present and enabled on the system, an AsyncSSH
  based SSH client can use host-based authentication without
  access to the host private keys.

* Added support for using pathlib path objects when reading and
  writing private and public keys and certificates.

* Added support for auth_completed() callback in the SSHServer
  class which runs when authentication completes successfully
  on each new connection.

* Fixed host-based authentication unit tests to mock out calls
  to getnameinfo() to avoid failures on systems with restricted
  network functionality.

Release 1.13.1 (16 Jun 2018)
----------------------------

* Added client and server support for host-based SSH authentication.
  If enabled, this will allow all users from a given host to be
  authenticated by a shared host key, rather than each user needing
  their own key. This should only be used with hosts which are trusted
  to keep their host keys secure and provide accurate client usernames.

* Added support for RSA key exchange algorithms (rsa2048-sha256 and
  rsa1024-sha1) available in PuTTY and some mobile SSH clients.

* Added support for the SECP256K1 elliptic curve for ECDSA keys and
  ECDH key exchange. This curve is supported by the Bitvise SSH client
  and server.

* Added debug logging of the algorithms listed in a received kexinit
  message.

Release 1.13.0 (20 May 2018)
----------------------------

* Added support for dynamic port forwarding via SOCKS, where AsyncSSH
  will open a listener which understands SOCKS connect requests and
  for each request open a TCP/IP tunnel over SSH to the requested host
  and port.

* Added support in SSHProcess for I/O redirection to file objects that
  implement read(), write(), and close() functions as coroutines, such
  as the "aiofiles" package. In such cases, AsyncSSH will automaically
  detect that it needs to make async calls to these methods when it
  performs I/O.

* Added support for using pathlib objects in SSHProcess I/O redirection.

* Added multiple improvements to pattern matching support in the SFTPClient
  glob(), mget(), mput(), and mcopy() methods. AsyncSSH now allows you
  to use '**' in a pattern to do a recursive directory search, allows
  character ranges in square brackets in a pattern, and allows a trailing
  slash in a pattern to be specified to request that only directories
  matching the pattern should be returned.

* Fixed an issue with calling readline() and readuntil() with a timeout,
  where partial data received before the timeout was sometimes discarded.
  Any partial data which was received when a timeout occurs will now be
  left in the input buffer, so it is still available to future read()
  calls.

* Fixed a race condition where trying to restart a read() after a timeout
  could sometimes raise an exception about multiple simultaneous reads.

* Changed readuntil() in SSHReader to raise IncompleteReadError if the
  receive window fills up before a delimiter match is found. This also
  applies to readline(), which will return a partial line without a
  newline at the end when this occurs. To support longer lines, a caller
  can call readuntil() or readline() as many times as they'd like,
  appending the data returned to the previous partial data until a
  delimiter is found or some maximum size is exceeded. Since the default
  window size is 2 MBytes, though, it's very unlikely this will be needed
  in most applications.

* Reworked the crypto support in AsyncSSH to separate packet encryption
  and decryption into its own module and simplified the directory
  structure of the asyncssh.crypto package, eliminating a pyca subdirectory
  that was created back when AsyncSSH used a mix of PyCA and PyCrypto.


Release 1.12.2 (17 Apr 2018)
----------------------------

* Added support for using pathlib objects as paths in calls to SFTP
  methods, in addition to Unicode and byte strings. This is mainly
  intended for use in constructing local paths, but it can also be
  used for remote paths as long as POSIX-style pathlib objects are
  used and an appropriate path encoding is set to handle the
  conversion from Unicode to bytes.

* Changed server EXT_INFO message to only be sent after the first SSH key
  exchange, to match the specification recently published in RFC 8308.

* Fixed edge case in TCP connection forwarding where data received
  on a forward TCP connection was not delivered if the connection was
  closed or half-closed before the corresponding SSH tunnel was fully
  established.

* Made note about OpenSSH not properly handling send_signal more visible.

Release 1.12.1 (10 Mar 2018)
----------------------------

* Implemented a fix for CVE-2018-7749, where a modified SSH client could
  request that an AsyncSSH server perform operations before authentication
  had completed. Thanks go to Matthijs Kooijman for discovering and
  reporting this issue and helping to review the fix.

* Added a non-blocking collect_output() method to SSHClientProcess to
  allow applications to retrieve data received on an output stream
  without blocking. This call can be called multiple times and freely
  intermixed with regular read calls with a guarantee that output will
  always be returned in order and without duplication.

* Updated debug logging implementation to make it more maintainable, and
  to fix an issue where unprocessed packets were not logged in some cases.

* Extended the support below for non-ASCII characters in comments to apply
  to X.509 certificates, allowing an optional encoding to be passed in to
  get_comment() and set_comment() and a get_comment_bytes() function to
  get the raw comment bytes without performing Unicode decoding.

* Fixed an issue where a UnicodeDecodeError could be reported in some
  cases instead of a KeyEncryptionError when a private key was imported
  using the wrong passphrase.

* Fixed the reporting of the MAC algorithm selected during key exchange to
  properly report the cipher name for GCM and Chacha ciphers that don't
  use a separate MAC algorithm. The correct value was being returned in
  queries after the key exchange was complete, but the logging was being
  done before this adjustment was made.

* Fixed the documentation of connection_made() in SSHSession subclasses
  to properly reflect the type of SSHChannel objects passed to them.

Release 1.12.0 (5 Feb 2018)
---------------------------

* Enhanced AsyncSSH logging framework to provide detailed logging of
  events in the connection, channel, key exchange, authentication,
  sftp, and scp modules. Both high-level information logs and more
  detailed debug logs are available, and debug logging supports
  multiple debug levels with different amounts of verboseness.
  Logger objects are also available on various AsyncSSH classes to
  allow applications to report their own log events in a manner that
  can be tied back to a specific SSH connection or channel.

* Added support for begin_auth() to be a coroutine, so asynchronous
  operations can be performed within it to load state needed to
  perform SSH authentication.

* Adjusted key usage flags set on generated X.509 certificates to be more
  RFC compliant and work around an issue with OpenSSL validation of
  self-signed non-CA certificates.

* Updated key and certificate comment handling to be less sensitive to
  the encoding of non-ASCII characters. The get_comment() and set_comment()
  functions now take an optional encoding paramter, defaulting to UTF-8
  but allowing for others encodings. There's also a get_comment_bytes()
  function to get the comment data as bytes without performing Unicode
  decoding.

* Updated AsyncSSH to be compatible with beta release of Python 3.7.

* Updated code to address warnings reported by the latest version of pylint.

* Cleaned up various formatting issues in Sphinx documentation.

* Significantly reduced time it takes to run unit tests by decreasing
  the rounds of bcrypt encryption used when unit testing encrypted
  OpenSSH private keys.

* Added support for testing against uvloop in Travis CI.

Release 1.11.1 (15 Nov 2017)
----------------------------

* Switched to using PBKDF2 implementation provided by PyCA, replacing a
  much slower pure-Python implementation used in earlier releases.

* Improved support for file-like objects in process I/O redirection,
  properly handling objects which don't support fileno() and allowing
  both text and binary file objects based on whether they have an
  'encoding' member.

* Changed PEM parser to be forgiving of trailing blank lines.

* Updated documentation to note lack of support in OpenSSH for send_signal(),
  terminate(), and kill() channel requests.

* Updated unit tests to work better with OpenSSH 7.6.

* Updated Travis CI config to test with more recent Python versions.

Release 1.11.0 (9 Sep 2017)
---------------------------

* Added support for X.509 certificate based client and server authentication,
  as defined in RFC 6187.

  * DSA, RSA, and ECDSA keys are supported.
  * New methods are available on SSHKey private keys to generate X.509
    user, host, and CA certificates.
  * Authorized key and known host support has been enhanced to support
    matching on X.509 certificates and X.509 subject names.
  * New arguments have been added to create_connection() and create_server()
    to specify X.509 trusted root CAs, X.509 trusted root CA hash directories,
    and allowed X.509 certificate purposes.
  * A new load_certificates() function has been added to more easily pre-load
    a list of certificates from byte strings or files.
  * Support for including and validating OCSP responses is not yet available,
    but may be added in a future release.
  * This support adds a new optional dependency on pyOpenSSL in setup.py.

* Added command, subsystem, and environment properties to SSHProcess,
  SSHCompletedProcess, and ProcessError classes, as well as stdout and
  stderr properties in ProcessError which mirror what is already present
  in SSHCompletedProcess. Thanks go to iforapsy for suggesting this.

* Worked around a datetime.max bug on Windows.

* Increased the build timeout on TravisCI to avoid build failures.

Release 1.10.1 (19 May 2017)
----------------------------

* Fixed SCP to properly call exit() on SFTPServer when the copy completes.
  Thanks go to Arthur Darcet for discovering this and providing a
  suggested fix.

* Added support for passphrase to be specified when loading default client
  keys, and to ignore encrypted default keys if no passphrase is specified.

* Added additional known hosts test cases. Thanks go to Rafael Viotti
  for providing these.

* Increased the default number of rounds for OpenSSH-compatible bcrypt
  private key encryption to avoid a warning in the latest version of the
  bcrypt module, and added a note that the encryption strength scale
  linearly with the rounds value, not logarithmically.

* Fixed SCP unit test errors on Windows.

* Fixed some issues with Travis and Appveyor CI builds.

Release 1.10.0 (5 May 2017)
---------------------------

* Added SCP client and server support, The new asyncssh.scp() function
  can get and put files on a remote SCP server and copy files between
  two or more remote SCP servers, with options similar to what was
  previously supported for SFTP. On the server side, an SFTPServer used
  to serve files over SFTP can also serve files over SCP by simply
  setting allow_scp to True in the call to create_server().

* Added a new SSHServerProcess class which supports I/O redirection on
  inbound connections to an SSH server, mirroring the SSHClientProcess
  class added previously for outbound SSH client connections.

* Enabled TCP keepalive on SSH client and server connections.

* Enabled Python 3 highlighting in Sphinx documentation.

* Fixed a bug where a previously loaded SSHKnownHosts object wasn't
  properly accepted as a known_hosts value in create_connection() and
  enhanced known_hosts to accept a callable to allow applications to
  provide their own function to return trusted host keys.

* Fixed a bug where an exception was raised if the connection closed
  while waiting for an asynchronous authentication callback to complete.

* Fixed a bug where empty passwords weren't being properly supported.

Release 1.9.0 (18 Feb 2017)
---------------------------

* Added support for GSSAPI key exchange and authentication when the
  "gssapi" module is installed on UNIX or the "sspi" module from pypiwin32
  is installed on Windows.

* Added support for additional Diffie Hellman groups, and added the ability
  for Diffie Hellman and GSS group exchange to select larger group sizes.

* Added overridable methods format_user() and format_group() to format user
  and group names in the SFTP server, defaulting to the previous behavior of
  using pwd.getpwuid() and grp.getgrgid() on platforms that support those.

* Added an optional progress reporting callback on SFTP file transfers,
  and made the block size for these transfers configurable.

* Added append_private_key(), append_public_key(), and append_certificate()
  methods on the corresponding key and certificate classes to simplify
  the creating of files containing a list of keys/certificates.

* Updated readdir to break responses into chunks to avoid hitting maximum
  message size limits on large directories.

* Updated SFTP to work better on Windows, properly handling drive letters
  and conversion between forward and back slashes in paths and handling
  setting of attributes on open files and proper support for POSIX rename.
  Also, file closes now block until the close completes, to avoid issues
  with file locking.

* Updated the unit tests to run on Windows, and enabled continuous
  integration builds for Windows to automatically run on Appveyor.

Release 1.8.1 (29 Dec 2016)
---------------------------

* Fix an issue in attempting to load the 'nettle' library on Windows.

Release 1.8.0 (29 Dec 2016)
---------------------------

* Added support for forwarding X11 connections. When requested, AsyncSSH
  clients will allow remote X11 applications to tunnel data back to a local
  X server and AsyncSSH servers can request an X11 DISPLAY value to export
  to X11 applications they launch which will tunnel data back to an X
  server associated with the client.

* Improved ssh-agent forwarding support on UNIX to allow AsyncSSH
  servers to request an SSH_AUTH_SOCK value to export to applications
  they launch in order to access the client's ssh-agent. Previously,
  there was support for agent forwarding on server connections within
  AsyncSSH itself, but they did not provide this forwarding to other
  applications.

* Added support for PuTTY's Pageant agent on Windows systems, providing
  functionality similar to the OpenSSH agent on UNIX. AsyncSSH client
  connections from Windows can now access keys stored in the Pageant
  agent when they perform public key authentication.

* Added support for the umac-64 and umac-128 MAC algorithms, compatible
  with the implementation in OpenSSH. These algorithms are preferred
  over the HMAC algorithms when both are available and the cipher chosen
  doesn't already include a MAC.

* Added curve25519-sha256 as a supported key exchange algorithm. This
  algorithm is identical to the previously supported algorithm named
  'curve25519-sha256\@libssh.org', matching what was done in OpenSSH 7.3.
  Either name may now be used to request this type of key exchange.

* Changed the default order of key exchange algorithms to prefer the
  curve25519-sha256 algorithm over the ecdh-sha2-nistp algorithms.

* Added support for a readuntil() function in SSHReader, modeled after
  the readuntil() function in asyncio.StreamReader added in Python 3.5.2.
  Thanks go to wwjiang for suggesting this and providing an example
  implementation.

* Fixed issues where the explicitly provided event loop value was not
  being passed through to all of the places which needed it. Thanks go
  to Vladimir Rutsky for pointing out this problem and providing some
  initial fixes.

* Improved error handling when port forwarding is requested for a port
  number outside of the range 0-65535.

* Disabled use of IPv6 in unit tests when opening local loopback sockets
  to avoid issues with incomplete IPv6 support in TravisCI.

* Changed the unit tests to always start with a known set of environment
  variables rather than inheriting the environment from the shell
  running the tests. This was leading to test breakage in some cases.

Release 1.7.3 (22 Nov 2016)
---------------------------

* Updated unit tests to run properly in environments where OpenSSH
  and OpenSSL are not installed.

* Updated a process unit test to not depend on the system's default
  file encoding being UTF-8.

* Updated Mac TravisCI builds to use Xcode 8.1.

* Cleaned up some wording in the documentation.

Release 1.7.2 (28 Oct 2016)
---------------------------

* Fixed an issue with preserving file access times in SFTP, and update
  the unit tests to more accurate detect this kind of failure.

* Fixed some markup errors in the documentation.

* Fixed a small error in the change log for release 1.7.0 regarding
  the newly added Diffie Hellman key exchange algorithms.

Release 1.7.1 (7 Oct 2016)
--------------------------

* Fix an error that prevented the docs from building.


Release 1.7.0 (7 Oct 2016)
--------------------------

* Added support for group 14, 16, and 18 Diffie Hellman key exchange
  algorithms which use SHA-256 and SHA-512.

* Added support for using SHA-256 and SHA-512 based signature algorithms
  for RSA keys and support for OpenSSH extension negotiation to advertise
  these signature algorithms.

* Added new load_keypairs and load_public_keys API functions which
  support expicitly loading keys using the same syntax that was
  previously available for specifying client_keys, authorized_client_keys,
  and server_host_keys arguments when creating SSH clients and servers.

* Enhanced the SSH agent client to support adding and removing keys
  and certificates (including support for constraints) and locking and
  unlocking the agent. Support has also been added for adding and
  removing smart card keys in the agent.

* Added support for getting and setting a comment value when generating
  keys and certificates, and decoding and encoding this comment when
  importing and exporting keys that support it. Currently, this is
  available for OpenSSH format private keys and OpenSSH and RFC 4716
  format public keys. These comment values are also passed on to the
  SSH agent when keys are added to it.

* Fixed a bug in the generation of ECDSA certificates that showed up
  when trying to use the nistp384 or nistp521 curves.

* Updated unit tests to use the new key and certificate generation
  functions, eliminating the dependency on the ssh-keygen program.

* Updated unit tests to use the new SSH agent support when adding keys
  to the SSH agent, eliminating the dependency on the ssh-add program.

* Incorporated a fix from Vincent Bernat for an issue with launching
  ssh-agent on some systems during unit testing.

* Fixed some typos in the documentation found by Jakub Wilk.

Release 1.6.2 (4 Sep 2016)
--------------------------

* Added generate_user_certificate() and generate_host_certificate() methods
  to SSHKey class to generate SSH certificates, and export_certificate()
  and write_certificate() methods on SSHCertificate class to export
  certificates for use in other tools.

* Improved editor unit tests to eliminate timing dependency.

* Cleaned up a few minor documentation issues.

Release 1.6.1 (27 Aug 2016)
---------------------------

* Added generate_private_key() function to create new DSA, RSA, ECDSA, or
  Ed25519 private keys which can be used as SSH user and host keys.

* Removed an unintended dependency in the SSHLineEditor on session objects
  keep a private member which referenced the corresponding channel.

* Fixed a race condition in SFTP unit tests.

* Updated dependencies to require version 1.5 of the cryptography module
  and started to take advantage of the new one-shot sign and verify
  APIs it now supports.

* Clarified the documentation of the default return value of eof_received().

* Added new multi-user client and server examples, showing a single
  process opening multiple SSH connections in parallel.

* Updated development status and Python versions listed in setup.py.


Release 1.6.0 (13 Aug 2016)
---------------------------

* Added new create_process() and run() APIs modeled after the "subprocess"
  module to simplify redirection of stdin, stdout, and stderr and
  collection of output from remote SSH processes.

* Added input line editing and echoing capabilities to better support
  interactive SSH server applications. AsyncSSH server sessions will now
  automatically perform input echoing and provide basic line editing
  capabilities to clients which request a pseudo-terminal, avoiding the
  need for applications to provide this functionality.

* Added the ability to use SSHReader objects as async iterators in
  Python 3.5, returning input a line at a time.

* Added support for the IUTF8 terminal mode now recognized by OpenSSH 7.3.

* Fixed a bug where an SSHReader read() call could return an empty string
  when it followed a call to readline() instead of blocking until more
  input was available.

* Updated AsyncSSH to use the bcrypt package from PyCA, now that it
  has support for the kdf function.

* Updated the documentation and examples to show how to take advantage
  of the new features listed here.

Release 1.5.6 (18 Jun 2016)
---------------------------

* Added support for Python 3.5 asynchronous context managers in
  SSHConnection, SFTPClient, and SFTPFile, while still maintaining
  backward compatibility with older Python 3.4 syntax.

* Updated bcrypt check in test code to only test features that depend
  on it when the right version is available.

* Switched testing over to using tox to better support testing on
  multiple versions of Python.

* Added tests of new Python 3.5 async syntax.

* Expanded Travis CI coverage to test both Python 3.4 and 3.5 on MacOS.

* Updated documentation and examples to use Python 3.5 syntax.

Release 1.5.5 (11 Jun 2016)
---------------------------

* Updated public_key module to make sure the right version of bcrypt is
  installed before attempting to use it.

* Updated forward and sftp module unit tests to work better on Linux.

* Changed README links to point at new readthedocs.io domain.


Release 1.5.4 (6 Jun 2016)
--------------------------

* Added support for setting custom SSH client and server version strings.

* Added unit tests for the sftp module, bringing AsyncSSH up to 100%
  code coverage under test on all modules.

* Added new wait_closed() method in SFTPClient class to wait for an
  SFTP client session to be fully closed.

* Fixed an issue with error handling in new parallel SFTP file copy code.

* Fixed some other minor issues in SFTP found during unit tests.

* Fixed some minor documentation issues.

Release 1.5.3 (2 Apr 2016)
--------------------------

* Added support for opening tunneled SSH connections, where an SSH
  connection is opened over another SSH connection's direct TCP/IP
  channel.

* Improve performance of SFTP over high latency connections by having
  the internal copy method issue multiple read requests in parallel.

* Reworked SFTP to mark all coroutine functions explicitly, to provide
  better compatibility with the new Python 3.5 "await" syntax.

* Reworked create_connection() and create_server() functions to do
  argument checking immediately rather than in the SSHConnection
  constructors, improving error reporting and avoiding a bug in
  asyncio which can leak socket objects.

* Fixed a hang which could occur when attempting to close an SSH
  connection with a listener still active.

* Fixed an error related to passing keys in via public_key_auth_requested().

* Fixed a potential leak of an SSHAgentClient object when an error occurs
  while opening a client connection.

* Fixed some race conditions related to channel and connection closes.

* Fixed some minor documentation issues.

* Continued to expand unit test coverage, completing coverage of the
  connection module.

Release 1.5.2 (25 Feb 2016)
---------------------------

* Fixed a bug in UNIX domain socket forwarding introduced in 1.5.1 by the
  TCP_NODELAY change.

* Fixed channel code to report when a channel is closed with incomplete
  Unicode data in the receive buffer. This was previously reported
  correctly when EOF was received on a channel, but not when it was
  closed without sending EOF.

* Added unit tests for channel, forward, and stream modules, partial
  unit tests for the connection module, and a placeholder for unit
  tests for the sftp module.

Release 1.5.1 (23 Feb 2016)
---------------------------

* Added basic support for running AsyncSSH on Windows. Some functionality
  such as UNIX domain sockets will not work there, and the test suite will
  not run there yet, but basic functionality has been tested and seems
  to work. This includes features like bcrypt and support for newer
  ciphers provided by libnacl when these optional packages are installed.

* Greatly improved the performance of known_hosts matching on exact
  hostnames and addresses. Full wildcard pattern matching is still
  supported, but entries involving exact hostnames or addresses are
  now matched thousands of times faster.

* Split known_hosts parsing and matching into separate calls so that a
  known_hosts file can be parsed once and used to make connections to
  several different hosts. Thanks go to Josh Yudaken for suggesting
  this and providing a sample implementation.

* Updated AsyncSSH to allow SSH agent forwarding when it is requested
  even when local client keys are used to perform SSH authentication.

* Updaded channel state machine to better handle close being received
  while the channel is paused for reading. Previously, some data would
  not be delivered in this case.

* Set TCP_NODELAY on sockets to avoid latency problems caused by TCP
  delayed ACK.

* Fixed a bug where exceptions were not always returned properly when
  attempting to drain writes on a stream.

* Fixed a bug which could leak a socket object after an error opening
  a local TCP listening socket.

* Fixed a number of race conditions uncovered during unit testing.

Release 1.5.0 (27 Jan 2016)
---------------------------

* Added support for OpenSSH-compatible direct and forwarded UNIX domain
  socket channels and local and remote UNIX domain socket forwarding.

* Added support for client and server side ssh-agent forwarding.

* Fixed the open_connection() method on SSHServerConnection to not include
  a handler_factory argument. This should only have been present on the
  start_server() method.

* Fixed wait_closed() on SSHForwardListener to work properly when a
  close is in progress at the time of the call.

Release 1.4.1 (23 Jan 2016)
---------------------------

* Fixed a bug in SFTP introduced in 1.4.0 related to handling of
  responses to non-blocking file closes.

* Updated code to avoid calling asyncio.async(), deprecated in
  Python 3.4.4.

* Updated unit tests to avoid errors on systems with an older version
  of OpenSSL installed.

Release 1.4.0 (17 Jan 2016)
---------------------------

* Added ssh-agent client support, automatically using it when SSH_AUTH_SOCK
  is set and client private keys aren't explicitly provided.

* Added new wait_closed() API on SSHConnection to allow applications to wait
  for a connection to be fully closed and updated examples to use it.

* Added a new login_timeout argument when create an SSH server.

* Added a missing acknowledgement response when canceling port forwarding
  and fixed a few other issues related to cleaning up port forwarding
  listeners.

* Added handlers to improve the catching and reporting of exceptions that
  are raised in asynchronous tasks.

* Reworked channel state machine to perform clean up on a channel only
  after a close is both sent and received.

* Fixed SSHChannel to run the connection_lost() handler on the SSHSession
  before unblocking callers of wait_closed().

* Fixed wait_closed() on SSHListener to wait for the acknowledgement from
  the SSH server before returning.

* Fixed a race condition in port forwarding code.

* Fixed a bug related to sending a close on a channel which got a failure
  when being opened.

* Fixed a bug related to handling term_type being set without term_size.

* Fixed some issues related to the automatic conversion of client
  keyboard-interactive auth to password auth. With this change, automatic
  conversion will only occur if the application doesn't override the
  kbdint_challenge_received() method and it will only attempt to
  authenticate once with the password provided.

Release 1.3.2 (26 Nov 2015)
---------------------------

* Added server-side support for handling password changes during password
  authentication, and fixed a few other auth-related bugs.

* Added the ability to override the automatic support for keyboard-interactive
  authentication when password authentication is supported.

* Fixed a race condition in unblocking streams.

* Removed support for OpenSSH v00 certificates now that OpenSSH no longer
  supports them.

* Added unit tests for auth module.

Release 1.3.1 (6 Nov 2015)
--------------------------

* Updated AsyncSSH to depend on version 1.1 or later of PyCA and added
  support for using its new Elliptic Curve Diffie Hellman (ECDH)
  implementation, replacing the previous AsyncSSH native Python
  version.

* Added support for specifying a passphrase in the create_connection,
  create_server, connect, and listen functions to allow file names
  or byte strings containing encrypted client and server host keys
  to be specified in those calls.

* Fixed handling of cancellation in a few AsyncSSH calls, so it is
  now possible to make calls to things like stream read or drain which
  time out.

* Fixed a bug in keyboard-interactive fallback to password auth which
  was introduced when support was added for auth functions optionally
  being coroutines.

* Move bcrypt check in encrypted key handling until it is needed so
  better errors can be returned if a passphrase is not specified or the
  key derivation function used in a key is unknown.

* Added unit tests for the auth_keys module.

* Updated unit tests to better handle bcrypt or libnacl not being
  installed.

Release 1.3.0 (10 Oct 2015)
---------------------------

* Updated AsyncSSH dependencies to make PyCA version 1.0.0 or later
  mandatory and remove the older PyCrypto support. This change also
  adds support for the PyCA implementation of ECDSA and removes support
  for RC2-based private key encryption that was only supported by
  PyCrypto.

* Refactored ECDH and Curve25519 key exchange code so they can share an
  implementation, and prepared the code for adding a PyCA shim for this
  as soon as support for that is released.

* Hardened the DSA and RSA implementations to do stricter checking of the
  key exchange response, and sped up the RSA implementation by taking
  advantage of optional RSA private key parameters when they are present.

* Added support for asynchronous client and server authentication,
  allowing auth-related callbacks in SSHClient and SSHServer to optionally
  be defined as coroutines.

* Added support for asynchronous SFTP server processing, allowing callbacks
  in SFTPServer to optionally be defined as coroutines.

* Added support for a broader set of open mode flags in the SFTP server.
  Note that this change is not completely backward compatible with previous
  releases. If you have application code which expects a Python mode
  string as an argument to SFTPServer open method, it will need to be
  changed to expect a pflags value instead.

* Fixed handling of eof_received() when it returns false to close the
  half-open connection but still allow sending or receiving of exit status
  and exit signals.

* Added unit tests for the asn1, cipher, compression, ec, kex, known_hosts,
  mac, and saslprep modules and expended the set of pbe and public_key
  unit tests.

* Fixed a set of issues uncovered by ASN.1 unit tests:

    * Removed extra 0xff byte when encoding integers of the form -128*256^n
    * Fixed decoding error for OIDs beginning with 2.n where n >= 40
    * Fixed range check for second component of ObjectIdentifier
    * Added check for extraneous 0x80 bytes in ObjectIdentifier components
    * Added check for negative component values in ObjectIdentifier
    * Added error handling for ObjectIdentifier components being non-integer
    * Added handling for missing length byte after extended tag
    * Raised ASN1EncodeError instead of TypeError on unsupported types

* Added validation on asn1_class argument, and equality and hash methods
  to BitString, RawDERObject, and TaggedDERObject. Also, reordered
  RawDERObject arguments to be consistent with TaggedDERObject and added
  str method to ObjectIdentifier.

* Fixed a set of issues uncovered by additional pbe unit tests:

    * Encoding and decoding of PBES2-encrypted keys with a PRF other than
      SHA1 is now handled correctly.
    * Some exception messages were made more specific.
    * Additional checks were put in for empty salt or zero iteration count
      in encryption parameters.

* Fixed a set of issues uncovered by additional public key unit tests:

    * Properly handle PKCS#8 keys with invalid ASN.1 data
    * Properly handle PKCS#8 DSA & RSA keys with non-sequence for arg_params
    * Properly handle attempts to import empty string as a public key
    * Properly handle encrypted PEM keys with missing DEK-Info header
    * Report check byte mismatches for encrypted OpenSSH keys as bad passphrase
    * Return KeyImportError instead of KeyEncryptionError when passphrase
      is needed but not provided

* Added information about branches to CONTRIBUTING guide.

* Performed a bunch of code cleanup suggested by pylint.

Release 1.2.1 (26 Aug 2015)
---------------------------

* Fixed a problem with passing in client_keys=None to disable public
  key authentication in the SSH client.

* Updated Unicode handling to allow multi-byte Unicode characters to be
  split across successive SSH data messages.

* Added a note to the documentation for AsyncSSH create_connection()
  explaining how to perform the equivalent of a connect with a timeout.

Release 1.2.0 (6 Jun 2015)
--------------------------

* Fixed a problem with the SSHConnection context manager on Python versions
  older than 3.4.2.

* Updated the documentation for get_extra_info() in the SSHConnection,
  SSHChannel, SSHReader, and SSHWriter classes to contain pointers
  to get_extra_info() in their parent transports to make it easier to
  see all of the attributes which can be queried.

* Clarified the legal return values for the session_requested(),
  connection_requested(), and server_requested() methods in
  SSHServer.

* Eliminated calls to the deprecated importlib.find_loader() method.

* Made improvements to README suggested by Nicholas Chammas.

* Fixed a number of issues identified by pylint.

Release 1.1.1 (25 May 2015)
---------------------------

* Added new start_sftp_server method on SSHChannel to allow applications
  using the non-streams API to start an SFTP server.

* Enhanced the default format_longname() method in SFTPServer to properly
  handle the case where not all of the file attributes are returned by
  stat().

* Fixed a bug related to the new allow_pty parameter in create_server.

* Fixed a bug in the hashed known_hosts support introduced in some recent
  refactoring of the host pattern matching code.

Release 1.1.0 (22 May 2015)
---------------------------

* SFTP is now supported!

  * Both client and server support is available.
  * SFTP version 3 is supported, with OpenSSH extensions.
  * Recursive transfers and glob matching are supported in the client.
  * File I/O APIs allow files to be accessed without downloading them.

* New simplified connect and listen APIs have been added.

* SSHConnection can now be used as a context manager.

* New arguments to create_server now allow the specification of a
  session_factory and encoding or sftp_factory as well as controls
  over whether a pty is allowed and the window and max packet size,
  avoiding the need to create custom SSHServer subclasses or custom
  SSHServerChannel instances.

* New examples have been added for SFTP and to show the use of the new
  connect and listen APIs.

* Copyrights in changed files have all been updated to 2015.

Release 1.0.1 (13 Apr 2015)
---------------------------

* Fixed a bug in OpenSSH private key encryption introduced in some
  recent cipher refactoring.

* Added bcrypt and libnacl as optional dependencies in setup.py.

* Changed test_keys test to work properly when bcrypt or libnacl aren't
  installed.

Release 1.0.0 (11 Apr 2015)
---------------------------

* This release finishes adding a number of major features, finally making
  it worthy of being called a "1.0" release.

* Host and user certificates are now supported!

  * Enforcement is done on principals in certificates.
  * Enforcement is done on force-command and source-address critical options.
  * Enforcement is done on permit-pty and permit-port-forwarding extensions.

* OpenSSH-style known hosts files are now supported!

  * Positive and negative wildcard and CIDR-style patterns are supported.
  * HMAC-SHA1 hashed host entries are supported.
  * The @cert-authority and @revoked markers are supported.

* OpenSSH-style authorized keys files are now supported!

  * Both client keys and certificate authorities are supported.
  * Enforcement is done on from and principals options during key matching.
  * Enforcement is done on no-pty, no-port-forwarding, and permitopen.
  * The command and environment options are supported.
  * Applications can query for their own non-standard options.

* Support has been added for OpenSSH format private keys.

  * DSA, RSA, and ECDSA keys in this format are now supported.
  * Ed25519 keys are supported when libnacl and libsodium are installed.
  * OpenSSH private key encryption is supported when bcrypt is installed.

* Curve25519 Diffie-Hellman key exchange is now available via either the
  curve25519-donna or libnacl and libsodium packages.

* ECDSA key support has been enhanced.

  * Support is now available for PKCS#8 ECDSA v2 keys.
  * Support is now available for both NamedCurve and explicit ECParameter
    versions of keys, as long as the parameters match one of the supported
    curves (nistp256, nistp384, or nistp521).

* Support is now available for the OpenSSH chacha20-poly1305 cipher when
  libnacl and libsodium are installed.

* Cipher names specified in private key encryption have been changed to be
  consistent with OpenSSH cipher naming, and all SSH ciphers can now be
  used for encryption of keys in OpenSSH private key format.

* A couple of race conditions in SSHChannel have been fixed and channel
  cleanup is now delayed to allow outstanding message handling to finish.

* Channel exceptions are now properly delivered in the streams API.

* A bug in SSHStream read() where it could sometimes return more data than
  requested has been fixed. Also, read() has been changed to properly block
  and return all data until EOF or a signal is received when it is called
  with no length.

* A bug in the default implementation of keyboard-interactive authentication
  has been fixed, and the matching of a password prompt has been loosened
  to allow it to be used for password authentication on more devices.

* Missing code to resume reading after a stream is paused has been added.

* Improvements have been made in the handling of canceled requests.

* The test code has been updated to test Ed25519 and OpenSSH format
  private keys.

* Examples have been updated to reflect some of the new capabilities.

Release 0.9.2 (26 Jan 2015)
---------------------------

* Fixed a bug in PyCrypto CipherFactory introduced during PyCA refactoring.

Release 0.9.1 (3 Dec 2014)
--------------------------

* Added some missing items in setup.py and MANIFEST.in.

* Fixed the install to work even when cryptographic dependencies aren't
  yet installed.

* Fixed an issue where get_extra_info calls could fail if called when
  a connection or session was shutting down.

Release 0.9.0 (14 Nov 2014)
---------------------------

* Added support to use PyCA (0.6.1 or later) for cryptography. AsyncSSH
  will automatically detect and use either PyCA, PyCrypto, or both depending
  on which is installed and which algorithms are requested.

* Added support for AES-GCM ciphers when PyCA is installed.

Release 0.8.4 (12 Sep 2014)
---------------------------

* Fixed an error in the encode/decode functions for PKCS#1 DSA public keys.

* Fixed a bug in the unit test code for import/export of RFC4716 public keys.

Release 0.8.3 (16 Aug 2014)
---------------------------

* Added a missing import in the curve25519 implementation.

Release 0.8.2 (16 Aug 2014)
---------------------------

* Provided a better long description for PyPI.

* Added link to PyPI in documentation sidebar.

Release 0.8.1 (15 Aug 2014)
---------------------------

* Added a note in the :meth:`validate_public_key()
  <SSHServer.validate_public_key>` documentation clarifying that AsyncSSH
  will verify that the client possesses the corresponding private key before
  authentication is allowed to succeed.

* Switched from setuptools to distutils and added an initial set of unit
  tests.

* Prepared the package to be uploaded to PyPI.

Release 0.8.0 (15 Jul 2014)
---------------------------

* Added support for Curve25519 Diffie Hellman key exchange on systems with
  the curve25519-donna Python package installed.

* Updated the examples to more clearly show what values are returned even
  when not all of the return values are used.

Release 0.7.0 (7 Jun 2014)
--------------------------

* This release adds support for the "high-level" ``asyncio`` streams API,
  in the form of the :class:`SSHReader` and :class:`SSHWriter` classes
  and wrapper methods such as :meth:`open_session()
  <SSHClientConnection.open_session>`, :meth:`open_connection()
  <SSHClientConnection.open_connection>`, and :meth:`start_server()
  <SSHClientConnection.start_server>`. It also allows the callback
  methods on :class:`SSHServer` to return either SSH session objects or
  handler functions that take :class:`SSHReader` and :class:`SSHWriter`
  objects as arguments. See :meth:`session_requested()
  <SSHServer.session_requested>`, :meth:`connection_requested()
  <SSHServer.connection_requested>`, and :meth:`server_requested()
  <SSHServer.server_requested>` for more information.

* Added new exceptions :exc:`BreakReceived`, :exc:`SignalReceived`, and
  :exc:`TerminalSizeChanged` to report when these messages are received
  while trying to read from an :class:`SSHServerChannel` using the new
  streams API.

* Changed :meth:`create_server() <SSHClientConnection.create_server>` to
  accept either a callable or a coroutine for its ``session_factory``
  argument, to allow asynchronous operations to be used when deciding
  whether to accept a forwarded TCP connection.

* Renamed ``accept_connection()`` to :meth:`create_connection()
  <SSHServerConnection.create_connection>` in the :class:`SSHServerConnection`
  class for consistency with :class:`SSHClientConnection`, and added a
  corresponding :meth:`open_connection() <SSHServerConnection.open_connection>`
  method as part of the streams API.

* Added :meth:`get_exit_status() <SSHClientChannel.get_exit_status>` and
  :meth:`get_exit_signal() <SSHClientChannel.get_exit_signal>` methods
  to the :class:`SSHClientChannel` class.

* Added :meth:`get_command() <SSHServerChannel.get_command>` and
  :meth:`get_subsystem() <SSHServerChannel.get_subsystem>` methods to
  the :class:`SSHServerChannel` class.

* Fixed the name of the :meth:`write_stderr() <SSHServerChannel.write_stderr>`
  method and added the missing :meth:`writelines_stderr()
  <SSHServerChannel.writelines_stderr>` method to the :class:`SSHServerChannel`
  class for outputting data to the stderr channel.

* Added support for a return value in the :meth:`eof_received()
  <SSHClientSession.eof_received>` of :class:`SSHClientSession`,
  :class:`SSHServerSession`, and :class:`SSHTCPSession` to support
  half-open channels. By default, the channel is automatically closed
  after :meth:`eof_received() <SSHClientSession.eof_received>` returns,
  but returning ``True`` will now keep the channel open, allowing output
  to still be sent on the half-open channel. This is done automatically
  when the new streams API is used.

* Added values ``'local_peername'`` and ``'remote_peername'`` to the set
  of information available from the :meth:`get_extra_info()
  <SSHTCPChannel.get_extra_info>` method in the :class:`SSHTCPChannel` class.

* Updated functions returning :exc:`IOError` or :exc:`socket.error` to
  return the new :exc:`OSError` exception introduced in Python 3.3.

* Cleaned up some errors in the documentation.

* The :ref:`API`, :ref:`ClientExamples`, and :ref:`ServerExamples` have
  all been updated to reflect these changes, and new examples showing the
  streams API have been added.

Release 0.6.0 (11 May 2014)
---------------------------

* This release is a major revamp of the code to migrate from the
  ``asyncore`` framework to the new ``asyncio`` framework in Python
  3.4. All the APIs have been adapted to fit the new ``asyncio``
  paradigm, using coroutines wherever possible to avoid the need
  for callbacks when performing asynchronous operations.

  So far, this release only supports the "low-level" ``asyncio`` API.

* The :ref:`API`, :ref:`ClientExamples`, and :ref:`ServerExamples` have
  all been updated to reflect these changes.


Release 0.5.0 (11 Oct 2013)
---------------------------

* Added the following new classes to support fully asynchronous
  connection forwarding, replacing the methods previously added in
  release 0.2.0:

  * :class:`SSHClientListener`
  * :class:`SSHServerListener`
  * :class:`SSHClientLocalPortForwarder`
  * :class:`SSHClientRemotePortForwarder`
  * :class:`SSHServerPortForwarder`

  These new classes allow for DNS lookups and other operations to be
  performed fully asynchronously when new listeners are set up. As with
  the asynchronous connect changes below, methods are now available
  to report when the listener is opened or when an error occurs during
  the open rather than requiring the listener to be fully set up in a
  single call.

* Updated examples in :ref:`ClientExamples` and :ref:`ServerExamples`
  to reflect the above changes.

Release 0.4.0 (28 Sep 2013)
---------------------------

* Added support in :class:`SSHTCPConnection` for the following methods
  to allow asynchronous operations to be used when accepting inbound
  connection requests:

  * :meth:`handle_open_request() <SSHTCPConnection.handle_open_request>`
  * :meth:`report_open() <SSHTCPConnection.report_open>`
  * :meth:`report_open_error() <SSHTCPConnection.report_open_error>`

  These new methods are used to implement asynchronous connect
  support for local and remote port forwarding, and to support
  trying multiple destination addresses when connection failures
  occur.

* Cleaned up a few minor documentation errors.

Release 0.3.0 (26 Sep 2013)
---------------------------

* Added support in :class:`SSHClient` and :class:`SSHServer` for setting
  the key exchange, encryption, MAC, and compression algorithms allowed
  in the SSH handshake.

* Refactored the algorithm selection code to pull a common matching
  function back into ``_SSHConnection`` and simplify other modules.

* Extended the listener class to open multiple listening sockets when
  necessary, fixing a bug where sockets opened to listen on ``localhost``
  were not properly accepting both IPv4 and IPv6 connections.

  Now, any listen request which resolves to multiple addresses will open
  listening sockets for each address.

* Fixed a bug related to tracking of listeners opened on dynamic ports.

Release 0.2.0 (21 Sep 2013)
---------------------------

* Added support in :class:`SSHClient` for the following methods related
  to performing standard SSH port forwarding:

  * :meth:`forward_local_port() <SSHClient.forward_local_port>`
  * :meth:`cancel_local_port_forwarding() <SSHClient.cancel_local_port_forwarding>`
  * :meth:`forward_remote_port() <SSHClient.forward_remote_port>`
  * :meth:`cancel_remote_port_forwarding() <SSHClient.cancel_remote_port_forwarding>`
  * :meth:`handle_remote_port_forwarding() <SSHClient.handle_remote_port_forwarding>`
  * :meth:`handle_remote_port_forwarding_error() <SSHClient.handle_remote_port_forwarding_error>`

* Added support in :class:`SSHServer` for new return values in
  :meth:`handle_direct_connection() <SSHServer.handle_direct_connection>`
  and :meth:`handle_listen() <SSHServer.handle_listen>` to activate
  standard SSH server-side port forwarding.

* Added a client_addr argument and member variable to :class:`SSHServer`
  to hold the client's address information.

* Added and updated examples related to port forwarding and using
  :class:`SSHTCPConnection` to open direct and forwarded TCP
  connections in :ref:`ClientExamples` and :ref:`ServerExamples`.

* Cleaned up some of the other documentation.

* Removed a debug print statement accidentally left in related to
  SSH rekeying.

Release 0.1.0 (14 Sep 2013)
---------------------------

* Initial release
