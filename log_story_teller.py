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
    url_error_count = {}

    for line in read_log(path):
        url = parse_url(line)
        status = parse_status(line)

        url_result[url] = url_result.get(url, 0) + 1
        status_result[status] = status_result.get(status, 0) + 1

        if status >= 400:
            url_error_count[url] = url_error_count.get(url, 0) + 1

    total = sum(url_result.values())
    error_total = sum(
        count for code, count in status_result.items()
        if code >= 400
    )

    error_rate = round((error_total / total) * 100, 2)

    access_admin = "/admin" in url_result
    top_url = max(url_result, key=url_result.get) # type: ignore

    danger_url = None
    if url_error_count:
        danger_url = max(url_error_count, key=url_error_count.get) # type: ignore

    health_score = max(0, 100 - int(error_rate * 2))

    return {
        "total": total,
        "error_total": error_total,
        "error_rate": error_rate,
        "top_url": top_url,
        "top_url_count": url_result[top_url],
        "danger_url": danger_url,
        "danger_count": url_error_count.get(danger_url, 0),
        "health_score": health_score,
        "access_admin": access_admin,
        "status_result": status_result
    }

def generate_story(stats):
    print(f"총 {stats['total']}개의 요청이 있었습니다.\n")

    print(
        f"가장 많이 요청된 URL은 "
        f"{stats['top_url']} ({stats['top_url_count']}회) 입니다."
    )

    print(f"\n에러 요청은 {stats['error_total']}회로,")
    print(f"전체 요청 대비 에러율은 {stats['error_rate']}% 입니다.")

    if stats["error_rate"] >= 30:
        print("에러율이 높습니다. 시스템 점검이 필요합니다.")
    elif stats["error_rate"] >= 10:
        print("일부 에러가 감지되었습니다.")
    else:
        print("시스템 상태는 양호합니다.")

    if stats["danger_url"]:
        print(
            f"\n가장 많은 에러가 발생한 URL은 "
            f"{stats['danger_url']} "
            f"({stats['danger_count']}회) 입니다."
        )

    print(f"\nLog Health Score: {stats['health_score']} / 100")

    if stats["access_admin"]:
        print("\n관리자 페이지(/admin)에 대한 접근 시도가 있었습니다.")

if (__name__ == "__main__"):
    stats = analyze_log("sample.log")
    generate_story(stats)