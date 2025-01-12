import time
import urllib.request
import urllib.error
import json
import os
import hashlib

class JSONDiskMap():
    def __init__(self, folder: str):
        self.folder = folder
        
        if os.path.exists(folder):
            if not os.path.isdir(folder):
                raise Exception(f"JSONDiskMap<{folder}> exists but is not a directory")
        else:
            os.mkdir(folder) 

    def __getitem__(self, key: str) -> dict:
        with open(f"{self.folder}/{key}.json", 'r') as file:
            data = json.load(file)
            return data

    def __setitem__(self, key: str, value: dict):
        with open(f"{self.folder}/{key}.json", 'w') as file:
            json.dump(value, file, indent=4)

    def __contains__(self, key: str) -> bool:
        return os.path.exists(f"{self.folder}/{key}.json")

    def __delitem__(self, key: str):
        retval = os.path.exists(f"{self.folder}/{key}.json")
        os.remove(f"{self.folder}/{key}.json")
        return retval

    def __iter__(self):
        files = os.listdir(self.folder)
        for file in files:
            yield self.__getitem__(file)

    def __len__(self):
        return len(os.listdir(self.folder))

default_disk_map = JSONDiskMap(".requestcache")

def get(url: str, cacheBust: bool = False, UserAgent: str = "VocabBuilder/1.0 (python)", Method: str = 'GET') -> dict:
    start_time = time.time()

    headers = {
        "User-Agent": UserAgent
    }

    request = urllib.request.Request(url, headers=headers, method=Method)

    h = hashlib.new('sha256')
    h.update(url.encode())
    h.update(UserAgent.encode())
    h.update(Method.encode())

    cache_key = h.hexdigest()


    def updateCache(response):
        stop_time = time.time()

        default_disk_map[cache_key] = {
            "request": {
                "url": url,
                "headers": headers,
                "method": Method
            },
            "response": response,
            "timing": {
                "start": start_time,
                "stop": stop_time,
                "duration_seconds": stop_time - start_time
            }
        }

    def resultFromCache(cache_key):
        cached = default_disk_map[cache_key]

        if cached == None:
            return None

        if cached["response"]["kind"] == "response":
            return json.loads(cached["response"]["data"])
        
        elif cached["response"]["kind"] == "HTTPError":
            raise urllib.error.HTTPError(url, cached["response"]["code"], cached["response"]["reason"], cached["response"]["headers"], None)
        
        elif cached["response"]["kind"] == "URLError":
            raise urllib.error.URLError(cached["response"]["reason"])
        
        elif cached["response"]["kind"] == "ContentTooShortError":
            raise urllib.error.ContentTooShortError(cached["response"]["data"])
        
        else:
            raise Exception(f"Unknown response kind: {cached['response']['kind']}")
    
    
    if not cacheBust:
        if cache_key in default_disk_map:
            return resultFromCache(cache_key)

    try:
        with urllib.request.urlopen(request) as response:
            data = response.read().decode()

            updateCache({
                "kind": "response",
                "status": response.status,
                "headers": response.getheaders(),
                "data": data
            })

    except urllib.error.HTTPError as e:
        updateCache({
            "kind": "HTTPError",
            "code": e.code,
            "reason": str(e.reason),
            "headers": e.getheaders(),
            "data": e.read().decode()
        })
    
    except urllib.error.URLError as e:
        updateCache({
            "kind": "URLError",
            "reason": str(e.reason)
        })
    

    except urllib.error.ContentTooShortError as e:
        updateCache({
            "kind": "ContentTooShortError",
            "data": e.content
        })

    except Exception as e:
        print(f"Failed to handle request to {url} for unknown reason: {e}")
        return None
    
    return resultFromCache(cache_key)
