"""train_dataset dataset."""
import os
import tensorflow_datasets as tfds

# TODO(train_dataset): Markdown description  that will appear on the catalog page.
_DESCRIPTION = """
Description is **formatted** as markdown.

It should also contain any processing which has been applied (if any),
(e.g. corrupted example skipped, images cropped,...):
"""

# TODO(train_dataset): BibTeX citation
_CITATION = """
"""



class TrainDataset(tfds.core.GeneratorBasedBuilder):
  """DatasetBuilder for train_dataset dataset."""

  VERSION = tfds.core.Version('1.0.2')
  RELEASE_NOTES = {
      '1.0.0': 'Initial release.',
  }

  MANUAL_DOWNLOAD_INSTRUCTIONS = 'Quando buildar, adicionar a flag --manual_dir=caminho_para_o_dataset'

  def _info(self) -> tfds.core.DatasetInfo:
    """Returns the dataset metadata."""
    # TODO(train_dataset): Specifies the tfds.core.DatasetInfo object
    return tfds.core.DatasetInfo(
        builder=self,
        description=_DESCRIPTION,
        features=tfds.features.FeaturesDict({
            # These are the features of your dataset like images, labels ...
            'image': tfds.features.Image(shape=(4608, 3456, 3)),
            'label': tfds.features.Image(shape=(4608, 3456, 3)),
        }),
        # If there's a common (input, target) tuple from the
        # features, specify them here. They'll be used if
        # `as_supervised=True` in `builder.as_dataset`.
        supervised_keys=('image', 'label'),  # Set to `None` to disable
        homepage='https://dataset-homepage/',
        citation=_CITATION,
    )

  def _split_generators(self, dl_manager: tfds.download.DownloadManager):

    dataset_path = "/home/jp/Documents/IC/Dataset/TrainTestSplit/dataset2.zip"
    # f = open("log", "w+")
    # f.write(str(dataset_path) + "\n")
    extracted_path = dl_manager.extract(dataset_path)
    # f.write(str(extracted_path / "Train/train_images"))
    # f.close()
    
    return {
      'train': self._generate_examples(
          images_path= extracted_path / "Train/train_images",
          label_path= extracted_path / "Train/train_segmentation",
      ),
      'test': self._generate_examples(
          images_path= extracted_path / "Validation/val_images",
          label_path= extracted_path / "Validation/val_segmentation",
      ),
    }

  def _generate_examples(self, images_path, label_path):
    # f = open("log", "w+")
    # f.write(str(images_path) + "\n")
    # f.close()
    # TODO(train_dataset): Yields (key, example) tuples from the dataset
    for data in images_path.glob('*.png'):
      yield data.name, {
          'image':  str(images_path) +"/"+ str(data.name),
          'label': str(label_path) +"/" +str(data.name),
      }
