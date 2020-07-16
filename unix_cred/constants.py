import sys

if sys.platform.startswith("netbsd"):
    LOCAL_PEEREID = 0x0003

if sys.platform.startswith(("freebsd", "dragonfly", "darwin")):
    XUCRED_VERSION = 0
    XU_NGROUPS = 16
