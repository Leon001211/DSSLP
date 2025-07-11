import os
from csv import reader
import wget
from multiprocessing import Pool, Value

dl_count = Value('i', 0)
wl_count = Value('i', 0)
data_source = "/SBU/dataset"

# correct:851000 wrong: 148957, 999957/1000000 finished

def image_dl(info):
    global dl_count, wl_count
    row_count = 1000000
    sub_dir = info.split('/')[-2]
    file_name = info.split('/')[-1]
    image_dir = os.path.join(data_source, sub_dir)
    image_path = os.path.join(image_dir, file_name)
    # if not correct download
    if os.path.exists(image_dir) and os.path.exists(image_path):
        with dl_count.get_lock():
            dl_count.value += 1
        return 1
    if not os.path.exists(image_dir):
        os.mkdir(image_dir)
    msg1 = ""
    try:
        wget.download(info, out=image_path)
        with dl_count.get_lock():
            dl_count.value += 1
    except IOError:
        msg1 = "image {} not found".format(info)
        with wl_count.get_lock():
            wl_count.value += 1
    # print(info[0], info[3])
    # video_dir
    if dl_count.value % 1000 == 0:
        print("\n")
        msg2 = "correct:{} wrong: {}, {}/{} finished".format(dl_count.value, wl_count.value, 
        dl_count.value+wl_count.value, row_count)
        print(msg2)
    # with open('webvid_data/download_logs.txt','a') as f:
    #     f.write(msg1 + "\n" + msg2)


# train / val dataset
urls = []
with open('/mnt/aiops/common/wangjp/SBU/SBU_captioned_photo_dataset_urls.txt', 'r') as fh:
    for line in fh:
        url = line.rstrip()
        urls.append(url)
print("{} imgs to be downloaded".format(len(urls)))

num_processes = 16
pool = Pool(num_processes)
pool.map(image_dl, tuple(list(urls)))