import time
from pathlib import Path
from typing import Set

from router.file_utils import (
    is_file_stable,
    read_text_file,
    write_text_file,
    move_file,
    read_json_file,
    delete_file,
)
from router.openai_router import OpenAIRouter


class RouterWatcher:
    def __init__(
        self,
        input_dir: Path,
        route_dirs: dict,
        pending_followup_dir: Path,
        action_followup_dir: Path,
        location_followup_dir: Path,
        symptom_followup_dir: Path,
        mixed_followup_dir: Path,
        etc_followup_dir: Path,
        poll_interval: float = 0.5,
        stable_wait: float = 0.2,
        skip_existing_on_start: bool = True,
    ) -> None:
        self.input_dir = input_dir
        self.route_dirs = route_dirs
        self.pending_followup_dir = pending_followup_dir
        self.action_followup_dir = action_followup_dir
        self.location_followup_dir = location_followup_dir
        self.symptom_followup_dir = symptom_followup_dir
        self.mixed_followup_dir = mixed_followup_dir
        self.etc_followup_dir = etc_followup_dir
        self.poll_interval = poll_interval
        self.stable_wait = stable_wait
        self.router = OpenAIRouter()
        self.seen: Set[str] = set()

        if skip_existing_on_start:
            for path in self.input_dir.glob("*.txt"):
                self.seen.add(path.name)

    def _print_block(self, filename: str, text: str, label: str) -> None:
        print()
        print("=" * 60)
        print(f"[ROUTER] 새 파일 감지: {filename}")
        print()
        print("[TEXT]")
        print(text if text else "(빈 파일)")
        print()
        print(f"[ROUTE] {label}")
        print("=" * 60)

    def _check_pending_followup(self):
        pending_path = self.pending_followup_dir / "current.json"
        if pending_path.exists():
            return pending_path
        return None

    def process_file(self, file_path: Path) -> None:
        if not is_file_stable(file_path, self.stable_wait):
            return

        try:
            text = read_text_file(file_path)

            pending_path = self._check_pending_followup()
            if pending_path is not None:
                pending = read_json_file(pending_path)
                category = pending.get("category", "")

                if category == "action":
                    target_name = pending.get("filename", file_path.name)
                    target_path = self.action_followup_dir / target_name
                    write_text_file(target_path, text)
                    delete_file(file_path)
                    delete_file(pending_path)
                    self._print_block(file_path.name, text, "action_followup")
                    return

                if category == "location":
                    target_name = pending.get("filename", file_path.name)
                    target_path = self.location_followup_dir / target_name
                    write_text_file(target_path, text)
                    delete_file(file_path)
                    delete_file(pending_path)
                    self._print_block(file_path.name, text, "location_followup")
                    return

                if category == "symptom":
                    target_name = pending.get("filename", file_path.name)
                    target_path = self.symptom_followup_dir / target_name
                    write_text_file(target_path, text)
                    delete_file(file_path)
                    delete_file(pending_path)
                    self._print_block(file_path.name, text, "symptom_followup")
                    return

                if category == "mixed":
                    target_name = pending.get("filename", file_path.name)
                    target_path = self.mixed_followup_dir / target_name
                    write_text_file(target_path, text)
                    delete_file(file_path)
                    delete_file(pending_path)
                    self._print_block(file_path.name, text, "mixed_followup")
                    return

                if category == "etc":
                    target_name = pending.get("filename", file_path.name)
                    target_path = self.etc_followup_dir / target_name
                    write_text_file(target_path, text)
                    delete_file(file_path)
                    delete_file(pending_path)
                    self._print_block(file_path.name, text, "etc_followup")
                    return

            label = self.router.classify(text)

            target_dir = self.route_dirs.get(label, self.route_dirs["etc"])
            move_file(file_path, target_dir)

            self._print_block(file_path.name, text, label)

        except Exception as e:
            print()
            print("=" * 60)
            print(f"[ERROR] router 처리 실패: {file_path.name}")
            print(e)
            print("=" * 60)

    def run(self) -> None:
        while True:
            try:
                txt_files = sorted(self.input_dir.glob("*.txt"))

                for file_path in txt_files:
                    if file_path.name in self.seen:
                        continue

                    self.seen.add(file_path.name)
                    self.process_file(file_path)

                time.sleep(self.poll_interval)

            except KeyboardInterrupt:
                break
            except Exception:
                time.sleep(self.poll_interval)
