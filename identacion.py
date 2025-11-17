from fastapi.responses import JSONResponse
import json

class IndentedJSONResponse(JSONResponse):
    def render(self, content: any) -> bytes:
        return json.dumps(content, indent=4, ensure_ascii=False).encode("utf-8")

