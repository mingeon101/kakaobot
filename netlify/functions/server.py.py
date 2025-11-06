# app.py 파일에서 Flask 앱 인스턴스 'app'을 임포트합니다.
from app import app 

# serverless_wsgi 라이브러리에서 핸들러 생성 함수를 임포트합니다.
from serverless_wsgi import handle_request

# WSGI 앱 (Flask 앱)을 인수로 전달하여 서버리스 핸들러를 생성합니다.
def handler(event, context):
    # event와 context를 serverless_wsgi의 handle_request 함수로 전달합니다.
    # 이 함수가 Flask 앱을 실행하고 응답을 Lambda 형식으로 변환합니다.
    return handle_request(app, event, context)

# -----------------------------------------------------------------
# 주의: app.py 파일의 맨 아래에 있던 'if __name__ == "__main__":' 
# 로컬 실행 코드는 반드시 제거하거나 주석 처리해야 합니다.
# -----------------------------------------------------------------