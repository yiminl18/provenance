from multiprocessing import Pool
import glob, os, gzip, json, time, psutil

from tqdm import tqdm

from absl import app
from absl import flags

import text_utils as text_utils

FLAGS = flags.FLAGS

DATA_DIR = os.path.join(os.path.expanduser("~"), "data", "v1.0")

flags.DEFINE_string(
    "data_dir", default=DATA_DIR, help="Path to directory containing original NQ files, matching the pattern `nq-<split>-??.jsonl.gz`.")

flags.DEFINE_string(
    "dataset", default="train", help="Path to directory containing original NQ files, matching the pattern `nq-<split>-??.jsonl.gz`.")

def get_unprocessed_files(data_dir, dataset):
    pattern = os.path.join(data_dir, f"nq-{dataset}-??.jsonl.gz")
    all_files = glob.glob(pattern)
    
    # Check which files already have simplified versions
    unprocessed = []
    for file in all_files:
        simplified_file = os.path.join(data_dir, f"simplified-{os.path.basename(file)}")
        if not os.path.exists(simplified_file):
            unprocessed.append(file)
            
    return unprocessed

def determine_optimal_workers():
    # Get number of physical cores (excluding hyperthreading)
    physical_cores = psutil.cpu_count(logical=False)
    # Leave 2 cores free for system processes
    return max(1, physical_cores - 2)

def process_single_file(args):
    inpath, data_dir = args
    filename = os.path.basename(inpath)
    outpath = os.path.join(data_dir, f"simplified-{filename}")
    
    if os.path.exists(outpath):
        return 0, filename, "skipped"
    
    num_processed = 0
    try:
        with gzip.open(outpath, "wb") as fout, gzip.open(inpath, "rb") as fin:
            for l in fin:
                utf8_in = l.decode("utf8", "strict")
                utf8_out = json.dumps(
                    text_utils.simplify_nq_example(json.loads(utf8_in))) + u"\n"
                fout.write(utf8_out.encode("utf8"))
                num_processed += 1
        return num_processed, filename, "completed"
    except Exception as e:
        return 0, filename, f"failed: {str(e)}"

def estimate_processing_time(data_dir, dataset, sample_size=2):
    """
    Estimates total processing time by running on a few files first
    """
    pattern = os.path.join(data_dir, f"{FLAGS.dataset}", f"nq-{dataset}-*.jsonl.gz")
    all_files = sorted(glob.glob(pattern))
    
    if not all_files:
        return None
        
    # Process first few files and time them
    start = time.time()
    num_examples = 0
    
    # Use minimum of sample_size or available files
    sample_files = all_files[:min(sample_size, len(all_files))]
    for file in sample_files:
        with gzip.open(file, "rb") as fin:
            for _ in fin:
                num_examples += 1
                
    duration = time.time() - start
    
    # Calculate estimates
    avg_examples_per_file = num_examples / len(sample_files)
    avg_time_per_file = duration / len(sample_files)
    total_files = len(all_files)
    
    estimated_total_examples = avg_examples_per_file * total_files
    estimated_total_time = avg_time_per_file * total_files
    
    # Account for parallelization
    num_workers = determine_optimal_workers()
    estimated_parallel_time = estimated_total_time / num_workers
    
    return {
        'total_files': total_files,
        'estimated_examples': int(estimated_total_examples),
        'estimated_serial_hours': estimated_total_time / 3600,
        'estimated_parallel_hours': estimated_parallel_time / 3600,
        'workers': num_workers
    }

def main(_):
    # Run estimation first
    print("Running processing time estimation...")
    estimate = estimate_processing_time(FLAGS.data_dir, FLAGS.dataset)
    
    if estimate:
        print("\nProcessing estimates:")
        print(f"Total files to process: {estimate['total_files']}")
        print(f"Estimated total examples: {estimate['estimated_examples']:,}")
        print(f"Estimated time (serial): {estimate['estimated_serial_hours']:.1f} hours")
        print(f"Estimated time ({estimate['workers']} workers): {estimate['estimated_parallel_hours']:.1f} hours")
        
    proceed = input("\nProceed with processing? (y/n): ").lower().strip()
    if proceed != 'y':
        print("Aborting processing")
        return
        
    # Rest of your processing code...
    # Get all input files
    pattern = os.path.join(FLAGS.data_dir,  f"{FLAGS.dataset}", f"nq-{FLAGS.dataset}-*.jsonl.gz")
    input_files = sorted(glob.glob(pattern))
    
    if not input_files:
        print(f"No files found matching pattern: {pattern}")
        return
    
    # Setup multiprocessing
    num_workers = determine_optimal_workers()
    print(f"Using {num_workers} worker processes")
    
    # Prepare arguments
    args = [(f, FLAGS.data_dir) for f in input_files]
    
    # Process files with progress bar
    start = time.time()
    total_processed = 0
    with Pool(num_workers) as pool:
        with tqdm(total=len(args), desc="Processing files") as pbar:
            for num_proc, filename, status in pool.imap_unordered(process_single_file, args):
                total_processed += num_proc
                pbar.set_postfix({
                    'file': filename, 
                    'status': status,
                    'total_examples': total_processed
                })
                pbar.update()
    
    duration = time.time() - start
    print(f"\nProcessing complete:")
    print(f"Total examples processed: {total_processed}")
    print(f"Total time: {duration:.2f}s")
    print(f"Processing rate: {total_processed/duration:.2f} examples/second")

if __name__ == "__main__":
    app.run(main)