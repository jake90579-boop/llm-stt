from result.config import (
    ACTION_RESULT_DIR,
    LOCATION_RESULT_DIR,
    SYMPTOM_RESULT_DIR,
    MIXED_RESULT_DIR,
    ETC_RESULT_DIR,
    DONE_DIR,
    POLL_INTERVAL,
    STABLE_WAIT,
    SKIP_EXISTING_ON_START,
)
from result.file_utils import ensure_dir
from result.watcher import ResultWatcher


def main() -> None:
    ensure_dir(ACTION_RESULT_DIR)
    ensure_dir(LOCATION_RESULT_DIR)
    ensure_dir(SYMPTOM_RESULT_DIR)
    ensure_dir(MIXED_RESULT_DIR)
    ensure_dir(ETC_RESULT_DIR)
    ensure_dir(DONE_DIR)

    source_dirs = {
        "action": ACTION_RESULT_DIR,
        "location": LOCATION_RESULT_DIR,
        "symptom": SYMPTOM_RESULT_DIR,
        "mixed": MIXED_RESULT_DIR,
        "etc": ETC_RESULT_DIR,
    }

    print()
    print("=" * 60)
    print("[INFO] result 패키지 시작")
    print("[INFO] 최종 응답 result 폴더들을 감시합니다.")
    print("=" * 60)

    watcher = ResultWatcher(
        source_dirs=source_dirs,
        done_dir=DONE_DIR,
        poll_interval=POLL_INTERVAL,
        stable_wait=STABLE_WAIT,
        skip_existing_on_start=SKIP_EXISTING_ON_START,
    )
    watcher.run()


if __name__ == "__main__":
    main()
