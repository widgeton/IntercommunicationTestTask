import random as rnd

from fastapi import FastAPI, UploadFile

app = FastAPI()


@app.post('/process_image/')
async def process_image(image: UploadFile):
    top_left_x = rnd.randint(0, 630)
    top_left_y = rnd.randint(0, 630)
    width = rnd.randint(0, 640 - top_left_x)
    height = rnd.randint(0, 640 - top_left_y)
    conf = rnd.random()
    response = {'top_left_x': top_left_x, 'top_left_y': top_left_y, 'width': width,
                'height': height, 'conf': conf, 'label': 1}
    return rnd.choice([None, response])
