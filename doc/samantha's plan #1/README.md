# web workflow summary

> AI feedback 을 활용한 웹 어플리케이션 맛보기

## Case 1. github / github actions/ aws

실무에서 가장 많이 사용하는 GitHub + GitHub Actions + 클라우드(AWS/Vercel 등) 조합을 기준으로 한 흐름

1. 설계 및 환경 설정 (Planning & Setup)

- 기술 스택 결정: 프레임워크(Express, NestJS, Next.js 중 선택), 데이터베이스(PostgreSQL, MongoDB 등), 패키지 매니저(npm, yarn, pnpm) 결정.
- 저장소 구성: GitHub/GitLab에 레포지토리를 생성하고 .gitignore 설정을 통해 불필요한 파일(node_modules, .env 등)이 업로드되지 않도록 합니다.

2. 로컬 개발 (Local Development)

- 환경 변수 관리: .env 파일을 통해 API 키나 DB 접속 정보를 관리합니다.
- 린트 & 포맷팅: ESLint와 Prettier를 설정해 코드 스타일을 통일합니다.
- 유닛 테스트: Jest나 Mocha를 이용해 주요 기능의 테스트 코드를 작성합니다.

3. 지속적 통합 (CI: Continuous Integration)개발자가 코드를 Push하면 자동으로 실행되는 단계입니다.

- 자동 빌드: Push된 코드가 Node.js 환경에서 정상적으로 빌드되는지 확인합니다.
- 자동 테스트: 작성된 테스트 코드를 실행하여 기존 기능이 망가지지 않았는지(Regression) 검사합니다.
- 코드 품질 검사: 린트 체크를 통과해야만 Merge가 가능하도록 제한합니다.

4. 지속적 배포 (CD: Continuous Deployment)CI를 통과한 코드를 실제 서버에 반영하는 단계입니다.

- 배포 방식 선택:
  - PaaS (Vercel, Render): 설정이 거의 필요 없고 Push 즉시 배포됩니다. (가장 쉬움)
  - Container (Docker): 애플리케이션을 이미지로 만들어 배포합니다. 환경 일관성이 높습니다.
- 무중단 배포: 새 버전이 실행될 때까지 구 버전을 유지하다가 교체하는 방식(Blue-Green 또는 Rolling Update)을 사용합니다.

5. 인프라 및 실행 관리 (Runtime Management)서버가 24시간 안정적으로 돌아가게 하는 관리 단계입니다.

- 프로세스 매니저 (PM2): 서버가 예상치 못한 오류로 죽었을 때 자동으로 재시작해주고, 로그를 관리합니다.
- 리버스 프록시 (Nginx): 보안 및 로드 밸런싱을 위해 Node.js 앱 앞에 배치합니다.

6. 모니터링 및 로깅 (Monitoring & Logging)서비스 운영 상태를 확인하는 단계입니다.

- 로깅: Winston이나 Pino 라이브러리로 서버 로그를 기록하고, 필요시 데이터독(Datadog)이나 ELK 스택으로 수집합니다.
- 에러 트래킹: Sentry 같은 도구를 연결해 사용자 브라우저나 서버에서 발생하는 에러를 실시간 알림으로 받습니다.

7. 유지보수 사이클 (Maintenance)

- 의존성 업데이트: npm audit으로 보안 취약점을 점검하고, Dependabot을 활용해 라이브러리 버전을 최신화합니다.
- 피드백 반영: 사용자 요구사항이나 버그 리포트를 바탕으로 다시 1단계로 돌아가 개발을 시작합니다.
