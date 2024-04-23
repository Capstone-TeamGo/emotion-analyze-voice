# 베이스 이미지 설정
FROM amazon/aws-lambda-python:3.8

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 설치
RUN /var/lang/bin/python3.8 -m pip install --upgrade pip

# Git 설치
RUN yum install -y git

# GitHub에서 코드 복사
RUN git clone https://github.com/Capstone-TeamGo/emotion-analyze-voice.git /app/

# 필요한 라이브러리 설치
RUN pip install -r /app/requirements.txt

# 실행 명령
CMD ["emotion_analysis.handler"]
