# cython: language_level=3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#


import errno


class DBusBaseError(Exception):
    def __init__(self, errno, err_name=None, err_message=None):
      is_base_error = self.__class__.__name__ == 'DBusBaseError'
      custom_msg = (
        "\nThis is DBusBaseError, a base error for DBus (i bet you did not "
        "see that coming) if you need a special error, enhance "
        "pystemd.sysdexc module!."
      ) if is_base_error else ''

      self.errno = errno
      self.err_name = (err_name or '') if is_base_error else ''
      self.err_message = err_message or ''

      super(DBusBaseError, self).__init__(
            '%s[err %s]: %s%s' % (self.err_name,
                              self.errno,
                              self.err_message, custom_msg))


class DBusFailedError(DBusBaseError):
    pass


class DBusNoMemoryError(DBusBaseError):
    pass


class DBusServiceUnknownError(DBusBaseError):
    pass


class DBusNameHasNoOwnerError(DBusBaseError):
    pass


class DBusNoReplyError(DBusBaseError):
    pass


class DBusIOErrorError(DBusBaseError):
    pass


class DBusBadAddressError(DBusBaseError):
    pass


class DBusNotSupportedError(DBusBaseError):
    pass


class DBusLimitsExceededError(DBusBaseError):
    pass


class DBusAccessDeniedError(DBusBaseError):
    pass


class DBusAuthFailedError(DBusBaseError):
    pass


class DBusNoServerError(DBusBaseError):
    pass


class DBusTimeoutError(DBusBaseError):
    pass


class DBusTimedOutError(DBusBaseError):
    pass


class DBusNoNetworkError(DBusBaseError):
    pass


class DBusAddressInUseError(DBusBaseError):
    pass


class DBusDisconnectedError(DBusBaseError):
    pass


class DBusInvalidArgsError(DBusBaseError):
    pass


class DBusFileNotFoundError(DBusBaseError):
    pass


class DBusFileExistsError(DBusBaseError):
    pass


class DBusUnknownMethodError(DBusBaseError):
    pass


class DBusUnknownObjectError(DBusBaseError):
    pass


class DBusUnknownInterfaceError(DBusBaseError):
    pass


class DBusUnknownPropertyError(DBusBaseError):
    pass


class DBusPropertyReadOnlyError(DBusBaseError):
    pass


class DBusUnixProcessIdUnknownError(DBusBaseError):
    pass


class DBusInvalidSignatureError(DBusBaseError):
    pass


class DBusInconsistentMessageError(DBusBaseError):
    pass


class DBusMatchRuleNotFoundError(DBusBaseError):
    pass


class DBusMatchRuleInvalidError(DBusBaseError):
    pass


class DBusInteractiveAuthorizationRequiredError(DBusBaseError):
    pass


class DBusNoSuchUnitError(DBusBaseError):
    pass


class DBusConnectionRefusedError(DBusBaseError):
    pass


class DBusInterruptedError(DBusBaseError, InterruptedError):
    pass


cdef dict DBUS_ERROR_MAP = {
    b"org.freedesktop.DBus.Error.Failed": DBusFailedError,
    b"org.freedesktop.DBus.Error.NoMemory": DBusNoMemoryError,
    b"org.freedesktop.DBus.Error.ServiceUnknown": DBusServiceUnknownError,
    b"org.freedesktop.DBus.Error.NameHasNoOwner": DBusNameHasNoOwnerError,
    b"org.freedesktop.DBus.Error.NoReply": DBusNoReplyError,
    b"org.freedesktop.DBus.Error.IOError": DBusIOErrorError,
    b"org.freedesktop.DBus.Error.BadAddress": DBusBadAddressError,
    b"org.freedesktop.DBus.Error.NotSupported": DBusNotSupportedError,
    b"org.freedesktop.DBus.Error.LimitsExceeded": DBusLimitsExceededError,
    b"org.freedesktop.DBus.Error.AccessDenied": DBusAccessDeniedError,
    b"org.freedesktop.DBus.Error.AuthFailed": DBusAuthFailedError,
    b"org.freedesktop.DBus.Error.NoServer": DBusNoServerError,
    b"org.freedesktop.DBus.Error.Timeout": DBusTimeoutError,
    b'org.freedesktop.DBus.Error.TimedOut': DBusTimedOutError,
    b"org.freedesktop.DBus.Error.NoNetwork": DBusNoNetworkError,
    b"org.freedesktop.DBus.Error.AddressInUse": DBusAddressInUseError,
    b"org.freedesktop.DBus.Error.Disconnected": DBusDisconnectedError,
    b"org.freedesktop.DBus.Error.InvalidArgs": DBusInvalidArgsError,
    b"org.freedesktop.DBus.Error.FileNotFound": DBusFileNotFoundError,
    b"org.freedesktop.DBus.Error.FileExists": DBusFileExistsError,
    b"org.freedesktop.DBus.Error.UnknownMethod": DBusUnknownMethodError,
    b"org.freedesktop.DBus.Error.UnknownObject": DBusUnknownObjectError,
    b"org.freedesktop.DBus.Error.UnknownInterface": DBusUnknownInterfaceError,
    b"org.freedesktop.DBus.Error.UnknownProperty": DBusUnknownPropertyError,
    b"org.freedesktop.DBus.Error.PropertyReadOnly": DBusPropertyReadOnlyError,
    b"org.freedesktop.DBus.Error.UnixProcessIdUnknown": DBusUnixProcessIdUnknownError,
    b"org.freedesktop.DBus.Error.InvalidSignature": DBusInvalidSignatureError,
    b"org.freedesktop.DBus.Error.InconsistentMessage": DBusInconsistentMessageError,
    b"org.freedesktop.DBus.Error.MatchRuleNotFound": DBusMatchRuleNotFoundError,
    b"org.freedesktop.DBus.Error.MatchRuleInvalid": DBusMatchRuleInvalidError,
    b"org.freedesktop.DBus.Error.InteractiveAuthorizationRequired":
        DBusInteractiveAuthorizationRequiredError,
    b"org.freedesktop.systemd1.NoSuchUnit": DBusNoSuchUnitError,
    b"System.Error.EINTR": DBusInterruptedError,
}


cdef dict OS_ERROR_MAP = {
    -errno.ECONNREFUSED: DBusConnectionRefusedError,
    -errno.ENOENT: DBusFileNotFoundError,
}


def DBusError(err_no, err_name=None, err_message=""):
    return DBUS_ERROR_MAP.get(
        err_name, OS_ERROR_MAP.get(err_no, DBusBaseError)
    )(err_no, err_name, err_message)
