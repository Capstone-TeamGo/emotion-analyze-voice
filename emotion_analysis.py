import json
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from faster_whisper import WhisperModel

# 음성 파일을 텍스트로 변환하고 해당 언어와 확률을 출력하는 함수
def transcribe_and_get_language_probability(audio_file):
    model_size = "small"
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_file, beam_size=5)
    detected_language = info.language
    language_probability = info.language_probability
    return segments, detected_language, language_probability

# 문장의 감정을 분석하고 확률을 반환하는 함수
def classify_sentence_with_prob(model, tokenizer, sentence):
    tokenized = tokenizer(sentence, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**tokenized)
    probabilities = torch.softmax(outputs.logits, dim=1)[0]
    labels = ["기쁨", "슬픔", "분노", "당황", "불안"]
    return labels, probabilities

# Lambda 핸들러 함수
def lambda_handler(event, context):
    # 음성 파일을 텍스트로 변환하고 언어 및 언어 확률을 가져옴
    audio_file = event['file']  # 음성 파일 경로 설정
    segments, detected_language, language_probability = transcribe_and_get_language_probability(audio_file)

    # 텍스트 생성
    sentence = ""
    for segment in segments:
        sentence += segment.text + " "

    # BERT 모델 로드 및 문장 감정 분류
    model_architecture = "kykim/bert-kor-base"
    model = BertForSequenceClassification.from_pretrained(model_architecture, num_labels=5)
    model_save_path = "fine_tuned_model3.pt"  # 미리 학습된 모델 경로 설정
    model.load_state_dict(torch.load(model_save_path, map_location=torch.device('cpu')))
    tokenizer = BertTokenizer.from_pretrained(model_architecture)
    labels, probabilities = classify_sentence_with_prob(model, tokenizer, sentence)

    # 가장 높은 확률의 감정 선택
    predicted_class = torch.argmax(probabilities).item()
    predicted_emotion = labels[predicted_class]

    # 결과 반환
    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            #'detectedLanguage': detected_language,
            #'languageProbability': language_probability,
            'transcribedText': sentence,
            'feelingState': predicted_emotion
        })
    }
    return response
