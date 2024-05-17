from base64 import b64decode


def get_bytes_from_base64(data: str):
    if (data.startswith("data:image/png")): 
        return (b64decode(data[22:]), "image/png")
    return (b64decode(data[23:]), "image/jpeg")