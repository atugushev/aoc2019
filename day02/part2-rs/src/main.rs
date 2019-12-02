use std::env;
use std::fs;
use std::process;
use test_case::test_case;

fn calc_first_elem(codes: &mut Vec<usize>) -> usize {
    let mut ip: usize = 0;
    loop {
        let opcode = codes[ip];
        if opcode == 99 {
            break;
        } else if opcode == 1 {
            let store = codes[ip + 3];
            codes[store] = codes[codes[ip + 1]] + codes[codes[ip + 2]];
        } else if opcode == 2 {
            let store = codes[ip + 3];
            codes[store] = codes[codes[ip + 1]] * codes[codes[ip + 2]];
        } else {
            panic!(
                "unexpected instruction pointer position, ip={}, opcode={}",
                ip, opcode
            );
        }
        ip += 4;
    }
    codes[0]
}

fn calc(s: String) -> usize {
    let codes: Vec<usize> = s.split(",").filter_map(|w| w.parse().ok()).collect();
    for noun in 0..99 {
        for verb in 0..99 {
            let mut new_codes = codes.to_vec();
            new_codes[1] = noun;
            new_codes[2] = verb;
            if calc_first_elem(&mut new_codes) == 19690720 {
                return 100 * noun + verb;
            }
        }
    }
    panic!("numbers not found")
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("no path given");
        process::exit(1);
    }

    let path = &args[1];
    let content = fs::read_to_string(path).unwrap();
    println!("{}", calc(content));
}

#[test_case(vec![1,9,10,3,2,3,11,0,99,30,40,50], 3500)]
#[test_case(vec![1,0,0,0,99], 2)]
#[test_case(vec![2,3,0,3,99], 2)]
#[test_case(vec![2,4,4,5,99,0], 2)]
#[test_case(vec![1,1,1,4,99,5,6,0,99], 30)]
fn tests(mass: Vec<usize>, expected_fuel: usize) {
    let fuel = calc_first_elem(&mut mass.to_vec());
    assert_eq!(fuel, expected_fuel);
}
