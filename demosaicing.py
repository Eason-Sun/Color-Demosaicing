import numpy as np
import cv2

a = 199
b = 354
img = cv2.imread('toronto_original.png')

# cv2.imshow('Original Image', img)
rows, cols, channels = img.shape
cfaImg = np.empty(shape=(rows, cols, channels), dtype=np.uint8)
for x in range(0, rows):
    for y in range(0, cols):
        if x % 2 == 0:
            if y % 2 == 0:
                cfaImg[x][y][0] = img[x][y][0]
                cfaImg[x][y][1] = 0
                cfaImg[x][y][2] = 0

            else:
                cfaImg[x][y][0] = 0
                cfaImg[x][y][1] = img[x][y][1]
                cfaImg[x][y][2] = 0
        else:
            if y % 2 == 0:
                cfaImg[x][y][0] = 0
                cfaImg[x][y][1] = img[x][y][1]
                cfaImg[x][y][2] = 0
            else:
                cfaImg[x][y][0] = 0
                cfaImg[x][y][1] = 0
                cfaImg[x][y][2] = img[x][y][2]
# cv2.imshow('CFA Image', cv2.pyrUp(cfaImg))
cv2.imwrite('toronto_bayer.png', cfaImg)

BLACK = [0, 0, 0]
cfaImgPadding1 = cv2.copyMakeBorder(cfaImg, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=BLACK)
bilinearImg = np.empty(shape=(rows + 2, cols + 2, channels), dtype=np.uint8)

sum = 0
counter = 0
for x in range(1, rows + 1):
    for y in range(1, cols + 1):
        if x % 2 == 1:
            if y % 2 == 1:
                bilinearImg[x][y][0] = cfaImgPadding1[x][y][0]
                bilinearImg[x][y][1] = int(0.25 * (
                        int(cfaImgPadding1[x][y - 1][1]) + int(cfaImgPadding1[x][y + 1][1]) + int(
                    cfaImgPadding1[x - 1][y][1]) + int(cfaImgPadding1[x + 1][y][1])))
                bilinearImg[x][y][2] = int(0.25 * (
                        int(cfaImgPadding1[x - 1][y - 1][2]) + int(cfaImgPadding1[x - 1][y + 1][2]) + int(
                    cfaImgPadding1[x + 1][y - 1][2]) + int(cfaImgPadding1[x + 1][y + 1][2])))
            else:
                bilinearImg[x][y][0] = int(0.5 * (int(cfaImgPadding1[x][y - 1][0]) + int(cfaImgPadding1[x][y + 1][0])))
                bilinearImg[x][y][1] = cfaImgPadding1[x][y][1]
                bilinearImg[x][y][2] = int(0.5 * (int(cfaImgPadding1[x - 1][y][2]) + int(cfaImgPadding1[x + 1][y][2])))
        else:
            if y % 2 == 1:
                bilinearImg[x][y][0] = int(0.5 * (int(cfaImgPadding1[x - 1][y][0]) + int(cfaImgPadding1[x + 1][y][0])))
                bilinearImg[x][y][1] = cfaImgPadding1[x][y][1]
                bilinearImg[x][y][2] = int(0.5 * (int(cfaImgPadding1[x][y - 1][2]) + int(cfaImgPadding1[x][y + 1][2])))
            else:
                bilinearImg[x][y][0] = int(0.25 * (
                        int(cfaImgPadding1[x - 1][y - 1][0]) + int(cfaImgPadding1[x - 1][y + 1][0]) + int(
                    cfaImgPadding1[x + 1][y - 1][0]) + int(cfaImgPadding1[x + 1][y + 1][0])))
                bilinearImg[x][y][1] = int(0.25 * (
                        int(cfaImgPadding1[x][y - 1][1]) + int(cfaImgPadding1[x][y + 1][1]) + int(
                    cfaImgPadding1[x - 1][y][1]) + int(cfaImgPadding1[x + 1][y][1])))
                bilinearImg[x][y][2] = cfaImgPadding1[x][y][2]
        sum += abs(int(img[x - 1][y - 1][0]) - bilinearImg[x][y][0])
        counter += 1
        print(sum / counter)

cv2.imwrite('toronto_bilinear.png', bilinearImg)
#cv2.imshow('After Bilinear Interpolation', bilinearImg)
cv2.imshow('After Bilinear Interpolation', cv2.pyrUp(bilinearImg))

BLACK = [0, 0, 0]
cfaImgPadding2 = cv2.copyMakeBorder(cfaImg, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=BLACK)

gradientImg = np.empty(shape=(rows + 4, cols + 4, channels), dtype=np.uint8)

for x in range(2, rows + 2):
    for y in range(2, cols + 2):
        if x % 2 == 0:
            if y % 2 == 0:
                gradientImg[x][y][0] = cfaImgPadding2[x][y][0]
                deltaX = abs(int(cfaImgPadding2[x][y - 1][1]) - int(cfaImgPadding2[x][y + 1][1])) + abs(
                    2 * int(cfaImgPadding2[x][y][0]) - int(cfaImgPadding2[x][y - 2][0]) - int(
                        cfaImgPadding2[x][y + 2][0]))
                deltaY = abs(int(cfaImgPadding2[x - 1][y][1]) - int(cfaImgPadding2[x + 1][y][1])) + abs(
                    2 * int(cfaImgPadding2[x][y][0]) - int(cfaImgPadding2[x - 2][y][0]) - int(
                        cfaImgPadding2[x + 2][y][0]))
                if deltaX < deltaY:
                    gradientImg[x][y][1] = int(
                        0.5 * (int(cfaImgPadding2[x][y - 1][1]) + int(cfaImgPadding2[x][y + 1][1])) + 0.085 * (
                            2 * int(cfaImgPadding2[x][y][0]) - int(cfaImgPadding2[x][y - 2][0]) - int(
                        cfaImgPadding2[x][y + 2][0])))

                elif deltaX > deltaY:
                    gradientImg[x][y][1] = int(
                        0.5 * (int(cfaImgPadding2[x - 1][y][1]) + int(cfaImgPadding2[x + 1][y][1])) + 0.25 * (
                            2 * int(cfaImgPadding2[x][y][0]) - int(cfaImgPadding2[x - 2][y][0]) - int(
                        cfaImgPadding2[x + 2][y][0])))

                else:
                    gradientImg[x][y][1] = int(
                        0.25 * (int(cfaImgPadding2[x][y - 1][1]) + int(cfaImgPadding2[x][y + 1][1]) + int(
                            cfaImgPadding2[x - 1][y][1]) + int(cfaImgPadding2[x + 1][y][1])) + 0.125 * (
                            4 * int(cfaImgPadding2[x][y][0]) - int(cfaImgPadding2[x][y - 2][0]) - int(
                        cfaImgPadding2[x][y + 2][0]) - int(cfaImgPadding2[x - 2][y][0]) - int(
                        cfaImgPadding2[x + 2][y][0])))
            else:
                gradientImg[x][y][1] = cfaImgPadding2[x][y][1]


        else:
            if y % 2 == 0:
                gradientImg[x][y][1] = cfaImgPadding2[x][y][1]

            else:
                gradientImg[x][y][2] = cfaImgPadding2[x][y][2]
                deltaX = abs(int(cfaImgPadding2[x][y - 1][1]) - int(cfaImgPadding2[x][y + 1][1])) + abs(
                    2 * int(cfaImgPadding2[x][y][2]) - int(cfaImgPadding2[x][y - 2][2]) - int(
                        cfaImgPadding2[x][y + 2][2]))
                deltaY = abs(int(cfaImgPadding2[x - 1][y][1]) - int(cfaImgPadding2[x + 1][y][1])) + abs(
                    2 * int(cfaImgPadding2[x][y][2]) - int(cfaImgPadding2[x - 2][y][2]) - int(
                        cfaImgPadding2[x + 2][y][2]))

                if deltaX < deltaY:

                    gradientImg[x][y][1] = int(
                        0.5 * (int(cfaImgPadding2[x][y - 1][1]) + int(cfaImgPadding2[x][y + 1][1]))) + int(0.15 * (
                            2 * int(cfaImgPadding2[x][y][2]) - int(cfaImgPadding2[x][y - 2][2]) - int(
                        cfaImgPadding2[x][y + 2][2])))
                elif deltaX > deltaY:
                    gradientImg[x][y][1] = int(
                        0.5 * (int(cfaImgPadding2[x - 1][y][1]) + int(cfaImgPadding2[x + 1][y][1]))) + int(0.24 * (
                            2 * int(cfaImgPadding2[x][y][2]) - int(cfaImgPadding2[x - 2][y][2]) - int(
                        cfaImgPadding2[x + 2][y][2])))

                else:
                    gradientImg[x][y][1] = int(
                        0.25 * (int(cfaImgPadding2[x][y - 1][1]) + int(cfaImgPadding2[x][y + 1][1]) + int(
                            cfaImgPadding2[x - 1][y][1]) + int(cfaImgPadding2[x + 1][y][1]))) + int(0.125 * (
                            4 * int(cfaImgPadding2[x][y][2]) - int(cfaImgPadding2[x][y - 2][2]) - int(
                        cfaImgPadding2[x][y + 2][2]) - int(cfaImgPadding2[x - 2][y][2]) - int(
                        cfaImgPadding2[x + 2][y][2])))

#
# cv2.imshow('before Gradient Based Interpolation', cv2.pyrUp(gradientImg))
for x in range(2, rows + 2):
    for y in range(2, cols + 2):
        if x % 2 == 0:
            if y % 2 == 0:
                deltaX = abs(int(gradientImg[x - 1][y + 1][2]) - int(gradientImg[x + 1][y - 1][2])) + abs(
                    2 * int(gradientImg[x][y][1]) - int(gradientImg[x - 1][y + 1][1]) - int(
                        gradientImg[x + 1][y - 1][1]))
                deltaY = abs(int(gradientImg[x - 1][y - 1][2]) - int(gradientImg[x + 1][y + 1][2])) + abs(
                    2 * int(gradientImg[x][y][1]) - int(gradientImg[x - 1][y - 1][1]) - int(
                        gradientImg[x + 1][y + 1][1]))
                if deltaX < deltaY:
                    gradientImg[x][y][2] = int(
                        0.5 * (int(gradientImg[x - 1][y + 1][2]) + int(gradientImg[x + 1][y - 1][2])) +
                        0.445 * (2 * int(gradientImg[x][y][1]) - int(gradientImg[x - 1][y + 1][1]) - int(
                            gradientImg[x + 1][y - 1][1])))

                elif deltaX > deltaY:
                    gradientImg[x][y][2] = int(
                        0.5 * (int(gradientImg[x - 1][y - 1][2]) + int(gradientImg[x + 1][y + 1][2])) +
                        0.4 * (2 * int(gradientImg[x][y][1]) - int(gradientImg[x - 1][y - 1][1]) - int(
                            gradientImg[x + 1][y + 1][1])))
                else:
                    gradientImg[x][y][2] = int(0.25 * (
                            int(gradientImg[x - 1][y + 1][2]) + int(gradientImg[x + 1][y - 1][2]) + int(
                        gradientImg[x - 1][y - 1][2]) + int(gradientImg[x + 1][y + 1][2])) + 0.18 * (
                                                       4 * int(gradientImg[x][y][1]) - int(
                                                   gradientImg[x - 1][y + 1][1]) - int(
                                                   gradientImg[x + 1][y - 1][1]) - int(
                                                   gradientImg[x - 1][y - 1][1]) - int(
                                                   gradientImg[x + 1][y + 1][1])))
            else:
                gradientImg[x][y][0] = gradientImg[x][y][1] + int(0.5 * (
                        int(gradientImg[x][y - 1][0]) - int(gradientImg[x][y - 1][1]) + int(
                    gradientImg[x][y + 1][0]) - int(gradientImg[x][y + 1][1])))
                gradientImg[x][y][2] = gradientImg[x][y][1] + int(0.5 * (
                        int(gradientImg[x - 1][y][2]) - int(gradientImg[x - 1][y][1]) + int(
                    gradientImg[x + 1][y][2]) - int(gradientImg[x + 1][y][1])))
        # print(gradientImg[x][y], img[x-2][y-2])
        else:
            if y % 2 == 0:
                gradientImg[x][y][0] = gradientImg[x][y][1] + int(0.5 * (
                        int(gradientImg[x - 1][y][0]) - int(gradientImg[x - 1][y][1]) + int(
                    gradientImg[x + 1][y][0]) - int(gradientImg[x + 1][y][1])))

                gradientImg[x][y][2] = gradientImg[x][y][1] + int(0.51 * (
                        int(gradientImg[x][y - 1][2]) - int(gradientImg[x][y - 1][1]) + int(
                    gradientImg[x][y + 1][2]) - int(gradientImg[x][y + 1][1])))
            else:
                deltaX = abs(int(gradientImg[x - 1][y + 1][0]) - int(gradientImg[x + 1][y - 1][0])) + abs(
                    2 * int(gradientImg[x][y][1]) - int(gradientImg[x - 1][y + 1][1]) - int(
                        gradientImg[x + 1][y - 1][1]))
                deltaY = abs(int(gradientImg[x - 1][y - 1][0]) - int(gradientImg[x + 1][y + 1][0])) + abs(
                    2 * int(gradientImg[x][y][1]) - int(gradientImg[x - 1][y - 1][1]) - int(
                        gradientImg[x + 1][y + 1][1]))
                if deltaX < deltaY:
                    gradientImg[x][y][0] = int(
                        0.5 * (int(gradientImg[x - 1][y + 1][0]) + int(gradientImg[x + 1][y - 1][0])) +
                        0.5 * (2 * int(gradientImg[x][y][1]) - int(gradientImg[x - 1][y + 1][1]) - int(
                            gradientImg[x + 1][y - 1][1])))
                elif deltaX > deltaY:
                    gradientImg[x][y][0] = int(
                        0.5 * (int(gradientImg[x - 1][y - 1][0]) + int(gradientImg[x + 1][y + 1][0])) +
                        0.45 * (2 * int(gradientImg[x][y][1]) - int(gradientImg[x - 1][y - 1][1]) - int(
                            gradientImg[x + 1][y + 1][1])))
                else:
                    gradientImg[x][y][0] = int(0.25 * (
                            int(gradientImg[x - 1][y + 1][0]) + int(gradientImg[x + 1][y - 1][0]) + int(
                        gradientImg[x - 1][y - 1][0]) + int(gradientImg[x + 1][y + 1][0])) +
                        0.25 * (4 * int(gradientImg[x][y][1]) - int(gradientImg[x - 1][y + 1][1]) - int(
                            gradientImg[x + 1][y - 1][1]) - int(gradientImg[x - 1][y - 1][1]) - int(
                            gradientImg[x + 1][y + 1][1])))
        # sum += abs(int(img[x - 2][y - 2][0]) - gradientImg[x][y][0])
        # counter += 1
        # print(sum / counter)

# dst = cv2.fastNlMeansDenoisingColored(gradientImg,None,5,5,7,21)
cv2.imwrite('toronto_gradient.png', gradientImg)
cv2.imshow('After Gradient Based Interpolation', cv2.pyrUp(gradientImg))

cv2.waitKey(0)
cv2.destroyAllWindows()
