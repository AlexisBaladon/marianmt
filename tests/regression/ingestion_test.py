import unittest
import os

from src.config.ingestion_config import get_data_ingestion_config
from src.components.data_ingestion import ingest_data
from src.components.processing.search_duplicates import search_duplicates

# TODO: Test if there are empty lines or the default vocabulary is not at the beginning of the file
class TestIngestion(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_ingestion(self):
        ingestion_config = get_data_ingestion_config()
        current_dir = os.path.dirname(os.path.realpath(__file__))
        test_data_dir = os.path.join(current_dir, '..', 'data')

        train_output_dir = os.path.join(test_data_dir, 'train.ingestion')
        validation_output_dir = os.path.join(test_data_dir, 'validation.ingestion')
        test_output_dir = os.path.join(test_data_dir, 'test.ingestion')
        vocab_output_dir = os.path.join(test_data_dir, 'vocab.ingestion')

        column_to_ingest = ingestion_config.raw_data_columns_to_clean[0]

        try:
            ingest_data(ingestion_config, [train_output_dir], [validation_output_dir], [test_output_dir], [vocab_output_dir], persist_each=100)
        except Exception as e:
            self.fail("Ingestion failed with exception {}".format(e))

        should_exist_paths = [train_output_dir, validation_output_dir, test_output_dir, vocab_output_dir]
        vocabulary_indexes = [should_exist_paths.index(vocab_output_dir)]
        should_exist_paths = [path + '.' + column_to_ingest for path in should_exist_paths]
        
        for path in should_exist_paths:
            if not os.path.exists(path):
                self.fail("Ingestion failed to create file {}".format(path))
            else:
                for index in vocabulary_indexes:
                    vocabulary_path = should_exist_paths[index]
                    _, duplicate_indexes = search_duplicates(vocabulary_path, verbose=False)
                    if len(duplicate_indexes.keys()) > 0:
                        self.fail("Ingestion created duplicate word in file {}".format(path))
                os.remove(path)

def main():
    unittest.main()

if __name__ == '__main__':
    main()