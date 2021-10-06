import os
import unittest

from hydra import initialize, compose
from pandas import DataFrame

from dataset_cleaning import DatasetCleaning


class DatasetCleaningTests(unittest.TestCase):
    def setUp(self):
        with initialize(config_path=""):
            configurations = compose(config_name="dataset_cleaning_configurations")
            self.dataset_cleaning = DatasetCleaning(configurations)

    def test_when_create_maps_then_maps_should_be_not_none(self):
        # act
        self.dataset_cleaning.create_maps()

        # assert
        self.assertIsNotNone(self.dataset_cleaning.image_map)
        self.assertIsNotNone(self.dataset_cleaning.landmark_map)

    def test_when_create_maps_then_maps_should_be_data_frames(self):
        # act
        self.dataset_cleaning.create_maps()

        # assert
        self.assertIsInstance(self.dataset_cleaning.image_map, DataFrame)
        self.assertIsInstance(self.dataset_cleaning.landmark_map, DataFrame)

    def test_when_create_maps_then_maps_should_have_correct_columns(self):
        # act
        self.dataset_cleaning.create_maps()

        # assert
        self.assertListEqual(list(self.dataset_cleaning.image_map), ["image", "landmark"])
        self.assertListEqual(list(self.dataset_cleaning.landmark_map), ["landmark", "images"])

    def test_given_0_threshold_when_remove_landmarks_with_few_images_then_should_be_unchanged(self):
        # arrange
        with initialize(config_path=""):
            configurations = compose(config_name="dataset_cleaning_configurations",
                                     overrides=["threshold=0"])
            self.dataset_cleaning = DatasetCleaning(configurations)
        self.dataset_cleaning.create_maps()
        shape = self.dataset_cleaning.landmark_map.shape

        # act
        self.dataset_cleaning.remove_landmarks_with_few_images()

        # assert
        self.assertEqual(self.dataset_cleaning.landmark_map.shape, shape)

    def test_given_10_threshold_when_remove_landmarks_with_few_images_then_landmark_map_should_be_smaller(self):
        # arrange
        with initialize(config_path=""):
            configurations = compose(config_name="dataset_cleaning_configurations",
                                     overrides=["threshold=10"])
            self.dataset_cleaning = DatasetCleaning(configurations)
        self.dataset_cleaning.create_maps()
        landmarks = self.dataset_cleaning.landmark_map.shape[0]

        # act
        self.dataset_cleaning.remove_landmarks_with_few_images()

        # assert
        self.assertLess(self.dataset_cleaning.landmark_map.shape[0], landmarks)

    def test_when_create_clean_dataset_folder_then_should_exist(self):
        # act
        self.dataset_cleaning.create_folder(self.dataset_cleaning.clean_dataset_folder_path)

        # assert
        self.assertTrue(os.path.exists(self.dataset_cleaning.clean_dataset_folder_path))

    def test_given_clean_dataset_when_split_dataset_then_training_set_should_be_smaller(self):
        # arrange
        self.dataset_cleaning.create_maps()
        self.dataset_cleaning.remove_landmarks_with_few_images()
        self.dataset_cleaning.remove_images_without_landmark()
        images = self.dataset_cleaning.image_map.shape[0]

        # act
        self.dataset_cleaning.split_dataset()
        training_images_number = self.dataset_cleaning.training_images.shape[0]
        training_landmarks_number = self.dataset_cleaning.training_landmarks.shape[0]

        # assert
        self.assertEqual(training_images_number, training_landmarks_number)
        self.assertLess(training_images_number, images)

    def test_given_split_dataset_when_save_splits_then_files_should_exist(self):
        # arrange
        self.dataset_cleaning.create_maps()
        self.dataset_cleaning.remove_landmarks_with_few_images()
        self.dataset_cleaning.remove_images_without_landmark()
        self.dataset_cleaning.split_dataset()

        # act
        self.dataset_cleaning.save_splits()

        # assert
        self.assertTrue(os.path.exists(os.path.join(self.dataset_cleaning.clean_dataset_folder_path, "training.csv")))
        self.assertTrue(os.path.exists(os.path.join(self.dataset_cleaning.clean_dataset_folder_path,
                                                    "validation.csv")))
        self.assertTrue(os.path.exists(os.path.join(self.dataset_cleaning.clean_dataset_folder_path, "testing.csv")))


if __name__ == '__main__':
    unittest.main()
