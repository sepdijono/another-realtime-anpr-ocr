import easyocr
import re
import ujson
from fastapi import FastAPI, Request
import pickle
import base64

app = FastAPI()
reader = easyocr.Reader(['id'], gpu=True)


@app.post('/ocr')
async def ocr(info: Request):
    async def json2im(json_str):
        try:
            """Convert a JSON string back to a Numpy array"""
            load = ujson.loads(json_str)
            imdata = base64.b64decode(load['image'])
            im = pickle.loads(imdata)
            return im
        except Exception as e:
            return "ERROR"
        
    async def parse_tnk(tnk_reader):
        parse_nk = {}
        if len(tnk_reader) > 0:
            s = ""
            for i in tnk_reader:
                # s = s + ' ' + str(i[1]).capitalize()
                print(i, ' ')
            return parse_nk

        
    async def parse_1(tnk_reader):
        """Parsing easyocr.readtext with parameter details=0"""
        j = 0
        parse_nk = {}
        try:
            if tnk_reader is not None or tnk_reader != []:
                print(tnk_reader)
        except Exception as e:
            pass
        for i in tnk_reader:
            j += 1
            s = str(i)
            if len(s) > 0:
                if s.isnumeric():
                    parse_nk['prefix'] = ""
                    parse_nk['nk'] = s
                    parse_nk['suffix'] = ""
                    return parse_nk
                else:
                    try:
                        find_num = re.findall(r'\d+', s)[0]
                        if len(find_num) > 0 and (j == 1):
                            split_by_num = s.split(find_num)
                            if len(split_by_num) == 1:
                                parse_nk['prefix'] = split_by_num[0]
                                parse_nk['nk'] = find_num
                                parse_nk['suffix'] = ""
                                return parse_nk
                            elif len(split_by_num) >= 1:
                                parse_nk['prefix'] = split_by_num[0]
                                parse_nk['nk'] = find_num
                                parse_nk['suffix'] = split_by_num[1]
                                return parse_nk
                    except Exception as e:
                        parse_nk['prefix'] = ""
                        parse_nk['nk'] = ""
                        parse_nk['suffix'] = ""
                        return parse_nk
        
    try:
        req_info = await info.json()
        img = await json2im(req_info)
        read_tnk = reader.readtext(img, detail=0, batch_size=10, allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        r = await parse_1(read_tnk)
        print(r)
        return r
    except Exception as e:
        # print(e)
        return 'ERROR'

