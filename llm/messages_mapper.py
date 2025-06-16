from model.domain.request import Request


def map_request_to_messages(request: Request):
    messages = []
    if request.content:
        messages.append({"type": "text", "text": request.content})
    for asset in request.assets:
        messages.append({"type": "image_url", "image_url": {"url": asset}})

    return messages
