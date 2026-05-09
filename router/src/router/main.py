from router.config import (
    INPUT_DIR,
    ACTION_DIR,
    LOCATION_DIR,
    SYMPTOM_DIR,
    MIXED_DIR,
    ETC_DIR,
    PENDING_FOLLOWUP_DIR,
    ACTION_FOLLOWUP_DIR,
    LOCATION_FOLLOWUP_DIR,
    SYMPTOM_FOLLOWUP_DIR,
    MIXED_FOLLOWUP_DIR,
    ETC_FOLLOWUP_DIR,
    POLL_INTERVAL,
    STABLE_WAIT,
    SKIP_EXISTING_ON_START,
)
from router.file_utils import ensure_dir
from router.watcher import RouterWatcher


def main() -> None:
    ensure_dir(INPUT_DIR)
    ensure_dir(ACTION_DIR)
    ensure_dir(LOCATION_DIR)
    ensure_dir(SYMPTOM_DIR)
    ensure_dir(MIXED_DIR)
    ensure_dir(ETC_DIR)
    ensure_dir(PENDING_FOLLOWUP_DIR)
    ensure_dir(ACTION_FOLLOWUP_DIR)
    ensure_dir(LOCATION_FOLLOWUP_DIR)
    ensure_dir(SYMPTOM_FOLLOWUP_DIR)
    ensure_dir(MIXED_FOLLOWUP_DIR)
    ensure_dir(ETC_FOLLOWUP_DIR)

    route_dirs = {
        "action": ACTION_DIR,
        "location": LOCATION_DIR,
        "symptom": SYMPTOM_DIR,
        "mixed": MIXED_DIR,
        "etc": ETC_DIR,
    }

    print()
    print("=" * 60)
    print("[INFO] router 패키지 시작")
    print(f"[INFO] 감시 폴더: {INPUT_DIR}")
    print("[INFO] 새 txt 파일이 생성되면 자동으로 분류합니다.")
    print("=" * 60)

    watcher = RouterWatcher(
        input_dir=INPUT_DIR,
        route_dirs=route_dirs,
        pending_followup_dir=PENDING_FOLLOWUP_DIR,
        action_followup_dir=ACTION_FOLLOWUP_DIR,
        location_followup_dir=LOCATION_FOLLOWUP_DIR,
        symptom_followup_dir=SYMPTOM_FOLLOWUP_DIR,
        mixed_followup_dir=MIXED_FOLLOWUP_DIR,
        etc_followup_dir=ETC_FOLLOWUP_DIR,
        poll_interval=POLL_INTERVAL,
        stable_wait=STABLE_WAIT,
        skip_existing_on_start=SKIP_EXISTING_ON_START,
    )
    watcher.run()


if __name__ == "__main__":
    main()
