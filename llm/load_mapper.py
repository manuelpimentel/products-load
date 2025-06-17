from model.domain.load import Load


def map_load_to_content(load: Load):
    messages = []
    if load.content:
        messages.append({"type": "text", "text": load.content})
    for asset in load.assets:
        messages.append({"type": "image_url", "image_url": {"url": asset}})

    return messages
