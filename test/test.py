import sys

import unittest

import io

import torch
from PIL import Image
import main
app = main.app


class TestApi(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_postWithoutImage_returns_400(self):
        resp = self.app.post('/similar-images')
        self.assertEqual(400, resp.status_code)

    def test_img_1(self):
        with open("test_images/0b3f356651664968.jpg", "rb") as imageFile:
            image = Image.open(imageFile, mode='r')
            blob = io.BytesIO()
            image.save(blob, format=image.format)
            blob = blob.getvalue()

        resp = self.app.post(
            '/similar-images',
            data={
                'file': (io.BytesIO(blob), 'hello world.jpg'),
            }
        )
        self.assertEqual(200, resp.status_code)
        print(resp.data)

    def test_img_2(self):
        with open("test_images/0e63ad09dec7a9ec.jpg", "rb") as imageFile:
            image = Image.open(imageFile, mode='r')
            blob = io.BytesIO()
            image.save(blob, format=image.format)
            blob = blob.getvalue()

        resp = self.app.post(
            '/similar-images',
            data={
                'file': (io.BytesIO(blob), 'hello world.jpg'),
            }
        )
        self.assertEqual(200, resp.status_code)
        print(resp.data)

    def test_img_3(self):
        with open("test_images/4b84008217bde366.jpg", "rb") as imageFile:
            image = Image.open(imageFile, mode='r')
            blob = io.BytesIO()
            image.save(blob, format=image.format)
            blob = blob.getvalue()

        resp = self.app.post(
            '/similar-images',
            data={
                'file': (io.BytesIO(blob), 'hello world.jpg'),
            }
        )
        self.assertEqual(200, resp.status_code)
        print(resp.data)


if __name__ == "__main__":
    unittest.main()
