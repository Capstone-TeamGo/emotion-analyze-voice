# 베이스 이미지 설정
FROM public.ecr.aws/lambda/python:3.11

# 작업 디렉토리 설정
WORKDIR ${LAMBDA_TASK_ROOT}

# 필요한 패키지 설치
# RUN python3.11 -m pip install --upgrade pip

#로컬 pc
COPY fine_tuned_model3.pt .
COPY lambda_function.py .
COPY requirements.txt .

# 필요한 라이브러리 설치
# 로컬 pc
RUN pip install --no-cache-dir -r requirements.txt

# 실행 명령
# 로컬
CMD ["lambda_function.handler"]
