import umsgpack
import itsdangerous

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
        return umsgpack.unpackb(data)
