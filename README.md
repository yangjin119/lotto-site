# 🎰 6/45 Lotto 모의 운영 서비스 (Django & Docker)

Django와 Docker Multi-container 아키텍처를 기반으로 구축한 6/45 로또 복권 모의 운영 웹 서비스입니다. 일반 사용자의 복권 구매 및 당첨 확인 기능과 관리자의 판매 내역 확인 및 추첨 제어 기능을 제공합니다.

---

## 🛠️ 개발 환경 및 아키텍처
- **Web Framework:** Django 4.2 (Python 3.11-slim)
- **Database:** PostgreSQL 15 (Docker Volume 기반 데이터 보존)
- **Containerization:** Docker Compose (Multi-Container 환경 분리)

---

## 🚀 실행 방법 (Quick Start)

본 프로젝트는 Docker 환경이 구축되어 있다면 명령어 몇 줄로 즉시 구동이 가능합니다.

### 1. 저장소 복제 및 이동
```bash
git clone <본인의 GitHub 저장소 링크>
cd lotto-site