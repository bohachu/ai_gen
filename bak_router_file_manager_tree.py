import json
import os
from pathlib import Path

from fastapi import APIRouter
from starlette.responses import HTMLResponse

router = APIRouter()


def get_file_tree(path: str) -> list:
    file_tree = []
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            file_tree.append({
                "text": item,
                "children": get_file_tree(full_path),
                "type": "folder"
            })
        else:
            file_tree.append({
                "text": item,
                "data": {"url": f"/read_file_content/{Path(full_path).as_posix()}"},
                "type": "file"
            })
    return file_tree


@router.get("/file_manager_tree", response_class=HTMLResponse)
async def file_manager_tree():
    file_tree = json.dumps(get_file_tree("./"))
    return f"""
        <html>
            <head>
                <title>File Manager</title>
                <style>
                    .jstree-default .jstree-icon {{
                        background-image: url("https://cdnjs.cloudflare.com/ajax/libs/jstree/3.3.12/themes/default/32px.png");
                    }}
                </style>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jstree/3.3.12/themes/default/style.min.css" />
                <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/jstree/3.3.12/jstree.min.js"></script>
                <script>
                    $(function() {{
                        var fileTree = {file_tree};
                        $("#jstree").jstree({{
                            "core": {{
                                "data": fileTree,
                                "dblclick_toggle": false
                            }},
                            "types": {{
                                "file": {{
                                    "icon": "jstree-file"
                                }},
                                "folder": {{
                                    "icon": "jstree-folder"
                                }}
                            }},
                            "plugins": ["types"]
                        }}).on("activate_node.jstree", function(e, data) {{
                            if (data.node.type === "file") {{
                                window.open(data.node.data.url, "_blank");
                            }} else {{
                                $("#jstree").jstree("toggle_node", data.node);
                            }}
                        }});
                    }});
                </script>
            </head>
            <body>
                <h1>File Manager</h1>
                <p>點擊一下即可展開或收合目錄結構，點擊檔案以查看內容。</p>
                <div id="jstree"></div>
            </body>
        </html>"""
