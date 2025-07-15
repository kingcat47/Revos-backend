# 구글에서 제공하는 id_token 검증용 모듈
from google.oauth2 import id_token

# 구글 인증서 다운로드 요청용 transport 객체
from google.auth.transport import requests

# 구글 토큰을 검증하고 사용자 정보를 반환하는 함수
def verify_google_token(token):
    try:
        # 구글의 공개키를 사용해 토큰을 검증하고 payload 추출
        idinfo = id_token.verify_oauth2_token(
            token,                           # 프론트에서 받은 id_token
            requests.Request(),              # HTTP 요청 객체
            audience='YOUR_GOOGLE_CLIENT_ID' # 구글 콘솔에서 발급받은 OAuth 2.0 Client ID
        )

        # 검증에 성공하면 사용자 정보를 담은 딕셔너리 반환
        return idinfo

    except Exception:
        # 검증 실패 시 None 반환 (예: 만료된 토큰, 위조된 토큰 등)
        return None
