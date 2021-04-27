import os
import datetime
from notion.client import NotionClient
from notion.collection import NotionDate
import traceback

try:
    노션토큰 = os.environ.get('NOTION_TOKEN')
    if 노션토큰 is None:
        raise Exception("NOTION_TOKEN is not provided")
    
    업무일지주소 = os.environ.get('NOTION_WORKLOG_VIEW')
    if 업무일지주소 is None:
        업무일지주소 = "https://www.notion.so/torderkorea/581c105a40144fb9a8dcc760ab1eb250?v=2280f0536a1f490d87d4a144bb014565"

    이슈및작업주소 = os.environ.get('NOTION_WORKCARD_VIEW')
    if 이슈및작업주소 is None:
        이슈및작업주소 = "https://www.notion.so/torderkorea/76f444fd05064c1d93a609d4a0ec71ae?v=197851e600ca4d27926283f5fc81291f"

    업무일지제목 = os.environ.get('NOTION_WORKLOG_TITLE')
    if 업무일지제목 is None:
        업무일지제목 = datetime.datetime.now().strftime("%Y%m%d")


    노션 = NotionClient(token_v2=노션토큰)
    나 = 노션.get_user(
        list( 노션.get_email_uid().values() )[0]
    )
    
    print("[*] " + 나.full_name + " 업무일지 작성 시작")
        
    # 기존 업무일지 존재 확인
    오늘내일지들 = 노션.get_collection_view(업무일지주소).build_query(filter={
        "filters": [
            {
                "filter": {
                    "value": {
                        "type": "relative",
                        "value": "today"
                    },
                    "operator": "date_is",
                },
                "property": "jagseongilsi"
            },
            {
                "filter": {
                    "value": {
                        "type": "relative",
                        "value": "me"
                    },
                    "operator": "person_contains",
                },
                "property": "eobmuja"
            }
        ],
        "operator": "and"
    }).execute()
    
    if(len(오늘내일지들) == 0):
        print("[+] 기존 업무일지 없음, 업무일지 새로 생성")
        업무일지 = 노션.get_collection_view(업무일지주소).collection.add_row()
    else:
        print("[+] 기존 업무일지 존재, 해당 업무일지 갱신")
        업무일지 = 오늘내일지들[0]


    작성일시 = NotionDate(start=datetime.datetime.now().date())
    업무자 = 나
    오늘내작업들 = 노션.get_collection_view(이슈및작업주소).build_query(filter={
        "filters": [
            {
                "filter": {
                    "value": {
                        "type": "relative",
                        "value": "me"
                    },
                    "operator": "person_contains",
                },
                "property": "pilsu_damdangja"
            },
            {
                "filter": {
                    "value": {
                        "type": "exact",
                        "value": "오늘 진행중"
                    },
                    "operator": "enum_is",
                },
                "property": "pilsu_jinhaengsanghwang"
            }
        ],
        "operator": "and"
    }).execute()
                          
    
    업무일지.jagseongilsi = 작성일시
    업무일지.eobmuja = 업무자
    업무일지.title = 업무일지제목

    새로넣을작업들 = []
    for 오늘내작업 in 오늘내작업들:
        # 이미 들어가 있는 작업일 경우
        if(len(list(filter(lambda x: x.id == 오늘내작업.id, 업무일지.eobmugirog))) != 0):
            continue
        print("[+] 작업 추가: " + 오늘내작업.title)
        새로넣을작업들.append(오늘내작업)
    업무일지.eobmugirog = 업무일지.eobmugirog + 새로넣을작업들
    
    print("[*] " + 나.full_name + " 업무일지 작성 완료")
    
except:
    print("[-] " + 나.full_name + " 업무일지 작성 실패")
    traceback.print_exc()
