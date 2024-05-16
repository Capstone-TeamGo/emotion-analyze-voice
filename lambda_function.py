import json
import base64
from transformers import BertTokenizer, BertForSequenceClassification
from faster_whisper import WhisperModel
import torch

# 음성 파일을 텍스트로 변환하고 해당 언어와 확률을 출력하는 함수
def transcribe_audio(audio_file):
    model_size = "small"
    model = WhisperModel(model_size, device="cpu", compute_type="int8") # run on CPU with INT8
    segments, info = model.transcribe(audio_file, beam_size=5)   # 음성 파일을 텍스트로 변환
    # print("Detected language '%s' with probability %f" % (info.language, info.language_probability)) # 해당 언어와 그 확률을 출력

    sentence = ""
    for segment in segments:
        sentence += segment.text + " "  # 각 세그먼트의 텍스트를 문자열에 추가

    return sentence

# 문장의 감정을 분석하고 확률을 반환하는 함수
def classify_sentence_with_prob(model, tokenizer, sentence):
    tokenized = tokenizer(sentence, padding=True, truncation=True, return_tensors="pt")   # 문장 토큰화 및 패딩
    with torch.no_grad(): # 모델을 사용하여 예측 수행
        outputs = model(**tokenized)

    probabilities = torch.softmax(outputs.logits, dim=1)[0] # 소프트맥스 함수를 통해 확률 계산
    labels = ["기쁨", "슬픔", "분노", "당황", "불안"] # 각 클래스에 대한 확률 출력

    # 예측 결과에서 가장 높은 확률을 가진 클래스 선택
    predicted_class = torch.argmax(probabilities).item()

    # 감정에 따른 점수화 진행
    if labels[predicted_class] == "슬픔":
        txt_score = int(70)
    elif labels[predicted_class] == "불안":
        txt_score = int(50)
    elif labels[predicted_class] == "분노":
        txt_score = int(40)
    elif labels[predicted_class] == "당황":
        txt_score = int(30)
    elif labels[predicted_class] == "기쁨":
        txt_score = int(0)

    return txt_score


# Lambda 핸들러 함수
def handler(event, context):
    body = event['body']  # HTTP 요청에서 body 추출

    # body가 base64로 인코딩되어 있을 경우 디코딩
    if event['isBase64Encoded']:
        body = base64.b64decode(body).decode('utf-8')

    # multipart/form-data 형식에서 파일 추출
    file_data = None
    for part in body.split('\r\n'):
        if 'name="file"' in part:
            file_data = part.split('\r\n\r\n')[1]
            break

    if file_data is None:
        return {
            'statusCode': 401,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                "message" : "파일이 존재하지 않습니다."
            })
        }

    # 음성 파일을 텍스트로 변환하고 언어 및 언어 확률을 가져옴
    audio_file = event['file']  # 음성 파일 경로 설정
    sentence = transcribe_audio(audio_file)


    # BERT 모델 로드 및 문장 감정 분류
    model_architecture = "kykim/bert-kor-base"
    model = BertForSequenceClassification.from_pretrained(model_architecture, num_labels=5)
    model_save_path = "/app/fine_tuned_model3.pt"  # 미리 학습된 모델 경로 설정
    model.load_state_dict(torch.load(model_save_path, map_location=torch.device('cpu')))
    tokenizer = BertTokenizer.from_pretrained(model_architecture)

    try:
        # 모델 호출
        txt_score = classify_sentence_with_prob(model, tokenizer, sentence)

        # 결과 반환
        response = {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'transcribedText': sentence,
                'feelingState': txt_score
            })
        }
        return response
    except Exception as e:
        # 모델 호출 중에 예외가 발생한 경우
        response = {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': 'Internal Server Error',
                'message': str(e)
            })
        }
        return response




