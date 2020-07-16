import errno

from unix_cred.util import build_oserror


def test_build_oserror() -> None:
    assert str(build_oserror(errno.EINVAL)) == "[Errno {}] Invalid argument".format(errno.EINVAL)
    assert str(build_oserror(errno.EINVAL, None)) == "[Errno {}] Invalid argument".format(
        errno.EINVAL
    )
    assert str(build_oserror(errno.EINVAL, None, None)) == "[Errno {}] Invalid argument".format(
        errno.EINVAL
    )

    assert str(build_oserror(errno.EINVAL, "")) == "[Errno {}] Invalid argument: ''".format(
        errno.EINVAL
    )
    assert str(build_oserror(errno.EINVAL, "a")) == "[Errno {}] Invalid argument: 'a'".format(
        errno.EINVAL
    )

    assert str(
        build_oserror(errno.EINVAL, "", "")
    ) == "[Errno {}] Invalid argument: '' -> ''".format(errno.EINVAL)
    assert str(
        build_oserror(errno.EINVAL, "a", "b")
    ) == "[Errno {}] Invalid argument: 'a' -> 'b'".format(errno.EINVAL)
