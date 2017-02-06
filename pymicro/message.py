import umsgpack
import itsdangerous

class CorruptedMessageError(Exception):
    """Exception rased when the message is corrupted."""
    pass

class Message:
    @staticmethod
    def pack(obj, secret=None):
        data = umsgpack.packb(obj)
        if secret:
            return itsdangerous.Signer(secret).sign(data)
        else:
            return data

    @staticmethod
    def unpack(data, secret=None):
        if secret:
            data = itsdangerous.Signer(secret).unsign(data)

        message = umsgpack.unpackb(data)
        if not isinstance(message, dict):
            raise CorruptedMessageError('Deserialized garbage')

        return message
