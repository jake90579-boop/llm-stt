import time
from pathlib import Path
from typing import Set, Dict

from result.file_utils import is_file_stable, read_text_file, move_file


class ResultWatcher:
    def __init__(
        self,
        source_dirs: Dict[str, Path],
        done_dir: Path,
        poll_interval: float = 0.5,
        stable_wait: float = 0.2,
        skip_existing_on_start: bool = True,
    ) -> None:
        self.source_dirs = source_dirs
        self.done_dir = done_dir
        self.poll_interval = poll_interval
        self.stable_wait = stable_wait
        self.seen: Set[str] = set()

        if skip_existing_on_start:
            for category, folder in self.source_dirs.items():
                for path in folder.glob("*.txt"):
                    key = f"{category}:{path.name}"
                    self.seen.add(key)

    def _print_block(self, category: str, filename: str, text: str) -> None:
        print()
        print("=" * 60)
        print(f"[RESULT] category: {category}")
        print(f"[FILE] {filename}")
        print()
        print("[FINAL ANSWER]")
        print(text if text else "(빈 응답)")
        print("=" * 60)

    def process_file(self, category: str, file_path: Path) -> None:
        if not is_file_stable(file_path, self.stable_wait):
            return

        try:
            text = read_text_file(file_path)
            self._print_block(category, file_path.name, text)
            move_file(file_path, self.done_dir / category)

        except Exception as e:
            print()
            print("=" * 60)
            print(f"[ERROR] result 처리 실패: {file_path.name}")
            print(e)
            print("=" * 60)

    def run(self) -> None:
        while True:
            try:
                for category, folder in self.source_dirs.items():
                    txt_files = sorted(folder.glob("*.txt"))

                    for file_path in txt_files:
                        key = f"{category}:{file_path.name}"
                        if key in self.seen:
                            continue

                        self.seen.add(key)
                        self.process_file(category, file_path)

                time.sleep(self.poll_interval)

            except KeyboardInterrupt:
                break
            except Exception:
                time.sleep(self.poll_interval)
