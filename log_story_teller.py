import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "sample.log")

def read_log(path):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            yield line.strip()
            
def parse_url(line):
    extract_middle = line.split('"')
    url = extract_middle[1].split()[1]
    
    return url

def parse_status(line):
    extract_middle = line.split('"')
    status = extract_middle[1].split()[2]
    
    return status

def analyze_log(path):
    access_admin = False
    url_result = {}
    status_result = {}
    for line in read_log(path):
        url = parse_url(line)
        status = parse_status(line)
        if url not in url_result:
            url_result[url] = 1
        else:
            url_result[url] += 1
            
        if status not in status_result:
            status_result[status] = 1
        else:
            status_result[status] += 1
            
    if ("/admin") in url_result:
        access_admin = True
    
    error = []
    normal = []
    for key in status_result:
        if int(key) >= 400:
            error.append(key)
        else:
            normal.append(key)
    
    total = sum(url_result.values())
    top_url = max(url_result, key=url_result.get) # type: ignore
    
            
    return {
        "total" : total,
        "top_url" : top_url,
        "url_result" : url_result,
        "status_result" : status_result,
        "error" : sorted(error),
        "normal" : normal,
        "access_admin" : access_admin
    }

def generate_story(stats):
    print(f"총 {stats['total']}개의 요청이 있었습니다.\n")
    print(f"가장 많이 요청된 URL은 {stats['top_url']} ({stats['url_result'][stats['top_url']]}회) 입니다.")
    print(f"정상 요청({stats['normal'][0]})은 {stats['status_result'][stats['normal'][0]]}회였습니다.\n")
    if stats['error'] != []:
        print("에러가 감지되었습니다.")
        print(f"- {stats['error'][0]} 에러 {stats['status_result'][stats['error'][0]]}회 (권환 문제 가능성)")
        print(f"- {stats['error'][1]} 에러 {stats['status_result'][stats['error'][1]]}회 (서버 오류 가능성)")
        
    if stats['access_admin'] == True:
        print("\n관리자 페이지 (/admin)에 대한 접근 시도가 있었습니다.")
    

if (__name__ == "__main__"):
    stats = analyze_log("sample.log")
    generate_story(stats)