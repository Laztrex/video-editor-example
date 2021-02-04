import cv2


def mask_img(img1, flag=True):
    """
    слияние картинки и иконок
    :param img1: картинка
    :param icon: имя иконки
    :param mode: weather/part_day/degree - меняентся пространство наслоения
    :param part_day: подсмотр координат в зависимости от части суток
    :return: изображение с иконками
    """
    img2 = cv2.imread(img1)
    # brows, bcols = img1.shape[:2]
    # rows, cols, channels = img2.shape
    #
    # roi = img1[0:rows, bcols - rows:bcols]
    #
    # img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    # ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    # mask_inv = cv2.bitwise_not(mask)
    #
    # img1_bg = cv2.bitwise_and(roi, roi, mask=mask)
    # img2_fg = cv2.bitwise_and(img2, img2, mask=mask_inv)
    #
    # dst = cv2.add(img1_bg, img2_fg)
    # img2 = dst
    #
    #
    # img1[0:rows, bcols - rows:bcols] = img2

    gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    th, threshed = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)

    cnts, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = sorted(cnts, key=cv2.contourArea)[-1]

    x, y, w, h = cv2.boundingRect(cnt)
    dst = img2[y:y + h, x:x + w]
    cv2.imwrite("001.png", dst)

    # return img1
