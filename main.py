from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from deta import Deta
import uuid
from tinydb import TinyDB, Query
import io
import datetime
from PIL import Image
import pjsekai_background_gen_pillow as pjbg

app = Flask(__name__)
deta = Deta()
charts_db = deta.Base("charts")
charts = deta.Drive("charts")
jackets = deta.Drive("jackets")
audios = deta.Drive("audios")
level_data = deta.Base("level_data")
backgrounds = deta.Drive("backgrounds")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/post", methods=["POST"])
def post():
    # ５日実装
    if request.method == "POST":
        
        # get file chart_sus

        # get form data
        chart_title = request.form["chart_title"]
        music_info = request.form["music_info"]
        chart_author = request.form["chart_author"]
        chart_level = request.form["chart_level"]
        chart_rating = request.form["chart_rating"]
        chart_key = request.form["chart_key"]
        try:
            chart_path = request.form["chart_path"]
        except:
            chart_path = "%NORMAL%"
        try:
            chart_description = request.form["chart_description"]
        except:
            chart_description = "No description provided."
        try:
            chart_hidden = request.form["chart_hidden"]
            chart_hidden = True
        except:
            chart_hidden = False
        try:
            chart_public = request.form["chart_public"]
            chart_public = True
        except:
            chart_public = False
        chart_timestamp = datetime.datetime.now()
        # to str
        chart_timestamp = str(chart_timestamp)
        charts_db.put({
            "chart_title": chart_title,
            "music_info": music_info,
            "chart_author": chart_author,
            "chart_level": chart_level,
            "chart_rating": chart_rating,
            "chart_key": chart_key,
            "chart_path": chart_path,
            "chart_description": chart_description,
            "chart_hidden": chart_hidden,
            "chart_public": chart_public,
            "chart_timestamp": chart_timestamp
        })
        # get key from charts_db
        chart_id = charts_db.fetch({"chart_title": chart_title, "chart_key": chart_key}).items[0]["key"]
        # upload files
        upload_path = "charts/" + chart_id
        if chart_path:
            upload_path = upload_path + "/" + chart_path
        
        chart_sus = request.files["chart_sus"]
        chart_sus = io.BytesIO(chart_sus.read())
        chart_jacket = request.files["chart_jacket"]
        chart_jacket_raw = bytes(chart_jacket.read())
        generator = pjbg.Generator()
        background = io.BytesIO()
        image = io.BytesIO(chart_jacket_raw)
        generator.generate(Image.open(image)).save(background, format="PNG")
        backgrounds.put(chart_id + ".png", background)
        
        chart_jacket = io.BytesIO(chart_jacket.read())
        chart_audio = request.files["chart_audio"]
        chart_audio = io.BytesIO(chart_audio.read())

        charts.put(chart_id + ".sus", chart_sus)
        jackets.put(chart_id + ".png", chart_jacket)
        audios.put(chart_id + ".mp3", chart_audio)

        # convert jacket to background
    
        return render_template("done.html", chart_title=chart_title, music_info=music_info, chart_author=chart_author, chart_id=chart_id, chart_level=chart_level, chart_rating=chart_rating, chart_key=chart_key, chart_path=chart_path, chart_description=chart_description)

@app.route("/sonolus")
def sonolus():
    return "200 OK"

@app.route("/sonolus/info")
def sonolus_info():
    return send_file("assets/info.json")

@app.route("/sonolus/levels/list")
def sonolus_levels_list():
    # get page
    page = request.args.get("page")
    if page:
        page = int(page)
    else:
        page = 1
    # get 20 charts from db that are hot hidden and path is %NORMAL%
    charts = charts_db.fetch({"chart_hidden": False, "chart_public": True, "chart_path": "%NORMAL%"})
    charts = charts.items
    # get total pages
    total_pages = len(charts) // 20
    if len(charts) % 20 != 0:
        total_pages += 1
    # get charts for this page
    charts = charts[(page - 1) * 20:page * 20]
    # get level data
    level_list = {
        "items": [],
        "search": {
            "options": [
                {
                    "name": "#KEYWORDS",
                    "placeholder": "キーワード",
                    "query": "#KEYWORDS",
                    "type": "text"
                },
                {
                    "name": "#CHART_ID",
                    "placeholder": "譜面ID",
                    "query": "#CHART_ID",
                    "type": "text"
                },
                {
                    "name": "#KEY",
                    "placeholder": "<Key>",
                    "query": "#KEY",
                    "type": "text"
                },
                {
                    "name": "#PATH",
                    "placeholder": "パス",
                    "query": "#PATH",
                    "type": "text"

                }    
            ]
            },
            "pageCount": total_pages,
    }
    for chart in charts:
        level_list["items"].append({
            "name": "ptsl-" + chart["chart_id"],
            "title": chart["chart_title"],
            "artists": chart["music_info"],
            "author": chart["chart_author"],
            "cover": {
                "type": "LevelCover",
                "url": "/cover/" + chart["chart_id"]
            },
            "bgm": {
                "type": "LevelBgm",
                "url": "/audio/" + chart["chart_id"]
            },
            "preview": {
                "type": "LevelPreview",
                "url": "/preview/" + chart["chart_id"]
            },
            "data": {
                "type": "LevelData",
                "url": "/data/" + chart["chart_id"]
            },
            "rating": chart["chart_rating"],
            "version": 1,
            "useSkin": {
                "useDefault": true
            },
            "useBackground": {
                "useDefault": false,
                "item": {
                    "name": "ptsl-" + chart["chart_id"],
                    "version": 1,
                    "title": chart["chart_title"],
                    "subtitle": chart["music_info"],
                    "author": chart["chart_author"],
                    "thumbnail": {
                        "type": "BackgroundThumbnail",
                        "url": "/cover/" + chart["chart_id"]
                    },
                    "data": {
                        "url": "https://cc.sevenc7c.com/sonolus/assets/backgrounds/BackgroundData",
                        "type": "BackgroundData"
                    },
                    "image": {
                        "type": "BackgroundImage",
                        "url": "/background/" + chart["chart_id"]
                    },
                    "configuration": {
                        "hash": "d4367d5b719299e702ca26a2923ce5ef3235c1c7",
                        "url": "https://cc.sevenc7c.com/sonolus/assets/backgrounds/BackgroundConfiguration",
                        "type": "BackgroundConfiguration"
                    }
                }
            },
            "useEffect": {
                "useDefault": true
            },
            "useParticle": {
                "useDefault": true
            },
            "engine": {
                "author": "Nanashi. (Forked from Burrito)",
                "background": {
                    "name": "chcy-pjsekai",
                    "version": 2,
                    "title": "Live",
                    "subtitle": "プロジェクトセカイ カラフルステージ!",
                    "author": "Burrito",
                    "thumbnail": {
                        "hash": "bc97c960f8cb509ed17ebfe7f15bf2a089a98b90",
                        "url": "https://cc.sevenc7c.com/sonolus/assets/backgrounds/BackgroundThumbnail",
                        "type": "BackgroundThumbnail"
                    },
                    "data": {
                        "hash": "5e32e7fc235b0952da1b7aa0a03e7745e1a7b3d2",
                        "url": "https://cc.sevenc7c.com/sonolus/assets/backgrounds/BackgroundData",
                        "type": "BackgroundData"
                    },
                    "image": {
                        "hash": "8dd5a1d679ffdd22d109fca9ccef37272a4fc5db",
                        "url": "https://cc.sevenc7c.com/sonolus/assets/backgrounds/BackgroundImage",
                        "type": "BackgroundImage"
                    },
                    "configuration": {
                        "hash": "d4367d5b719299e702ca26a2923ce5ef3235c1c7",
                        "url": "https://cc.sevenc7c.com/sonolus/assets/backgrounds/BackgroundConfiguration",
                        "type": "BackgroundConfiguration"
                    }
                },
                "configuration": {
                    "hash": "967d362c11091d4e2c1b6e8fbac05bd517a6e25a",
                    "url": "https://cc.sevenc7c.com/sonolus/assets/engines/EngineConfiguration",
                    "type": "EngineConfiguration"
                },
                "data": {
                    "hash": "d0a1872bbce429119c533b6d4386662672f30c33",
                    "url": "https://cc.sevenc7c.com/sonolus/assets/engines/EngineData",
                    "type": "EngineData"
                },
                "name": "chcy-pjsekai-extended",
                "particle": {
                    "author": "Sonolus",
                    "data": {
                        "hash": "f84c5dead70ad62a00217589a73a07e7421818a8",
                        "url": "https://cc.sevenc7c.com/sonolus/assets/particles/ParticleData",
                        "type": "ParticleData"
                    },
                    "name": "chcy-pjsekai",
                    "subtitle": "From servers.sonolus.com/pjsekai",
                    "description": "Nothing changed.",
                    "texture": {
                        "hash": "57b4bd504f814150dea87b41f39c2c7a63f29518",
                        "url": "https://cc.sevenc7c.com/sonolus/assets/particles/ParticleTexture",
                        "type": "ParticleTexture"
                    },
                    "thumbnail": {
                        "hash": "e5f439916eac9bbd316276e20aed999993653560",
                        "url": "https://cc.sevenc7c.com/sonolus/assets/particles/ParticleThumbnail",
                        "type": "ParticleThumbnail"
                    },
                    "title": "PJSekai",
                    "version": 1
                },
                "skin": {
                    "author": "Sonolus + Nanashi.",
                    "data": {
                        "hash": "addf894d5a34951114d65ed97256d346793d7bab",
                        "url": "https://cc.sevenc7c.com/sonolus/assets/skins/SkinData",
                        "type": "SkinData"
                    },
                    "name": "chcy-pjsekai-extended",
                    "subtitle": "PJSekai Extended",
                    "description": "PjSekai + Trace notes",
                    "texture": {
                        "hash": "b17fa1472246825b43b822bd1a7f4fb4718864a1",
                        "url": "https://cc.sevenc7c.com/sonolus/assets/skins/SkinTexture",
                        "type": "SkinTexture"
                    },
                    "thumbnail": {
                        "hash": "24faf30cc2e0d0f51aeca3815ef523306b627289",
                        "url": "https://cc.sevenc7c.com/sonolus/assets/skins/SkinThumbnail",
                        "type": "SkinThumbnail"
                    },
                    "title": "PJSekai+",
                    "version": 2
                },
                "effect": {
                    "audio": {
                        "hash": "a22436b66b74c7f984a3209b170e78a544d15ed7",
                        "url": "https://cc.sevenc7c.com/sonolus/assets/effects/EffectAudio",
                        "type": "EffectAudio"
                    },
                    "author": "Sonolus",
                    "data": {
                        "hash": "92996df89e4cd349b763d04195cb3e9cd5b934ee",
                        "url": "https://cc.sevenc7c.com/sonolus/assets/effects/EffectData",
                        "type": "EffectData"
                    },
                    "name": "chcy-pjsekai-fixed",
                    "subtitle": "From servers.sonolus.com/pjsekai",
                    "description": "PJSekai + Trace notes",
                    "thumbnail": {
                        "hash": "e5f439916eac9bbd316276e20aed999993653560",
                        "url": "https://cc.sevenc7c.com/sonolus/assets/effects/EffectThumbnail",
                        "type": "EffectThumbnail"
                    },
                    "title": "PJSekai",
                    "version": 4
                },
                "description": "PJSekai + Trace notes, custom judgement, etc.",
                "subtitle": "From servers.sonolus.com/pjsekai",
                "thumbnail": {
                    "hash": "e5f439916eac9bbd316276e20aed999993653560",
                    "url": "https://cc.sevenc7c.com/sonolus/assets/engines/EngineThumbnail",
                    "type": "EngineThumbnail"
                },
                "title": "PJSekai+",
                "version": 7
            }
        },)





if __name__ == "__main__":
    app.run(debug=True)