from rest_framework.renderers import BaseRenderer

class SSERenderer(BaseRenderer):
    media_type = 'text/event-stream'
    format = 'sse'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # Ensure the data is properly formatted as SSE
        if isinstance(data, str):
            return f"data: {data}\n\n"
        elif isinstance(data, dict):
            import json
            return f"data: {json.dumps(data)}\n\n"
        else:
            raise TypeError("Unsupported data format for SSE")
