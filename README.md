# notion-worklog-bot
업무일지 자동 작성/연결 봇

- 실행시 `오늘작업중` 에 있는 모든 작업카드를 기준으로 현재날짜의 업무일지를 작성
- 이미 업무일지가 존재할경우 새로운 작업카드만 알아서 추가

## 의존성 설치
```bash
python3 -m venv venv

source ./venv/bin/activate

pip install -r requirements.txt

deactivate
```

## 실행 방법
```bash
source ./venv/bin/activate

NOTION_TOKEN=노션로그인토큰 \            # https://minimin2.tistory.com/99#05cfe4a1-87e1-4edf-a903-66f3e7cdcac1 참조
NOTION_WORKLOG_TITLE=업무일지제목 \      # 생략시 YYYYMMDD 자동 기입
NOTION_WORKLOG_VIEW=노션업무일지URL \    # 생략가능
NOTION_WORKCARD_VIEW=노션작업및이슈URL \ # 생략가능
python bot.py

deactivate

```

