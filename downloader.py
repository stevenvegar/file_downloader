import requests, os, sys
from tqdm import tqdm
#sudo pip3 install clint
from pathlib import Path
import hashlib


def start_funct():
    if len(sys.argv) > 1:
        result = sys.argv[1]
    else:  
        result = False

    if result == False:
        print ("URL not defined...!!!")
        print ("Usage: python3 downloader.py URL_of_the_file_to_download")
        sys.exit()
    else:
        file_url = sys.argv[1]
        file_name = file_url.split('/')[-1]
        check_download(file_url,file_name)


def check_download(file_url,file_name):
    print ("Checking online file... Connecting...\n")
    try:
        s = requests.head(file_url,headers=custom_header)
        if s.status_code != 200:
            print ("File response status code: " +  str(s.status_code))
            print ("Invalid response code, check URL and file exist...!!!")
            sys.exit()
        else:
            print ("File response status code: " +  str(s.status_code))
            print ("Request headers: " + str(s.request.headers))
            print ("Response headers: " + str(s.headers))
            file_size_online = int(s.headers['Content-Length'])
            if "Accept-Ranges" not in s.headers:
                print ("CAUTION: Server doesn't provide chunked downloads...!!!")
            check_file(attempt_round,file_url,file_name,file_size_online)
    except requests.exceptions.MissingSchema as e:
        print ("Invalid URL of file doesn't exists...!!!")
        print ("Connection exception: " + str(e))
    except requests.exceptions.ConnectionError as e:
        print ("Connection error, please check...!!!")
        print ("Connection exception: " + str(e))


def check_file(attempt_round,file_url,file_name,file_size_online):
    file = Path('.') / file_name
    attempt_round = attempt_round + 1
    print ("\nOnline file size: " + str(round(file_size_online / 1048576,2)) + "MB")
    if file.exists():
        file_size_offline = file.stat().st_size
        print ("Local file size: " + str(round(file_size_offline / 1048576,2)) + "MB")
        print ("Local file: " + os.getcwd() + "/" + str(file))
        if file_size_online != file_size_offline:
            print ('File is incomplete. ' + str(round((file_size_online - file_size_offline) / 1048576,2)) + 'MB remaining. Resuming download...\n')
            downloader(attempt_round,file,file_url,file_name,file_size_online,file_size_offline)
        else:
            print ('File is complete. Skip download...')
            print ("MD5: " + md5_hashing(file))
            print ("SHA256: " + sha256_hashing(file) + '\n')
            pass
    else:
        print ('File does not exist. Starting to download it...\n')
        downloader(attempt_round,file,file_url,file_name,file_size_online)


def downloader(attempt_round,file,file_url,file_name,file_size_online,file_size_offline: int = None):
    block_size = 1024
    if file_size_offline:
        custom_header['Range'] = f'bytes={file_size_offline}-'
        mode = "ab"
        initial_pos = file_size_offline
    else:
        mode = "wb"
        initial_pos = 0
        
    try:
        with requests.get(file_url, stream=True, headers=custom_header, timeout=30) as r:
            print ("Download response status code: " + str(r.status_code))
            print ("Request headers: " + str(r.request.headers))
            print ("Response headers: " + str(r.headers) + "\n")
            print ("Attempt #" + str(attempt_round))
            with open(os.path.basename(file_name), mode) as output:
                with tqdm(total=file_size_online, unit='B',unit_scale=True, unit_divisor=block_size, desc=file_name, initial=initial_pos,ascii=True, miniters=1) as pbar:
                    for chunk in r.iter_content(128 * block_size):
                        output.write(chunk)
                        pbar.update(len(chunk))
                check_completition(attempt_round,file,file_url,file_name,file_size_online)
    except requests.exceptions.ConnectionError:
        check_completition(attempt_round,file,file_url,file_name,file_size_online)
    except Exception as e:
        print ("Request exception: " + str(e))


def check_completition(attempt_round,file,file_url,file_name,file_size_online):
    file_size_offline = file.stat().st_size
    if file_size_offline != file_size_online:
        check_file(attempt_round,file_url,file_name,file_size_online)
    else:
        print ('\nFile download is complete...')
        print ("MD5: " + md5_hashing(file))
        print ("SHA256: " + sha256_hashing(file) + '\n')
        sys.exit()


def md5_hashing(file):
    BLOCK_SIZE = 65536
    file_hash = hashlib.md5()
    with open(file, 'rb') as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(BLOCK_SIZE)
    return file_hash.hexdigest()

def sha256_hashing(file):
    BLOCK_SIZE = 65536
    file_hash = hashlib.sha256()
    with open(file, 'rb') as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(BLOCK_SIZE)
    return file_hash.hexdigest()


if __name__ == '__main__':
    custom_header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0"}
    attempt_round = 0
    start_funct()
