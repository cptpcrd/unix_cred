.. unix-cred documentation master file, created by
   sphinx-quickstart on Mon Jul 20 14:37:28 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to unix-cred's documentation!
=====================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Cross-platform interfaces
=========================

For most use cases, these interfaces (in particular :py:func:`get_peer_uid_gid()`) should be enough.

.. py:function:: get_peer_uid_gid(sock)

   Returns the ``(uid, gid)`` of the peer connected to the given **stream** socket.


.. py:function:: get_peer_pid_uid_gid(sock)

   Returns the ``(pid, uid, gid)`` of the peer connected to the given **stream** socket.

   On some platforms, this function is not available. On other platforms, the returned PID
   may be ``None`` if the current version of that platform does not support retrieving the PID
   (for example, FreeBSD prior to version 13 does not, and will always return ``None``).

   Availability: Linux, OpenBSD, NetBSD, FreeBSD (PID only available on version 13+), macOS, Solaris, Illumos


Platform-specific interfaces
============================

In most cases, you should use the cross-platform interfaces. However, the platform-specific interfaces may be useful (for example, they may provide additional information).


.. py:function:: get_peerpid(sock)

   Returns the PID of the process that last accessed the given stream socket.

   Availability: macOS


.. py:module:: ucred
   :platform: Linux, OpenBSD, NetBSD

ucred
-----

The ``ucred`` module provides an interface to the ``ucred`` interface on Linux, the ``sockpeecred`` interface on OpenBSD, or the ``unpcbid`` interface on NetBSD.

The reason that the interfaces for all three of these are in one module is that they are all essentially the same interface, with only minor implementation differences (such as the order of the fields in the C struct, or the name of the socket option used to retrieve them).

.. note::
   This module is only here for completeness. In nearly all cases, you should use
   :py:func:`get_peer_pid_uid_gid()` (which has slightly better cross-platform support) instead.

.. py:class:: Ucred

   Availability: Linux, OpenBSD, NetBSD

   .. py:attribute:: pid

        :type: int

        The PID of the connected peer.

   .. py:attribute:: uid

        :type: int

        The effective UID of the connected peer.

   .. py:attribute:: gid

        :type: int

        The effective GID of the connected peer.

.. py:function:: get_ucred(sock)

   Returns a :py:class:`Ucred` object representing the credentials of the peer connected to the
   given socket.

   Availability: Linux, OpenBSD, NetBSD


.. py:module:: xucred
   :platform: FreeBSD, DragonFlyBSD, macOS

xucred
------

The ``xucred`` module provides an interface to the ``xucred`` interface on FreeBSD, DragonflyBSD, and macOS.

.. py:class:: Xucred

   Availability: FreeBSD, DragonFlyBSD, macOS

   .. py:attribute:: pid

        :type: int or None

        The PID of the connected peer.

        This attribute is only set on FreeBSD 13+. On macOS/DragonFlyBSD, and on previous versions of FreeBSD,
        it is always ``None``. Always make sure to check for a ``None`` value.

        To get the PID on macOS, use :py:func:`get_peerpid()`.

        Availability: FreeBSD 13+

   .. py:attribute:: uid

        :type: int

        The effective UID of the connected peer.

   .. py:attribute:: gid

        :type: int

        The effective GID of the connected peer.

   .. py:attribute:: groups

        :type: list[int]

        The supplementary groups of the connected peer.

        .. note::
            On macOS, the value placed in this attribute differs from that of
            `os.getgroups() <https://docs.python.org/3/library/os.html#os.getgroups>`_.
            Effectively, it always behaves as if the deployment target is less than 10.5.

        .. note::
            On FreeBSD, this group list is truncated to the first 16 supplementary groups.
            (Technically, it's also truncated on DragonflyBSD and macOS, but they only support
            16 groups normally.)

.. py:function:: get_xucred(sock)

   Returns a :py:class:`Xucred` object representing the credentials of the peer connected to the
   given socket.

   Availability: FreeBSD, DragonFlyBSD, macOS


peerucred
---------

.. py:module:: peerucred
   :platform: Solaris, Illumos

The ``peerucred`` module provides an interface to the ``getpeerucred()`` function on Solaris/Illumos.

.. warning::
   This module is experimental and has undergone no testing whatsoever. Use with caution.

.. py:class:: Ucred

   Availability: Solaris, Illumos

   .. py:attribute:: pid

        :type: int

        The PID of the connected peer.

   .. py:attribute:: ruid

        :type: int

        The real UID of the connected peer.

   .. py:attribute:: euid

        :type: int

        The effective UID of the connected peer.

   .. py:attribute:: suid

        :type: int

        The saved UID of the connected peer.

   .. py:attribute:: rgid

        :type: int

        The real GID of the connected peer.

   .. py:attribute:: egid

        :type: int

        The effective GID of the connected peer.

   .. py:attribute:: sgid

        :type: int

        The saved GID of the connected peer.

   .. py:attribute:: groups

        :type: list[int]

        The supplementary groups of the connected peer.

.. py:function:: getpeerucred(sock)

   Returns a :py:class:`Ucred` object representing the credentials of the peer connected to the
   given socket.

   Availability: Solaris, Illumos


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. vim: ts=3 expandtab
