from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

router = APIRouter()


class FileContent(BaseModel):
    content: str


@router.get("/read_file_content/{file_path:path}", response_class=HTMLResponse)
async def read_file_content(file_path: str = ...):
    file_path_obj = Path(file_path)
    file_name = file_path_obj.name
    with open(file_path_obj, "r") as f:
        file_content = f.read()

    return HTMLResponse(
        """
        <html>
            <head>
                <title>Edit File - %s</title>
                <style>
                    body {
                        margin: 0;
                        padding: 0;
                        overflow: hidden;
                    }
                    #editor {
                        position: absolute;
                        top: 0;
                        right: 0;
                        bottom: 0;
                        left: 0;
                    }
                </style>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/ace.js"></script>
            </head>
            <body>
                <div id="editor">%s</div>
                <script>
                    var editor = ace.edit("editor");
                    editor.setTheme("ace/theme/monokai");
                    editor.getSession().setMode("ace/mode/text");
                    editor.getSession().setValue(`%s`);
                    editor.commands.addCommand({
                        name: 'save',
                        bindKey: {win: 'Ctrl-S', 'mac': 'Command-S'},
                        exec: function(editor) {
                            var content = editor.getValue();
                            var xhr = new XMLHttpRequest();
                            xhr.open('POST', '/save_file_content/%s', true);
                            xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
                            xhr.onload = function () {
                                if (xhr.readyState === xhr.DONE) {
                                    if (xhr.status === 200) {
                                        alert('File saved successfully!');
                                    } else {
                                        alert('Failed to save file!');
                                    }
                                }
                            };
                            xhr.send(JSON.stringify({content: content}));
                        }
                    });
                </script>
            </body>
        </html>
    """ % (file_name, file_content, file_content, file_path))


@router.post("/save_file_content/{file_path:path}")
async def save_file_content(file_path: str, file_content: FileContent):
    file_path_obj = Path(file_path)
    with open(file_path_obj, "w") as f:
        f.write(file_content.content)
    return {"message": "File saved successfully!"}
