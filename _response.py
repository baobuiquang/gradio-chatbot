def generate_response(message):
    response = "[(" + message + ")]"
    suggestions = [[response+"-1"], [response+"-2"], [response+"-3"]]
    return response, suggestions