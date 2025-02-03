
def json_parser(file):
    with open(file, "r") as f:
        data = f.read()
    return data if data else ""
