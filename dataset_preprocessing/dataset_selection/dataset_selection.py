import os
import random
import shutil

import hydra
import pandas
from pandas import concat, DataFrame, read_csv


class DatasetSelection:
    def __init__(self, configurations):
        dataset_path = configurations.dataset_path
        self.dataset_folder_path = os.path.join(dataset_path, configurations.dataset_folder)
        self.labeled_samples_path = os.path.join(dataset_path, configurations.labeled_samples_file)
        self.clean_dataset_folder_path = os.path.join(dataset_path, configurations.clean_dataset_folder)
        self.training_folder_path = os.path.join(self.clean_dataset_folder_path, configurations.training_folder)
        self.validation_folder_path = os.path.join(self.clean_dataset_folder_path, configurations.validation_folder)
        self.testing_folder_path = os.path.join(self.clean_dataset_folder_path, configurations.testing_folder)
        self.application_folder_path = os.path.join(self.clean_dataset_folder_path, configurations.application_folder)

        self.percentage = configurations.percentage
        self.training_percentage = configurations.training_percentage
        self.validation_percentage = configurations.validation_percentage
        self.testing_percentage = configurations.testing_percentage

        self.image_map, self.landmark_map = None, None
        self.training_images, self.training_landmarks, self.validation_images, self.validation_landmarks, \
        self.testing_images, self.testing_landmarks = None, None, None, None, None, None

    def apply(self):
        self.create_maps()
        self.remove_landmarks_with_few_images()
        self.remove_excess_images()
        self.remove_images_without_landmark()
        self.create_folder(self.clean_dataset_folder_path)
        self.save_maps()
        self.split_dataset()
        self.save_splits()
        self.create_split_folders(self.training_folder_path, self.training_landmarks)
        self.create_split_folders(self.validation_folder_path, self.validation_landmarks)
        self.create_split_folders(self.testing_folder_path, self.testing_landmarks)
        self.save_dataset(self.training_images, self.training_landmarks, self.training_folder_path)
        self.save_dataset(self.validation_images, self.validation_landmarks, self.validation_folder_path)
        self.save_dataset(self.testing_images, self.testing_landmarks, self.testing_folder_path)
        self.save_application_dataset()

    def create_maps(self):
        self.image_map = read_csv(self.labeled_samples_path)
        self.image_map = self.image_map.rename(columns={"id": "image", "landmark_id": "landmark"})
        self.image_map = self.image_map[["image", "landmark"]]
        self.landmark_map = DataFrame(self.image_map.groupby(["landmark"])["image"].apply(list)).reset_index()
        self.landmark_map = self.landmark_map.rename(columns={"image": "images"})

    def remove_landmarks_with_few_images(self):
        self.landmark_map.drop(self.landmark_map[self.landmark_map["images"].map(len) < self.percentage * 3].index,
                               inplace=True)

    def get_selected_images(self, images):
        images_number = len(images) * self.percentage // 100
        return random.sample(images, images_number)

    def remove_excess_images(self):
        self.landmark_map["images"] = self.landmark_map["images"].apply(self.get_selected_images)

    def remove_images_without_landmark(self):
        self.image_map = self.landmark_map.explode("images")
        self.image_map = self.image_map.rename(columns={"images": "image"})

    @staticmethod
    def create_folder(path):
        if not os.path.exists(path):
            os.makedirs(path)

    def save_maps(self):
        self.image_map = self.image_map[["image", "landmark"]]
        self.image_map.to_csv(os.path.join(self.clean_dataset_folder_path, "images with landmarks.csv"), index=False,
                              mode="w+")
        self.landmark_map = self.landmark_map[["landmark", "images"]]
        self.landmark_map.to_csv(os.path.join(self.clean_dataset_folder_path, "landmarks with enough images.csv"),
                                 index=False, mode="w+")

    @staticmethod
    def get_splits(image_map, count, training_count, validation_count, testing_count):
        training_indexes = [first_index + second_index for first_index in range(0, image_map.shape[0], count)
                            for second_index in range(training_count)]
        validation_indexes = [first_index + second_index
                              for first_index in range(training_count, image_map.shape[0], count)
                              for second_index in range(validation_count)]
        testing_indexes = [first_index + second_index
                           for first_index in range(training_count + validation_count, image_map.shape[0], count)
                           for second_index in range(testing_count)]
        training_dataset = image_map.iloc[training_indexes]
        validation_dataset = image_map.iloc[validation_indexes]
        testing_dataset = image_map.iloc[testing_indexes]
        return training_dataset["image"], training_dataset["landmark"], validation_dataset["image"], \
               validation_dataset["landmark"], testing_dataset["image"], testing_dataset["landmark"]

    def split_dataset(self):
        splits = []
        for count in range(3, 11):
            image_map = self.image_map[self.image_map["landmark"]
                                           .map(self.image_map["landmark"].value_counts()) == count]
            splits += [self.get_splits(image_map, count, count - 2, 1, 1)]
        maximum_landmark_count = self.image_map["landmark"].value_counts().max()
        for count in range(11, maximum_landmark_count + 1):
            image_map = self.image_map[self.image_map["landmark"]
                                           .map(self.image_map["landmark"].value_counts()) == count]
            training_count = round(self.training_percentage * count)
            validation_count = round(self.validation_percentage * count)
            testing_count = count - training_count - validation_count
            splits += [self.get_splits(image_map, count, training_count, validation_count, testing_count)]
        self.training_images, self.training_landmarks, self.validation_images, self.validation_landmarks, \
        self.testing_images, self.testing_landmarks = [pandas.concat([split[second_index] for split in splits])
                                                       for second_index in range(6)]

    def save_splits(self):
        concat([self.training_images, self.training_landmarks], axis=1).to_csv(os.path.join(
            self.clean_dataset_folder_path, "training.csv"), index=False, mode="w+")
        concat([self.validation_images, self.validation_landmarks], axis=1).to_csv(os.path.join(
            self.clean_dataset_folder_path, "validation.csv"), index=False, mode="w+")
        concat([self.testing_images, self.testing_landmarks], axis=1).to_csv(os.path.join(
            self.clean_dataset_folder_path, "testing.csv"), index=False, mode="w+")

    def create_split_folders(self, path, landmarks):
        self.create_folder(path)
        for landmark in landmarks.unique():
            self.create_folder(os.path.join(path, str(landmark)))

    def save_dataset(self, images, landmarks, folder_path):
        index = 0
        for _, image in images.items():
            image += ".jpg"
            source_path = os.path.join(self.dataset_folder_path, image[0], image[1], image[2], image)
            destination_path = os.path.join(folder_path, str(landmarks.iloc[index]), image)
            shutil.copy(source_path, destination_path)
            index += 1

    def save_application_dataset(self):
        self.create_folder(self.application_folder_path)
        directories = [name for name in os.listdir(self.testing_folder_path)
                       if os.path.isdir(os.path.join(self.testing_folder_path, name))]
        for directory in directories:
            old_directory = os.path.join(self.testing_folder_path, directory)
            new_directory = os.path.join(self.application_folder_path, directory)
            self.create_folder(new_directory)
            files = [name for name in os.listdir(old_directory)
                     if os.path.isfile(os.path.join(old_directory, name))]
            for index, file in enumerate(random.sample(files, min(10, len(files)))):
                source_path = os.path.join(old_directory, file)
                destination_path = os.path.join(new_directory, str(index) + '.jpg')
                shutil.copy(source_path, destination_path)


@hydra.main(config_path="", config_name="dataset_selection_configurations")
def main(configurations):
    dataset_cleaning = DatasetSelection(configurations)
    dataset_cleaning.apply()


if __name__ == '__main__':
    main()
