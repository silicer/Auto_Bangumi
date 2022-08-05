import uvicorn
from uvicorn.config import LOGGING_CONFIG
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:7892",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")


# HTML
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)


# Main page info
@app.get("/api/v1/info/Rules")
def get_all_rules() -> list:
    return [
        {
            "id": 1,
            "official_title": "Lycoris Recoil",
            "title_zh": "李克莉丝",
            "title_jp": "リコリス-リコイル",
            "title_en": "Lycoris Recoil",
            "year": 2022,
            "season": 1,
            "cover_url": "https://www.mangaupdates.com/images/covers/lkrs.jpg",
            "sub_group": "Lilith-Raw",
            "resolution": "1080P",
            "source": "Baha",
            "sub_language": "CHT",
            "contain": "lycoris",
            "not_contain": "720",
            "added": True,
            "eps_collect": True,
            "ep_offset": 0
        },
    ]


@app.get("/api/v1/info/Log")
async def get_log():
    log_path = "/api_demo/log/api_demo.log"
    return FileResponse(log_path)


@app.get("/api/v1/info/Config")
def get_config():
    return json_config.load(settings.setting_path)


# Set config
@app.post("/api/v1/set/Config")
def set_config(config: SetConf):
    api_func.set_config(config)
    return "Success"


# Change Rule settings
@app.post("/api/v1/set/Rule")
def change_rule(rule: ChangeRule):
    api_func.change_rule(rule)
    return "Success"


# Delete rule
@app.get("/api/v1/set/removeRule/{id}")
def remove_rule(id: str):
    return api_func.remove_rule(id)


@app.get("/api/v1/set/resetRule")
def reset_rule():
    return api_func.reset_rule()


@app.post("/api/v1/add/Collection")
async def collection(link: RssLink):
    return api_func.download_collection(link.rss_link)


@app.post("/api/v1/add/Subscribe")
async def subscribe(link: RssLink):
    return api_func.add_subscribe(link.rss_link)


@app.post("/api/v1/add/Rule")
async def add_rule(info: AddRule):
    return api_func.add_rule(info.title, info.season)


def run():
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = "[%(asctime)s] %(levelprefix)s %(message)s"
    uvicorn.run(app, host="0.0.0.0", port=settings.webui_port)


if __name__ == "__main__":
    run()