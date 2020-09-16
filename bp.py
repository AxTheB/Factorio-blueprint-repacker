import base64
import zlib
import sys
import pyperclip


def to_json(export):
    try:
        version = export[0]
        payload = export[1:]
        payload_compressed = base64.b64decode(payload)
        payload_json = zlib.decompress(payload_compressed)
    except IndexError:
        return "Does not look like a valid blueprint string"
    return payload_json.decode()


def to_export(content):
    content = "".join(content)
    payload_compressed = zlib.compress(content.strip().encode(), 9)
    payload_enc = b"0" + base64.standard_b64encode(payload_compressed)
    payload = payload_enc.decode().strip()
    pyperclip.copy(payload)
    return payload


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as ifile:
            content = ifile.read()
            if content[0] == "0":
                print(to_json(content))
            else:
                print(to_export(content))
    else:
        content = pyperclip.paste()
        print(to_json(content))
