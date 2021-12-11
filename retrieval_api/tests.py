import unittest

import main

application = main.application


class TestApi(unittest.TestCase):
    def setUp(self):
        self.application = application.test_client()
        self.application.testing = True
        self.resnet_ibn_gem_path = '/similar-images/resnet-ibn-gem'
        self.efficientnet_path = '/similar-images/efficientnet'

    def test_post_without_model_returns_404(self):
        response = self.application.post('/similar-images')
        self.assertEqual(404, response.status_code)
        self.assertEqual({
            'error': 'Not found'
        }, response.json)

    def test_post_without_image_returns_400(self):
        response = self.application.post(self.resnet_ibn_gem_path)
        self.assertEqual(400, response.status_code)
        self.assertEqual({
            'error': 'Missing image'
        }, response.json)

    def test_post_with_invalid_image_returns_400(self):
        response = self.application.post(self.resnet_ibn_gem_path, data={
            'file': open('labels.json', 'rb')
        })
        self.assertEqual(400, response.status_code)
        self.assertEqual({
            'error': 'Invalid image'
        }, response.json)

    def test_post_first_photo_with_resnet_ibn_gem_returns_200(self):
        response = self.application.post(self.resnet_ibn_gem_path, data={
            'file': open('images/0b3f356651664968.jpg', 'rb')
        })
        self.assertEqual(200, response.status_code)
        self.assertEqual(3, len(response.json))
        print(response.json)

    def test_post_first_photo_with_efficientnet_returns_200(self):
        response = self.application.post(self.efficientnet_path, data={
            'file': open('images/0b3f356651664968.jpg', 'rb')
        })
        self.assertEqual(200, response.status_code)
        self.assertEqual(3, len(response.json))
        print(response.json)

    def test_post_second_photo_with_resnet_ibn_gem_returns_200(self):
        response = self.application.post(self.resnet_ibn_gem_path, data={
            'file': open('images/0e63ad09dec7a9ec.jpg', 'rb')
        })
        self.assertEqual(200, response.status_code)
        self.assertEqual(3, len(response.json))
        print(response.json)

    def test_post_second_photo_with_efficientnet_returns_200(self):
        response = self.application.post(self.efficientnet_path, data={
            'file': open('images/0e63ad09dec7a9ec.jpg', 'rb')
        })
        self.assertEqual(200, response.status_code)
        print(response.json)

    def test_post_third_photo_with_resnet_ibn_gem_returns_200(self):
        response = self.application.post(self.resnet_ibn_gem_path, data={
            'file': open('images/4b84008217bde366.jpg', 'rb')
        })
        self.assertEqual(200, response.status_code)
        self.assertEqual(3, len(response.json))
        print(response.json)

    def test_post_third_photo_with_efficientnet_returns_200(self):
        response = self.application.post(self.efficientnet_path, data={
            'file': open('images/4b84008217bde366.jpg', 'rb')
        })
        self.assertEqual(200, response.status_code)
        self.assertEqual(3, len(response.json))
        print(response.json)

    def test_post_fourth_photo_with_resnet_ibn_gem_returns_200(self):
        response = self.application.post(self.resnet_ibn_gem_path, data={
            'file': open('images/palace_of_culture.jpg', 'rb')
        })
        self.assertEqual(200, response.status_code)
        self.assertEqual(3, len(response.json))
        print(response.json)

    def test_post_fourth_photo_with_efficientnet_returns_200(self):
        response = self.application.post(self.efficientnet_path, data={
            'file': open('images/palace_of_culture.jpg', 'rb')
        })
        self.assertEqual(200, response.status_code)
        self.assertEqual(3, len(response.json))
        print(response.json)


if __name__ == "__main__":
    unittest.main()
