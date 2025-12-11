from __future__ import annotations

import os
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

try:
	from ref2dbc4CAN import write_dbc_file
except Exception:
	write_dbc_file = None  # type: ignore


# Optional drag-and-drop support (requires `pip install tkinterdnd2`).
try:
	from tkinterdnd2 import DND_FILES, TkinterDnD  # type: ignore

	HAVE_DND = True
except Exception:  # pragma: no cover - optional dependency
	TkinterDnD = None
	DND_FILES = ""
	HAVE_DND = False


def extract_hex_from_ref(path: str) -> str:
	data = Path(path).read_bytes()
	start = data.find(b"\x78\xda")
	if start == -1:
		raise ValueError("No '78 da' zlib header found in file")

	tail = data[start:]
	return " ".join(f"{b:02x}" for b in tail)


class RefToHexUI:
	def __init__(self) -> None:
		if HAVE_DND:
			self.root = TkinterDnD.Tk()
		else:
			self.root = tk.Tk()

		self.root.title("ref2dbc4CAN Converter")
		self.root.geometry("800x1000")

		self.hex_text: tk.Text | None = None
		self.current_hex: str = ""
		self._build_ui()

	def _build_ui(self) -> None:
		container = ttk.Frame(self.root, padding=10)
		container.pack(fill=tk.BOTH, expand=True)

		info = ttk.Label(
			container,
			text=(
				"Drop a .ref file or click Browse. "
				"The tool will keep bytes from the first '78 DA' onward, ignoring the header."
			),
			wraplength=760,
			justify=tk.LEFT,
		)
		info.pack(anchor=tk.W, pady=(0, 8))

		drop_style = {
			"relief": tk.RIDGE,
			"padding": 12,
			"width": 760,
		}
		self.drop_label = ttk.Label(container, text=self._drop_text(), **drop_style)
		self.drop_label.pack(fill=tk.X, pady=(0, 8))

		if HAVE_DND:
			self.drop_label.drop_target_register(DND_FILES)
			self.drop_label.dnd_bind("<<Drop>>", self._on_drop)

		btn_row = ttk.Frame(container)
		btn_row.pack(fill=tk.X, pady=(0, 8))

		ttk.Button(btn_row, text="Browse .ref", command=self._choose_file).pack(side=tk.LEFT)
		self.copy_btn = ttk.Button(btn_row, text="Copy hex", command=self._copy_hex, state=tk.DISABLED)
		self.copy_btn.pack(side=tk.LEFT, padx=6)
		self.save_btn = ttk.Button(btn_row, text="Save hex to file", command=self._save_hex, state=tk.DISABLED)
		self.save_btn.pack(side=tk.LEFT)
		self.dbc_btn = ttk.Button(btn_row, text="Convert to DBC", command=self._to_dbc, state=tk.DISABLED)
		self.dbc_btn.pack(side=tk.LEFT, padx=6)

		# Text widget with scrollbars for hex output
		text_frame = ttk.Frame(container)
		text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 8))

		self.hex_text = tk.Text(text_frame, height=18, wrap=tk.WORD)
		v_scroll = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.hex_text.yview)
		h_scroll = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL, command=self.hex_text.xview)
		self.hex_text.config(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

		self.hex_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
		h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

		self.status = ttk.Label(container, text="Ready", anchor=tk.W)
		self.status.pack(fill=tk.X, pady=(6, 0))

	def _drop_text(self) -> str:
		if HAVE_DND:
			return "Drop .ref file here"
		return "Drag-and-drop requires 'tkinterdnd2'. Click Browse to select a file."

	def _on_drop(self, event):  # type: ignore[override]
		path = event.data.strip()
		if path.startswith("{") and path.endswith("}"):
			path = path[1:-1]
		self._process_file(path)

	def _choose_file(self) -> None:
		path = filedialog.askopenfilename(
			title="Select .ref file",
			filetypes=[("REF files", "*.ref"), ("All files", "*.*")],
		)
		if path:
			self._process_file(path)

	def _process_file(self, path: str) -> None:
		try:
			hex_out = extract_hex_from_ref(path)
		except Exception as exc:  # noqa: BLE001
			messagebox.showerror("Error", str(exc))
			self._set_status(f"Failed: {exc}")
			return

		self.current_hex = hex_out
		if self.hex_text:
			self.hex_text.delete("1.0", tk.END)
			self.hex_text.insert(tk.END, hex_out)

		self.save_btn.config(state=tk.NORMAL)
		self.copy_btn.config(state=tk.NORMAL)
		self.dbc_btn.config(state=tk.NORMAL)
		self._set_status(f"Extracted from: {os.path.basename(path)}")

	def _copy_hex(self) -> None:
		if not self.current_hex:
			return
		try:
			self.root.clipboard_clear()
			self.root.clipboard_append(self.current_hex)
			self._set_status("Hex copied to clipboard")
		except Exception as exc:  # noqa: BLE001
			messagebox.showerror("Error", str(exc))
			self._set_status(f"Copy failed: {exc}")

	def _save_hex(self) -> None:
		if not self.current_hex:
			return
		out_path = filedialog.asksaveasfilename(
			title="Save hex text",
			defaultextension=".txt",
			filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
		)
		if not out_path:
			return
		Path(out_path).write_text(self.current_hex, encoding="utf-8")
		self._set_status(f"Saved to {out_path}")

	def _to_dbc(self) -> None:
		if not self.current_hex:
			return
		if write_dbc_file is None:
			messagebox.showerror("Error", "ref2dbc4CAN.py not importable; cannot convert to DBC.")
			return

		out_path = filedialog.asksaveasfilename(
			title="Save DBC file",
			defaultextension=".dbc",
			filetypes=[("DBC files", "*.dbc"), ("All files", "*.*")],
		)
		if not out_path:
			return
		try:
			write_dbc_file(self.current_hex, Path(out_path))
			self._set_status(f"DBC saved to {out_path}")
		except Exception as exc:  # noqa: BLE001
			messagebox.showerror("Error", str(exc))
			self._set_status(f"DBC conversion failed: {exc}")

	def _set_status(self, text: str) -> None:
		self.status.config(text=text)

	def run(self) -> None:
		self.root.mainloop()


def main() -> None:
	app = RefToHexUI()
	app.run()


if __name__ == "__main__":
	main()
