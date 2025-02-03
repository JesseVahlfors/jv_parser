
def json_parser(file):
    with open(file, "r") as f:
        data = f.read()
        braces_equal = data.count("{") == data.count("}")
        quotes_equal = data.count("\"") % 2 == 0 if data.count("\"") > 0 else True
        commas_correct = data.count(",") == data.count(":") - 1 if data.count(",") > 0 else True
        if data:
            if braces_equal and quotes_equal and commas_correct:
                return eval(data)
    return "Invalid JSON"
