from fastapi.responses import StreamingResponse


def stream_response(generator):

    return StreamingResponse(
        generator,
        media_type="text/plain"
    )