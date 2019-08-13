from lfw import lfw_acquisition
from task import face_rec

import numpy
import time


URL = 'http://vis-www.cs.umass.edu/lfw/lfw.tgz'
MD5SUM = 'a17d05bd522c52d84eca14327a23d494'
PATH = '/svc/images'


if __name__ == "__main__":

    try:
        print("############################################################")
        print(f'{time.strftime("%b %d %Y %H:%M:%S:%s", time.localtime())} - Starting Producer Process...')
        dataset_list = lfw_acquisition(url=URL, md5sum=MD5SUM, path=PATH)

        print(f'{time.strftime("%b %d %Y %H:%M:%S:%s", time.localtime())} - Starting Creating Tasks...')
        results = []

        for data in dataset_list:
            results.append(face_rec.delay(image_path=data))

        total_tasks = len(results)
        
        print(f'{time.strftime("%b %d %Y %H:%M:%S:%s", time.localtime())} - Total of Tasks Created: {total_tasks}')
        print(f'{time.strftime("%b %d %Y %H:%M:%S:%s", time.localtime())} - Getting Tasks Done...')

        tasks_done = []

        while results:
            for index, query in enumerate(results):
                if query.ready():
                    tasks_done.append(query.get(timeout=3600))
                    del(results[index])
            time.sleep(0.1)

        total_tasks_done = len(tasks_done)

        print(f'{time.strftime("%b %d %Y %H:%M:%S:%s", time.localtime())} - Total of Tasks Finished: {total_tasks_done}')
        print(f'{time.strftime("%b %d %Y %H:%M:%S:%s", time.localtime())} - Calculating Average Vectors...')

        average = numpy.array(tasks_done[0][1])
        photos = []

        for done in tasks_done[1:]:
            if done[1] is not None:
                photos.append(done[0])
                average = (average + numpy.array(done[1])) / 2

        total_photos = len(photos)

        print(f'{time.strftime("%b %d %Y %H:%M:%S:%s", time.localtime())} - Total of Photos Processed: {total_photos}')
        print(f'{time.strftime("%b %d %Y %H:%M:%S:%s", time.localtime())} - Result of calculation the average of values:')
        print(f'{average}')
        print("############################################################")

        while True:
            time.sleep(1)

    except Exception as err:
        print('[FAIL] - ', err)
