from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PIL import Image, ImageEnhance, ImageOps

file = None
orig_file = None
angle = 0

def upd_effects(img):
    new_brgt = slider.value() / 100
    new_ctrt = slider2.value() / 100
    new_clr = slider3.value() / 100

    image_mod_b = ImageEnhance.Brightness(img)
    mid1_image = image_mod_b.enhance(new_brgt)

    image_mod_c = ImageEnhance.Contrast(mid1_image)
    mid2_image = image_mod_c.enhance(new_ctrt)

    image_mod_cl = ImageEnhance.Color(mid2_image)
    new_image = image_mod_cl.enhance(new_clr)
    return new_image

def img_update():
    global file
    if file is None:
        return

    display_img = upd_effects(file)
    show_img(display_img)

def show_img(img):
    rgba_img = img.convert("RGBA")
    data = rgba_img.tobytes("raw", "RGBA")
    q_img = QImage(data, rgba_img.size[0], rgba_img.size[1], QImage.Format_RGBA8888)

    pixmap = QPixmap.fromImage(q_img)
    image_label.setPixmap(pixmap)

def clear_effects():
    global file, orig_file
    if orig_file is None:
        return

    slider.blockSignals(True)
    slider2.blockSignals(True)
    slider3.blockSignals(True)

    slider.setValue(100)
    slider2.setValue(100)
    slider3.setValue(100)

    slider.blockSignals(False)
    slider2.blockSignals(False)
    slider3.blockSignals(False)

    file = orig_file.copy()
    show_img(file)

def open_file():
    global file, orig_file
    file_path, _ = QFileDialog.getOpenFileName(main_win, "Выберите файл", "", "Все файлы (*);;Изображения (*.png *.jpg *.jpeg);")
    if file_path:
        file = Image.open(file_path)
        orig_file = file.copy()
        print(file_path)
        img_update()

def save_file():
    global file, orig_file
    if file is not None:
        file_path, _ = QFileDialog.getSaveFileName(
            main_win, "Выберите путь", f"new_image.png", "Все файлы (*);;Изображения (*.png *.jpg *.jpeg);"
        )
        if file_path:
            final_image = upd_effects(file)
            final_image.save(file_path)
            print(f"Файл успешно сохранен: {file_path}")

def rotate_pic_l():
    global file, orig_file
    global angle
    if file is None:
        return

    file = file.rotate(-90, expand=True)
    orig_file = orig_file.rotate(-90, expand=True)

    img_update()

def rotate_pic_r():
    global file, orig_file
    global angle
    if file is None:
        return

    file = file.rotate(90, expand=True)
    orig_file = orig_file.rotate(90, expand=True)

    img_update()

def mirror_x():
    global file, orig_file
    if file is None:
        return

    file = file.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    orig_file = orig_file.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    img_update()

def mirror_y():
    global file, orig_file
    if file is None:
        return

    file = file.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    orig_file = orig_file.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    img_update()


app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Photozhop Beta')
main_win.setStyleSheet("background-color: #000000;")
main_win.resize(750, 600)

image_label = QLabel(main_win)

b_label = QLabel("B", main_win)
b_label.setGeometry(15, 452, 20, 40)
b_label.setStyleSheet("color: white; font-weight: bold; font-size: 21px")

c_label = QLabel("C", main_win)
c_label.setGeometry(15, 502, 20, 40)
c_label.setStyleSheet("color: white; font-weight: bold; font-size: 21px")

s_label = QLabel("S", main_win)
s_label.setGeometry(15, 552, 20, 40)
s_label.setStyleSheet("color: white; font-weight: bold; font-size: 21px")

slider = QSlider(Qt.Horizontal, main_win)
slider.setMinimum(0)
slider.setMaximum(200)
slider.setValue(100)

slider2 = QSlider(Qt.Horizontal, main_win)
slider2.setMinimum(0)
slider2.setMaximum(200)
slider2.setValue(100)

slider3 = QSlider(Qt.Horizontal, main_win)
slider3.setMinimum(0)
slider3.setMaximum(200)
slider3.setValue(100)

btn_open = QPushButton("Открыть картинку", main_win)
btn_open.setGeometry(525, 460, 190, 35)
btn_open.setStyleSheet("background-color: #34495e; color: white; font-weight: bold;")
btn_open.clicked.connect(open_file)

btn_save = QPushButton("Сохранить картинку", main_win)
btn_save.setGeometry(525, 510, 190, 35)
btn_save.setStyleSheet("background-color: #34495e; color: white; font-weight: bold;")
btn_save.clicked.connect(save_file)

btn_clear = QPushButton("Сбросить", main_win)
btn_clear.setGeometry(525, 560, 190, 35)
btn_clear.setStyleSheet("background-color: #34495e; color: white; font-weight: bold;")
btn_clear.clicked.connect(clear_effects)

btn_rr90 = QPushButton("<", main_win)
btn_rr90.setGeometry(330, 460, 35, 35)
btn_rr90.setStyleSheet("background-color: #34495e; color: white; font-weight: bold;")
btn_rr90.clicked.connect(rotate_pic_l)

btn_rl90 = QPushButton(">", main_win)
btn_rl90.setGeometry(330, 510, 35, 35)
btn_rl90.setStyleSheet("background-color: #34495e; color: white; font-weight: bold;")
btn_rl90.clicked.connect(rotate_pic_r)

btn_mrx = QPushButton("-", main_win)
btn_mrx.setGeometry(380, 460, 35, 35)
btn_mrx.setStyleSheet("background-color: #34495e; color: white; font-weight: bold;")
btn_mrx.clicked.connect(mirror_x)

btn_mry = QPushButton("|", main_win)
btn_mry.setGeometry(380, 510, 35, 35)
btn_mry.setStyleSheet("background-color: #34495e; color: white; font-weight: bold;")
btn_mry.clicked.connect(mirror_y)

image_label.setGeometry(0, 0, 750, 450)
image_label.setScaledContents(True)
slider.setGeometry(50, 460, 250, 30)
slider2.setGeometry(50, 510, 250, 30)
slider3.setGeometry(50, 560, 250, 30)


slider.valueChanged.connect(img_update)
slider2.valueChanged.connect(img_update)
slider3.valueChanged.connect(img_update)

main_win.show()
app.exec()
