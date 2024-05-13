# 베이스 이미지 설정
FROM public.ecr.aws/lambda/python:3.11

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 설치
RUN python3.11 -m pip install --upgrade pip

#로컬 pc
COPY . /app

# 필요한 라이브러리 설치
# 로컬 pc
RUN pip install -r /app/requirements.txt


# 실행 명령
# 로컬
CMD ["emotion_analysis.lambda_handler"]
