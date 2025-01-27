# coding=utf-8
# Copyright 2018 The Google AI Language Team Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# this script bears slight modifications from the original source code; 
# the original source code is available at https://github.com/google-research-datasets/natural-questions/blob/master/simplify_nq_data.py
# this has been modified to run in parallel

r"""Script to apply `text_utils.simplify_nq_data` to all examples in a split.

We have provided the processed training set at the link below.

https://storage.cloud.google.com/natural_questions/v1.0-simplified/simplified-nq-train.jsonl.gz

The test set, used by NQ's competition website, is only provided in the original
NQ format. If you wish to use the simplified format, then you should call
`text_utils.simplify_nq_data` in your submitted system.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import glob
import gzip
import json
import os
import time

from absl import app
from absl import flags

import text_utils as text_utils

FLAGS = flags.FLAGS

DATA_DIR = os.path.join(os.path.expanduser("~"), "data", "v1.0")

flags.DEFINE_string(
    "data_dir", default=DATA_DIR, help="Path to directory containing original NQ files, matching the pattern `nq-<split>-??.jsonl.gz`.")

flags.DEFINE_string(
    "dataset", default="train", help="Path to directory containing original NQ files, matching the pattern `nq-<split>-??.jsonl.gz`.")


def main(_):
    """Runs `text_utils.simplify_nq_example` over multiple files in a directory.
    Creates simplified versions in the same directory with 'simplified-' prefix.
    """
    # Get all matching files
    pattern = os.path.join(FLAGS.data_dir, f"{FLAGS.dataset}", f"nq-{FLAGS.dataset}-*.jsonl.gz")
    input_files = glob.glob(pattern)
    
    if not input_files:
        print(f"No files found matching pattern: {pattern}")
        return
        
    num_processed = 0
    start = time.time()
    
    for inpath in input_files:
        # Create output filename based on input filename
        filename = os.path.basename(inpath)
        outpath = os.path.join(FLAGS.data_dir, f"{FLAGS.dataset}", f"simplified-{filename}")
        
        print(f"Processing {filename}")
        
        with gzip.open(outpath, "wb") as fout, gzip.open(inpath, "rb") as fin:
            for l in fin:
                utf8_in = l.decode("utf8", "strict")
                utf8_out = json.dumps(
                    text_utils.simplify_nq_example(json.loads(utf8_in))) + u"\n"
                fout.write(utf8_out.encode("utf8"))
                num_processed += 1
                if not num_processed % 100:
                    print(f"Processed {num_processed} examples in {time.time() - start:.2f}s")
                    
        print(f"Completed {filename}")
    
    print(f"\nFinished processing {num_processed} total examples in {time.time() - start:.2f}s")

if __name__ == "__main__":
    app.run(main)
