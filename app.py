from flask import Flask, request, jsonify
import requests
import random
import re # 정규표현식 라이브러리 (계산기 기능에 사용)
import psutil

app = Flask(__name__)

# 명언 목록 (랜덤 명언 기능용)
QUOTES = [
    "성공은 최종적인 것이 아니며, 실패는 치명적인 것이 아니다. 중요한 것은 계속하려는 용기이다. - 윈스턴 처칠",
    "인생은 용감한 모험이거나 아무것도 아니다. - 헬렌 켈러",
    "할 수 없다고 생각하는 것을 할 수 있게 될 때까지 해보면 결국 해낼 수 있다. - 마이클 조던",
    "오늘의 당신이 내일의 당신을 만든다. - 익명",
    "배움은 일종의 경험이다. 다른 모든 것은 단지 정보다. - 알베르트 아인슈타인"
]

# (이전 코드에서 사용된) 날씨 API 설정 - 실제 사용 시 반드시 키를 발급받아 대체해야 합니다.
# **1. 랜덤 명언 기능**
# -----------------------------------------------------
def get_random_quote():
    """랜덤으로 명언을 선택하여 반환"""
    return random.choice(QUOTES)

# -----------------------------------------------------
# **2. 간단 덧셈 계산기 기능**
# -----------------------------------------------------
def calculate_sum(expression):
    """
    "!계산 10 + 5"와 같은 형태의 문자열에서 덧셈을 수행
    """
    # [숫자] + [숫자] 형태를 정규표현식으로 찾습니다.
    # 예: "!계산 10 + 5" -> match (10, 5)
    match = re.search(r'(\d+)\s*\+\s*(\d+)', expression)
    
    if match:
        try:
            num1 = int(match.group(1))
            num2 = int(match.group(2))
            result = num1 + num2
            return f"**{num1} + {num2}**의 결과는 **{result}**입니다."
        except ValueError:
            return "숫자 형식 오류입니다. 정확히 입력해주세요. (예: !계산 10 + 5)"
    else:
        return "계산 형식이 올바르지 않습니다. (예: !계산 10 + 5)"

# -----------------------------------------------------
# **3. 배터리 조회 기능 (이전 코드와 동일)**
# -----------------------------------------------------
def b_sum():
    battery = psutil.sensors_battery()    
    if battery:
            # 배터리 잔량 (percent)
            percent = battery.percent
            return f"현재 배터리 잔량은 {percent}% 입니다."


# -----------------------------------------------------
# **메인 API 엔드포인트**
# -----------------------------------------------------
@app.route('/skill/v1', methods=['POST'])
def handle_skill_request():
    """
    카카오톡 오픈빌더의 모든 요청을 한 번에 처리하는 엔드포인트.
    오픈빌더의 스킬 설정에 이 URL을 등록해야 합니다.
    """
    req = request.get_json()
    user_utterance = req['userRequest']['utterance'].strip()
    
    # 기본 응답 메시지
    response_text = "이해하지 못했어요. '!날씨 서울', '!명언', 또는 '!계산 10 + 5'처럼 명령어를 입력해보세요."

    if user_utterance == '!명언':
        response_text = get_random_quote()   
    elif user_utterance.startswith('!계산'):
        response_text = calculate_sum(user_utterance)
    elif user_utterance.startswith('!배터리'):
        response_text = b_sum(user_utterance)
        
    # 카카오톡 응답 형식(SimpleText)에 맞게 JSON 생성
    response_body = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": response_text
                    }
                }
            ]
        }
    }
    
    return jsonify(response_body)
