from .social import (
    KakaoLoginAPI, KakaoCallbackAPI, GoogleLoginAPI, GoogleSignInAPI
)

kakao_login_view = KakaoLoginAPI.as_view()
kakao_callback_view = KakaoCallbackAPI.as_view()
google_login_view = GoogleLoginAPI.as_view()
google_sign_in_view = GoogleSignInAPI.as_view()
