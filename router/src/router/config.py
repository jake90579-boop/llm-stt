from pathlib import Path

MODEL_NAME = "gpt-4o-mini"

# STT 결과 txt 파일이 저장되는 폴더
INPUT_DIR = Path("/home/pc415-28/stt_package/stt/outputs")

# 분류 후 이동할 폴더
ACTION_DIR = Path("/home/pc415-28/llm_package/bus/action")
LOCATION_DIR = Path("/home/pc415-28/llm_package/bus/location")
SYMPTOM_DIR = Path("/home/pc415-28/llm_package/bus/symptom")
MIXED_DIR = Path("/home/pc415-28/llm_package/bus/mixed")
ETC_DIR = Path("/home/pc415-28/llm_package/bus/etc")

PENDING_FOLLOWUP_DIR = Path("/home/pc415-28/llm_package/bus/pending_followup")
ACTION_FOLLOWUP_DIR = Path("/home/pc415-28/llm_package/bus/action_followup")
LOCATION_FOLLOWUP_DIR = Path("/home/pc415-28/llm_package/bus/location_followup")
SYMPTOM_FOLLOWUP_DIR = Path("/home/pc415-28/llm_package/bus/symptom_followup")
MIXED_FOLLOWUP_DIR = Path("/home/pc415-28/llm_package/bus/mixed_followup")
ETC_FOLLOWUP_DIR = Path("/home/pc415-28/llm_package/bus/etc_followup")

POLL_INTERVAL = 0.5
STABLE_WAIT = 0.2
SKIP_EXISTING_ON_START = True

SYSTEM_PROMPT = """
너는 병원 안내 시스템의 라우터다.
사용자 입력 문장을 아래 다섯 가지 라벨 중 정확히 하나로만 분류하라.

라벨 정의:
- action: 사용자가 어떤 행동을 해야 하는지, 절차/방법/대처를 묻는 질문
- location: 특정 장소의 위치를 묻는 질문
- symptom: 사용자의 특정 증상, 통증, 몸 상태를 말하거나 묻는 질문
- mixed: 위 의도 둘 이상이 복합적으로 섞인 질문
- etc: 위 네 가지 어디에도 분명하게 속하지 않는 질문

반드시 아래 JSON 형식으로만 출력하라.
{"label":"location"}

허용 라벨:
action, location, symptom, mixed, etc

설명, 이유, 부가 문장, 마크다운은 절대 출력하지 마라.
"""
