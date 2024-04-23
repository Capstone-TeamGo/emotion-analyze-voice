import json


# from simple_emotion_analysis import analyze_emotion

def lambda_handler(event, context):
    body = json.loads(event['body'])
    text = body.get('text', '')

    # 감정 분석
    score = analyze_emotion(text)

    # 결과 반환
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'feelingState': score})
    }


def analyze_emotion(text):
    # 실제 감정 분석 로직을 여기에 구현
    # 예시로 단순한 점수를 반환하도록 구현
    return 50
