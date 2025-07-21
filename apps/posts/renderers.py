from rest_framework.renderers import JSONRenderer

class CustomResponseRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get('response')
        status_code = getattr(response, 'status_code', 200)

        # Mặc định message theo status
        default_message = "Success" if 200 <= status_code < 300 else "Error"
        message = default_message

        if isinstance(data, dict):
            # Nếu có message trong data
            if 'message' in data:
                message = data.pop('message')

            # Nếu là response phân trang
            if 'results' in data:
                meta = {
                    'total_items': data.pop('count', None),
                    'next': data.pop('next', None),
                    'previous': data.pop('previous', None),
                }
                request = renderer_context.get('request')
                if request:
                    page = request.query_params.get('page')
                    page_size = request.query_params.get('page_size')
                    if page: meta['page'] = int(page)
                    if page_size: meta['page_size'] = int(page_size)

                return super().render({
                    'code': status_code,
                    'message': message,
                    'data': data.pop('results'),
                    'meta': meta
                }, accepted_media_type, renderer_context)

        # Trường hợp không phân trang
        return super().render({
            'code': status_code,
            'message': message,
            'data': data
        }, accepted_media_type, renderer_context)
