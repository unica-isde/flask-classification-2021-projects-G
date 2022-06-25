from ml.classification_utils import fetch_image


def generate(img_id):
    """! Generate histogram data

    @param img_id Id of the image to retrieve and analyze

    @return List of histogram data for RGB
    """
    img = fetch_image(img_id)
    r, g, b = img.split()
    img.close()

    results = [0]*3

    results[0] = r.histogram()
    results[1] = g.histogram()
    results[2] = b.histogram()

    return results

