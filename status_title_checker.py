import requests
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time
import sys


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def requete(url):
    try:
        req = requests.get(url)

        # change encode for display
        if req.encoding == 'ISO-8859-1':
            encodings = requests.utils.get_encodings_from_content(req.text)
            # print(encodings)
            if encodings:
                encoding = encodings[0]
            else:
                encoding = req.apparent_encoding
            #     # global encode_content
            encode_content = req.content.decode(encoding, 'replace')
        # print(encode_content)

        title_rule = re.compile(r'(?<=\<title\>)(?:.|\n)+?(?=\<)')
        title_result = title_rule.findall(encode_content)
        # print(title_result)
        # return url, r.status_code
        # print(req.status_code, title_result)
        return url, req.status_code, title_result
    except:
        pass


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print
        "Usage: ./" + sys.argv[0] + " [URL list] "
        sys.exit(1)

url_list = [line.rstrip('\n') for line in open(sys.argv[1])]

start = time()

processes = []
with ThreadPoolExecutor(max_workers=10) as executor:
    for url in url_list:
        processes.append(executor.submit(requete, url))

    for task in as_completed(processes):
        if task.result() is not None:
            url, status_code, title = task.result()
            print("{}".format(url) + bcolors.OKGREEN + " - {}".format(status_code) + bcolors.ENDC + " - {}".format(title) + bcolors.ENDC)
