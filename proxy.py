from fastapi import Request, Response, APIRouter
from cache import get_cached_response, set_cached_response
from config import ALLOWED_DOMAIN
import httpx

router = APIRouter()

@router.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy(request: Request, full_path: str) -> Response:
    target_url: str | None = request.query_params.get("url")

    if not target_url:
        return Response(content="Missing 'url' query parameter", status_code=400)
    
    if ALLOWED_DOMAIN and not any(target_url.startswith(d) for d in ALLOWED_DOMAIN):
        return Response(content="Domain not allowed", status_code=403)

    cached: bytes | None = get_cached_response(target_url)

    if cached:
        return Response(content=cached, media_type="application/json", headers={
            "Access-Control-Allow-Origin": "*",
        })

    method: str = request.method
    headers: dict = dict(request.headers)
    body: bytes = await request.body()

    async with httpx.AsyncClient() as client:
        try:
            resp: httpx.Response = await client.request(method=method, url=target_url, headers=headers, content=body)
        except httpx.RequestError as e:
            return Response(content=str(e), status_code=500)

    content: bytes = resp.content
    set_cached_response(target_url, content)


    return Response(content=content, status_code=resp.status_code, headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,PATCH,OPTIONS",
        "Access-Control-Allow-Headers": "*"
    })