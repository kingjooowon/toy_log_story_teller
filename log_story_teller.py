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
    
    return int(status)

def analyze_log(path):
    url_result = {}
    status_result = {}
    
    for line in read_log(path):
        url = parse_url(line)
        status = parse_status(line)
        
        url_result[url] = url_result.get(url, 0) + 1
        status_result[status] = status_result.get(status, 0) + 1
        
    access_admin = "/admin" in url_result
    
    normal_count = sum(
        count for code, count in status_result.items()
        if int(code) < 400
    )
    
    error_status = {
        code: count
        for code, count in status_result.items()
        if code >= 400
    }
    
    total = sum(url_result.values())
    top_url = max(url_result, key=url_result.get) # type: ignore
    
    return {
        'total' : total,
        'top_url' : top_url,
        'top_url_count': url_result[top_url],
        'normal_count' : normal_count,
        'error_status' : error_status,
        'access_admin' : access_admin
    }

def generate_story(stats):
    print(f"총 {stats['total']}개의 요청이 있었습니다.\n")

    print(
        f"가장 많이 요청된 URL은 "
        f"{stats['top_url']} ({stats['top_url_count']}회) 입니다.\n"
    )

    print(f"정상 요청은 총 {stats['normal_count']}회였습니다.")

    if stats["error_status"]:
        print("\n에러가 감지되었습니다.")
        for code, count in stats["error_status"].items():
            if code == 403:
                reason = "권한 문제 가능성"
            elif code >= 500:
                reason = "서버 오류 가능성"
            else:
                reason = "기타 오류"

            print(f"- {code} 에러 {count}회 ({reason})")

    if stats["access_admin"]:
        print("\n관리자 페이지(/admin)에 대한 접근 시도가 있었습니다.")

if (__name__ == "__main__"):
    stats = analyze_log("sample.log")
    generate_story(stats)