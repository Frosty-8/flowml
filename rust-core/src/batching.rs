use rayon::prelude::*;

pub fn process_batches<T: Send + Sync>(
    data: Vec<T>,
    batch_size: usize,
    func: fn(&[T])
) {
    data.par_chunks(batch_size)
        .for_each(|chunk| {
            func(chunk);
        });
}