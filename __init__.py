import datetime
import io
import json
from multiprocessing import Pool
import multiprocessing as mp
import zipfile
from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
import requests
from functools import partial

from config import *

app = FastAPI()

def get_Packs(ip):
    try:
        response = requests.get(f'http://{ip}/api/v1_0/packs_queue')
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return http_err
    except Exception as err:
        print(f'Other error occurred: {err}')
        return err
    else:
        responseJS = json.loads(response.content)
        return(len(responseJS))

def get_Mulps(ip):
    try:
        response = requests.get(f'http://{ip}/api/v1_0/multipacks_queue')
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return http_err
    except Exception as err:
        print(f'Other error occurred: {err}')
        return err
    else:
        responseJS = json.loads(response.content)
        return(len(responseJS))

def f(x,url):
    id = x['Monitor']['Id']
    print(id)
    response = requests.get(url + str(id))
    img = io.BytesIO(response.content)
    return((id,img))

@app.get("/get_images/{ip}",response_class=Response)
async def read_root(LineEnum: str):
    backIp = Backend[LineEnum].value
    zmIp = Zm[LineEnum].value
    url = f'http://{zmIp}/zm/cgi-bin/nph-zms?mode=single&monitor='
    zip_buffer = io.BytesIO()
    try:
        response = requests.get(f'http://{zmIp}/zm/api/monitors.json')
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
        if __name__ == '__init__':
            with Pool(mp.cpu_count()) as p:
                fotos = p.map(func, json.loads(response.content)['monitors'])
        # print(fotos)
        for file_name, file_object in fotos:
            zip_file.writestr(f"{file_name}.jpeg", file_object.getvalue())
        zip_file.writestr(f"status.txt", str(get_Packs(backIp)) + " / " + str(get_Mulps(backIp)))
        zip_file.close()
        return StreamingResponse(
            iter([zip_buffer.getvalue()]), 
            media_type="application/x-zip-compressed", 
            headers = { "Content-Disposition": f"attachment; filename={datetime.datetime.now()}.zip"}
        )
