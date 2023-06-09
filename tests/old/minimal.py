import os
import logging
from src import logger
import subprocess
import multiprocessing

logger = logging.getLogger(__name__)

def minimal_train_cpu(base_dir):
    # type: (str) -> None
    command = """ \
    content/marian/build/marian \
        --train-sets {base_dir}/train_gn.txt {base_dir}/train_es.txt \
        --model ./model.npz \
        --after-epochs 1 \
        --vocabs {base_dir}/gn_unique_tokens.txt {base_dir}/sp_unique_tokens.txt \
        --seed 1234 \
        --devices 0 \
        --cpu-threads 4 \
        --log model.log \
        --valid-log dev.log \
        --valid-sets {base_dir}/val_gn.txt {base_dir}/val_es.txt \
        --valid-metrics cross-entropy translation \
        --valid-script-path ./validate.sh \
        --overwrite
    """.format(base_dir=base_dir)
    os.system(command)

def minimal_evaluation_cpu(base_dir):
    # type: (str) -> None
    command = """ \
    content/marian/build/marian-decoder \
        --models ./model.npz \
        --vocabs {base_dir}/vocabulary/gn_unique_tokens.txt {base_dir}/vocabulary/sp_unique_tokens.txt \
        --input {base_dir}/test/test_gn.txt \
        --output test_es.txt \
        --beam-size 12 \
        --normalize 1 \
        --max-length 100 \
        --max-length-crop \
        --quiet-translation \
        --log test.log \
        --quiet
    """.format(base_dir=base_dir)
    os.system(command)

def minimal_train_gpu(marian_dir, corpus_dir):
    # type: (str, str) -> None
    # TODO: Arreglar direcciones para unirlas con os.path.join
    logger.info('Starting minimal_train_gpu with corpus_dir: {corpus_dir} and marian_dir: {marian_dir}'.format(corpus_dir=corpus_dir, marian_dir=marian_dir))
    command = """ \
        {marian_dir}/marian \
            --train-sets {corpus_dir}/train/train_gn.txt {corpus_dir}/train/train_es.txt \
            --model {marian_dir}/model.npz \
            --after-epochs 1 \
            --vocabs {corpus_dir}/vocabulary/gn_unique_tokens.txt {corpus_dir}/vocabulary/sp_unique_tokens.txt \
            --seed 1234 \
            --cpu-threads {cpu_count} \
            --devices 0 \
            --log model.log \
            --valid-log dev.log \
            --valid-sets {corpus_dir}/validation/val_gn.txt {corpus_dir}/validation/val_es.txt \
            --valid-metrics cross-entropy translation \
            --valid-script-path scripts/validate.sh \
            --overwrite
    """.format(marian_dir=marian_dir, corpus_dir=corpus_dir, cpu_count=multiprocessing.cpu_count())
    logger.info('Running command: {}'.format(command))
    result = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]
    logger.info('Finished minimal_train_gpu')
    logger.info('Process output: {}'.format(result))