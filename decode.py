from PIL import Image
import numpy as np
from pyzbar.pyzbar import decode as dc, ZBarSymbol
import imagehash
import cv2 as cv


class Detector:
    def __init__(self):
        pass

    @staticmethod
    def decode_and_detect(img):
        decode = dc(img, [ZBarSymbol.QRCODE] )
        print(decode)
        if len(decode)==0:
            print("没有检测到二维码！")
            return None, None
        else:
            decode = decode[0]
            # print(decode)
            # 解码出来的结果形如b'http://xxxxxxxxxx/xxxxx.jpg', 因此要去掉前后缀
            code = str(decode.data)[2:-1].split("/")[-1]
            rect = decode.rect
            img2 = img.crop(
                (rect.left, rect.top, rect.left + rect.width, rect.top + rect.height)
            )
            # img2.show()
            return code, img2

    def _haming_distance(self, x, y):
        '''海明距离'''
        if len(x) != len(y):
            print('length error!')
            return -1
        else:
            dis = 0
            for i in range(len(x)):
                if x[i] != y[i]:
                    dis += 1
            return dis

    def compare(self, img1, img2):
        '''img1,img2 -> a float between 0 and 1'''
        img1.convert("L")
        img2.convert("L")
        area1 = img1.size[0] * img1.size[1]
        area2 = img2.size[0] * img2.size[1]
        if area1 > area2:
            img1, img2 = img2, img1
        # 缩放至较小的图片规格
        img2 = img2.resize(img1.size)
        # print(img1.size, img2.size)

        # 直接相减比较
        area = img1.size[0] * img1.size[1]
        matrix1 = np.asarray(img1, dtype=np.uint8)
        matrix2 = np.asarray(img2, dtype=np.uint8)
        _, binary1 = cv.threshold(matrix1, 0, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)
        _, binary2 = cv.threshold(matrix2, 0, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)
        # cv.imshow("bin1", binary1)
        # cv.waitKey(0)
        sim1 = 1 - np.count_nonzero(binary1 - binary2) / area
        # print(sim1)

        # dhash比较
        h1 = str(imagehash.dhash(img1))
        h2 = str(imagehash.dhash(img2))
        h1 = bin(int(h1, 16))
        h2 = bin(int(h2, 16))
        h1 = str(h1)[2:]
        h2 = str(h2)[2:]
        diff = self._haming_distance(h1, h2)

        return (sim1 > 0.9) and (diff < 5)


if __name__ == "__main__":
    obj = Detector()
    img = Image.open("images/{154jelxbdg2d907122.jpg")  # .convert("L")  # L表示8位深灰度图像
    width, height = img.size
    # mat = np.asarray(img)[70: height*8//10,40:width*10//21]
    # img = Image.fromarray(mat)
    img.show()
    code, qr = obj.decode_and_detect(img)
    qr.show()
