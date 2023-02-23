use std::time::{Instant, Duration};

fn elapsed_ms(start: Instant, end: Instant) -> f64 {
    let dur: Duration = end - start;
    dur.as_secs_f64()
}

fn cut(tour: Vec<u32>, subset: Vec<u32>) -> Vec<Vec<u32>> {
    let mut subtours: Vec<Vec<u32>> = vec![];
    let mut idxs: Vec<usize> = tour
        .iter()
        .enumerate()
        .filter_map(|(i, &node)| if subset.contains(&node) { Some(i) } else { None })
        .collect::<Vec<usize>>();
    idxs.sort();

    let last_ix: usize = tour.len() - 1;
    let mut prev: i32 = -1 as i32;
    for (e, idx) in idxs.iter().enumerate() {
        if e == idxs.len() - 1 && *idx != last_ix {
            for subtour in vec![tour[(prev + 1) as usize..*idx].to_vec(), tour[*idx..].to_vec()] {
                if !subtour.is_empty() {
                    if subset.contains(&subtour[0]) {
                        subtours.push(subtour)
                    } else {
                        subtours.push(subtour.into_iter().rev().collect())
                    }
                }
            }
        } else {
            let subtour: Vec<u32> = tour[(prev + 1) as usize..=*idx].to_vec();
            if !subtour.is_empty() {
                if subset.contains(&subtour[0]) {
                    subtours.push(subtour)
                } else {
                    subtours.push(subtour.iter().rev().cloned().collect())
                }
            }
            prev = *idx as i32
        }
    }
    subtours

}

fn main() {
    let mut printed: bool = false;
    let start: Instant = Instant::now();
    for _i in 0..=100000 {
        let tour: Vec<u32> = vec![780, 778, 540, 610, 414, 5, 30, 406, 596, 516, 746, 730, 512, 576, 382, 498, 374, 562, 488, 706, 708, 490, 564, 376, 500, 384, 578, 514, 740, 756, 518, 598, 408, 532, 416, 612, 542, 346, 344, 256, 294, 246, 334, 326, 238, 286, 228, 316, 318, 230, 288, 240, 328, 336, 248, 296, 258, 190, 188, 176, 178];
        let subset: Vec<u32> = vec![416, 514, 258, 230, 542, 190];
        let resultz: Vec<Vec<u32>> = cut(tour, subset);

        if !printed {
            let expected: Vec<Vec<u32>> = vec![vec![514, 578, 384, 500, 376, 564, 490, 708, 706, 488, 562, 374, 498, 382, 576, 512, 730, 746, 516, 596, 406, 30, 5, 414, 610, 540, 778, 780], vec![416, 532, 408, 598, 518, 756, 740], vec![542, 612], vec![230, 318, 316, 228, 286, 238, 326, 334, 246, 294, 256, 344, 346], vec![258, 296, 248, 336, 328, 240, 288], vec![190, 188, 176, 178]];
            println!("{:?}", resultz);
            printed = true;
            assert_eq!(expected, resultz)
        }
    }
    println!("x100000: cut() took {} secs", elapsed_ms(start, Instant:: now()));
}
