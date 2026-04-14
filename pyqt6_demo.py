import argparse
import os
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget


def build_window() -> QWidget:
    window = QWidget()
    window.setWindowTitle("PyQt6 Demo")

    label = QLabel("Привет! Это тестовое окно PyQt6")
    button = QPushButton("Нажми меня")

    def on_click() -> None:
        label.setText("Кнопка нажата ✅")

    button.clicked.connect(on_click)

    layout = QVBoxLayout()
    layout.addWidget(label)
    layout.addWidget(button)
    window.setLayout(layout)
    return window


def main() -> int:
    parser = argparse.ArgumentParser(description="Minimal PyQt6 demo app")
    parser.add_argument(
        "--screenshot",
        help="Path to save a screenshot after the window is rendered",
        default=None,
    )
    parser.add_argument(
        "--auto-quit-ms",
        type=int,
        default=2000,
        help="Automatically quit after N milliseconds (default: 2000)",
    )
    args = parser.parse_args()

    app = QApplication(sys.argv)
    window = build_window()

    print(f"QT_QPA_PLATFORM={os.environ.get('QT_QPA_PLATFORM', '<not set>')}")
    print("Starting PyQt6 demo app...")

    window.show()

    if args.screenshot:
        def capture() -> None:
            pixmap = window.grab()
            ok = pixmap.save(args.screenshot)
            print(f"Screenshot saved={ok} path={args.screenshot}")

        # Give Qt a brief moment to finish first paint before capture.
        QTimer.singleShot(200, capture)

    # Автовыход для headless/CI среды, чтобы команда не зависала.
    QTimer.singleShot(args.auto_quit_ms, app.quit)

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
