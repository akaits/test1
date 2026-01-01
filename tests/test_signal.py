import pytest

import signal as signal_mod


def test_setup_prints(capsys):
    signal_mod.setup()
    captured = capsys.readouterr()
    assert "Set up" in captured.out


def test_cleanup_calls_sleep_and_prints(monkeypatch, capsys):
    calls = []

    def fake_sleep(n):
        calls.append(n)

    monkeypatch.setattr(signal_mod.time, "sleep", fake_sleep)
    signal_mod.cleanup()
    captured = capsys.readouterr()
    assert "Clean up Done" in captured.out
    assert calls == [10]


def test_sig_handler_exits_with_code_1():
    with pytest.raises(SystemExit) as exc:
        signal_mod.sig_handler(15, None)
    assert exc.value.code == 1
