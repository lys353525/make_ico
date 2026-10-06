import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image

class ImageToIcoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PNG/JPG to ICO 변환기")
        self.root.geometry("450x350")
        self.root.resizable(False, False)

        self.selected_file_path = None

        # 메인 레이아웃 설정
        self.setup_ui()

    def setup_ui(self):
        # 안내 문구
        title_label = tk.Label(
            self.root, 
            text="PNG / JPG 파일을 ICO로 변환", 
            font=("맑은 고딕", 14, "bold")
        )
        title_label.pack(pady=15)

        # 드래그 앤 드롭 영역 Frame (relief="solid"로 수정)
        self.drop_frame = tk.Frame(
            self.root, 
            relief="solid", 
            bd=1, 
            bg="#f8f9fa"
        )
        self.drop_frame.pack(fill="both", expand=True, padx=25, pady=10)

        # 드래그 앤 드롭 프레임 이벤트 연결
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.handle_drop)

        # 안내 텍스트
        self.drop_label = tk.Label(
            self.drop_frame,
            text="여기에 PNG 또는 JPG 파일을\n드래그 앤 드롭 하세요",
            font=("맑은 고딕", 11),
            bg="#f8f9fa",
            fg="#666666"
        )
        self.drop_label.pack(expand=True)

        # 변환 버튼
        self.convert_btn = tk.Button(
            self.root,
            text="ICO 파일로 변환 및 저장",
            font=("맑은 고딕", 11, "bold"),
            bg="#0078d4",
            fg="white",
            state="disabled",
            command=self.convert_and_save,
            padx=10,
            pady=5
        )
        self.convert_btn.pack(pady=15)

    def handle_drop(self, event):
        # 드래그 앤 드롭 경로 추출 (경로에 공백/중괄호 포함 대응)
        file_path = event.data.strip('{}')
        
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ['.png', '.jpg', '.jpeg']:
            self.selected_file_path = file_path
            filename = os.path.basename(file_path)
            self.drop_label.config(
                text=f"선택된 파일:\n{filename}", 
                fg="#0078d4"
            )
            self.convert_btn.config(state="normal")
        else:
            messagebox.showwarning("지원하지 않는 형식", "PNG 또는 JPG/JPEG 파일만 드롭할 수 있습니다.")

    def convert_and_save(self):
        if not self.selected_file_path:
            return

        # 원본 파일명에서 기본 이름 추출
        default_name = os.path.splitext(os.path.basename(self.selected_file_path))[0]

        # 저장 위치 및 파일명 입력 Dialog
        save_path = filedialog.asksaveasfilename(
            defaultextension=".ico",
            initialfile=f"{default_name}.ico",
            filetypes=[("ICO Icon File", "*.ico")],
            title="ICO 파일로 저장하기"
        )

        if save_path:
            try:
                # 이미지 열기 및 변환 (Windows 아이콘 표준 해상도들 포함)
                img = Image.open(self.selected_file_path)
                
                # 다양한 해상도가 포함된 표준 ICO 생성
                icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
                img.save(save_path, format='ICO', sizes=icon_sizes)

                messagebox.showinfo("성공", f"ICO 파일이 성공적으로 생성되었습니다!\n\n저장 경로:\n{save_path}")
            except Exception as e:
                messagebox.showerror("오류", f"변환 중 오류가 발생했습니다:\n{e}")

if __name__ == "__main__":
    # TkinterDnD 적용을 위한 root 생성
    root = TkinterDnD.Tk()
    app = ImageToIcoApp(root)
    root.mainloop()