from __future__ import annotations

import importlib.util
import inspect
import io
import sys
import tempfile
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path


class _CaptureResult:
    def __init__(self, out: str, err: str) -> None:
        self.out = out
        self.err = err


class _Capsys:
    def __init__(self) -> None:
        self._stdout = io.StringIO()
        self._stderr = io.StringIO()

    def __enter__(self):
        self._out_cm = redirect_stdout(self._stdout)
        self._err_cm = redirect_stderr(self._stderr)
        self._out_cm.__enter__()
        self._err_cm.__enter__()
        return self

    def __exit__(self, exc_type, exc, tb):
        self._err_cm.__exit__(exc_type, exc, tb)
        self._out_cm.__exit__(exc_type, exc, tb)

    def readouterr(self) -> _CaptureResult:
        result = _CaptureResult(self._stdout.getvalue(), self._stderr.getvalue())
        self._stdout = io.StringIO()
        self._stderr = io.StringIO()
        self._out_cm = redirect_stdout(self._stdout)
        self._err_cm = redirect_stderr(self._stderr)
        self._out_cm.__enter__()
        self._err_cm.__enter__()
        return result


def _load_module(path: Path, index: int):
    spec = importlib.util.spec_from_file_location(f"_test_module_{index}", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _run_test(func, module_path: Path):
    kwargs = {}
    capsys = None
    tmpdir = None
    for name in inspect.signature(func).parameters:
        if name == "capsys":
            capsys = _Capsys()
            kwargs[name] = capsys
        elif name == "tmp_path":
            tmpdir = tempfile.TemporaryDirectory()
            kwargs[name] = Path(tmpdir.name)
        else:
            raise TypeError(f"Unsupported fixture: {name}")

    if capsys is not None:
        capsys.__enter__()
    try:
        func(**kwargs)
    finally:
        if capsys is not None:
            capsys.__exit__(None, None, None)
        if tmpdir is not None:
            tmpdir.cleanup()


def main() -> int:
    args = [arg for arg in sys.argv[1:] if arg != "-q"]
    total = 0
    failed = 0
    root = Path.cwd()
    src = root / "src"
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    for index, arg in enumerate(args):
        path = Path(arg)
        module = _load_module(path, index)
        for name in dir(module):
            if not name.startswith("test_"):
                continue
            total += 1
            try:
                _run_test(getattr(module, name), path)
            except Exception as exc:
                failed += 1
                print(f"FAILED {path.name}::{name}: {exc}", file=sys.stderr)

    if failed:
        print(f"{failed} failed, {total - failed} passed")
        return 1
    print(f"{total} passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
