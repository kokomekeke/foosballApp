import cv2
import numpy as np


def posterize(img, n):
    indices = np.arange(0, 256)  # List of all colors

    divider = np.linspace(0, 255, n + 1)[1]  # we get a divider

    quantiz = np.int0(np.linspace(0, 255, n))  # we get quantization colors

    color_levels = np.clip(np.int0(indices / divider), 0, n - 1)  # color levels 0,1,2..

    palette = quantiz[color_levels]  # Creating the palette

    im2 = palette[img]  # Applying palette on image

    im2 = cv2.convertScaleAbs(im2)

    return im2


def noisy(noise_typ, image):
    if noise_typ == "gauss":
        row, col, ch = image.shape
        mean = 0
        var = 0.1
        sigma = var ** 0.5
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        noisy = image + gauss
        return noisy

    elif noise_typ == "s&p":
        row, col, ch = image.shape
        s_vs_p = 0.5
        amount = 0.004
        out = np.copy(image)

        # Salt mode
        num_salt = int(np.ceil(amount * image.size * s_vs_p))
        coords = [np.random.randint(0, i, num_salt) for i in image.shape]
        out[tuple(coords)] = 1

        # Pepper mode
        num_pepper = int(np.ceil(amount * image.size * (1. - s_vs_p)))
        coords = [np.random.randint(0, i, num_pepper) for i in image.shape]
        out[tuple(coords)] = 0

        return out

    elif noise_typ == "poisson":
        vals = len(np.unique(image))
        vals = 2 ** np.ceil(np.log2(vals))
        noisy = np.random.poisson(image * vals) / float(vals)
        return noisy

    elif noise_typ == "speckle":
        row, col, ch = image.shape
        gauss = np.random.randn(row, col, ch)
        noisy = image + image * gauss
        return noisy


def add_noise(img, noise_level=0.2):
    noisy_img = img.copy().astype(np.float32)

    noise = np.random.normal(0, 255 * noise_level, img.shape).astype(np.float32)

    noisy_img = np.clip(noisy_img + noise, 0, 255)

    return noisy_img.astype(np.uint8)


def sharpening(img):
    gaussian_blur = cv2.GaussianBlur(img, (7, 7), sigmaX=2)
    return cv2.addWeighted(img, 6.5, gaussian_blur, -5.5, 0)


def distortion(img, intensity=10):
    contrast_img = cv2.convertScaleAbs(img, alpha=intensity, beta=0)

    hsv = cv2.cvtColor(contrast_img, cv2.COLOR_RGB2HSV)
    hsv[:, :, 1] = cv2.add(hsv[:, :, 1], 30)

    if intensity > 1:
        hsv[:, :, 0] = (hsv[:, :, 0] + 50) % 180
    else:
        hsv[:, :, 0] = (hsv[:, :, 0] - 50) % 180

    distorted_img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return distorted_img


def enhance_brightness_and_saturation(image, brightness_increase=50, saturation_increase=50):
    # Átalakítás HSV színtérre
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Fényerő növelése
    hsv_img[:, :, 2] = np.clip(hsv_img[:, :, 2] + brightness_increase, 0, 255)

    # Szaturáció növelése
    hsv_img[:, :, 1] = np.clip(hsv_img[:, :, 1] + saturation_increase, 0, 255)

    # Vissza BGR színtérre
    enhanced_img = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)
    return enhanced_img


def thicken_edges(image, low_threshold=50, high_threshold=150, dilation_iterations=1):
    # Szürkeárnyalatú kép létrehozása
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Canny éldetektálás
    edges = cv2.Canny(gray_img, low_threshold, high_threshold)

    # Kontúrok vastagítása dilate művelettel
    kernel = np.ones((3, 3), np.uint8)  # 3x3 kernel a vastagításhoz
    thick_edges = cv2.dilate(edges, kernel, iterations=dilation_iterations)

    # Kontúrok rávetítése az eredeti képre
    thick_edges_colored = cv2.cvtColor(thick_edges, cv2.COLOR_GRAY2BGR)  # Szürkeárnyalatból BGR-be
    enhanced_image = cv2.bitwise_or(image, thick_edges_colored)

    return enhanced_image


def process_image(im):
    n = 8

    im2 = posterize(im, n)

    im2 = cv2.convertScaleAbs(im2, alpha=1.5)
    im2 = cv2.convertScaleAbs(im2, beta=-10)

    im2 = noisy("s&p", im2)

    im2 = sharpening(im2)

    # im2 = distortion(im2, 10)

    im2 = add_noise(im2, 0.01)

    im2 = enhance_brightness_and_saturation(im2, -10, -1)

    im2 = thicken_edges(im2, 20, 13000)

    return im2
