import datetime
import io
import json
from multiprocessing import Pool
import multiprocessing as mp
import zipfile
import cv2
from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
import requests
from functools import partial
from PIL import Image

app = FastAPI()

def f(x,url):
    id = x['Monitor']['Id']
    print(id)
    cap = cv2.VideoCapture(url + str(id))
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(frame)
    file_object = io.BytesIO()
    im_pil.save(file_object, "PNG")
    im_pil.close()
    cap.release()
    return((id,file_object))

@app.get("/get_images/{ip}",response_class=Response)
async def read_root(ip: str):
    html_content = "<h2>Hello METANIT.COM!</h2>"
    url = f'http://{ip}/zm/cgi-bin/nph-zms?mode=jpeg&monitor='
    # zip = zipfile.ZipFile(str(datetime.datetime.now()), 'w')
    zip_buffer = io.BytesIO()
    try:
        response = requests.get(f'http://{ip}/zm/api/monitors.json')
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return http_err
    except Exception as err:
        print(f'Other error occurred: {err}')
        return err
    else:
        print('Success!')
        zip_buffer = io.BytesIO()
        zip_file = zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, True)
        func = partial(f, url = url)
        # zip_file.writestr(f"{id}.jpeg", file_object.getvalue())
        if __name__ == 'main':
            with Pool(mp.cpu_count()) as p:
                fotos = p.map(func, json.loads(response.content)['monitors'])
        print(fotos)
        for file_name, file_object in fotos:
            zip_file.writestr(f"{file_name}.jpeg", file_object.getvalue())
        zip_file.close()
        with open('1.zip', 'wb') as file:
            file.write(zip_buffer.getvalue())
        return StreamingResponse(
            iter([zip_buffer.getvalue()]), 
            media_type="application/x-zip-compressed", 
            headers = { "Content-Disposition": f"attachment; filename={datetime.datetime.now()}.zip"}
        )
