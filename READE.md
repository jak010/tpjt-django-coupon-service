# README.md

# Project Description

## Summary

tpjt-django-coupon-service는 FastCampus 강의를 참고로하여 Django 프레임워크를 기반으로 한 쿠폰 관리 시스템입니다.  
쿠폰 생성, 발급, 검증 기능을 수행하는 과정에서 동시성 제어, 트래픽 제어를 어떤 식으로 개선할 수 있는지를 다루기 위해 만들어졌습니다.

## Structure

```
tpjt-django-coupon-service/
├── .docker/             # Docker 관련 설정 파일
├── config/              # Django 설정 파일
├── contrib/             # 외부 패키지 또는 서드파티 연동
├── coupon/              # 쿠폰 관련 앱 (모델, 뷰, 시리얼라이저 등)
├── libs/                # 공통 라이브러리 및 유틸리티
├── tests/               # 테스트 코드
├── utils/               # 보조 유틸리티 함수
├── manage.py            # Django 관리 스크립트
├── requirements.txt     # 프로젝트 의존성 목록
├── makefile             # 자주 사용하는 명령어 모음
├── pytest.ini           # Pytest 설정 파일
└── conftest.py          # Pytest 설정 및 픽스처
```

## 주요 기능

- 쿠폰 생성 및 관리: 다양한 유형의 쿠폰을 생성하고 관리할 수 있습니다.
- 쿠폰 발급 및 사용: 사용자에게 쿠폰을 발급하고, 사용 여부를 추적할 수 있습니다.
- 쿠폰 검증: 쿠폰의 유효성 검사 및 사용 가능 여부를 확인할 수 있습니다.
- API 제공: RESTful API를 통해 외부 시스템과의 연동이 가능합니다.

