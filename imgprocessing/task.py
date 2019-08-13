from celery import Celery

import face_recognition


app = Celery('task',
             broker='amqp://imgprocessing:imgprocessing@rabbitmq:5672/imgprocessing',
             backend='amqp://imgprocessing:imgprocessing@rabbitmq:5672/imgprocessing')


@app.task(bind=True, autoretry_for=(Exception,), exponential_backoff=2,
          retry_kwargs={'max_retries': 5}, retry_jitter=False)
def face_rec(self, image_path):
    """
    Function to retry the vectors from a photo
    """
    photo = face_recognition.load_image_file(image_path)
    
    try:
        photo_encoding = list(face_recognition.face_encodings(photo)[0])
        return image_path, photo_encoding

    except IndexError:
        return image_path, None
