# 베이스 이미지 설정
FROM public.ecr.aws/lambda/python:3.11

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 설치
RUN python3.11 -m pip install --upgrade pip


# Git 설치
RUN yum install -y git

#GitHub에서 코드 복사
RUN git clone https://github.com/Capstone-TeamGo/emotion-analyze-voice.git /app/
#로컬 pc
#COPY . /app

# 필요한 라이브러리 설치
# git으로 가져올떄
RUN pip install -r /app/emotion-analyze-voice/requirements.txt
# 로컬 pc
#RUN pip install -r /app/requirements.txt


# 실행 명령
# 로컬
CMD ["emotion_analysis.lambda_handler"]
