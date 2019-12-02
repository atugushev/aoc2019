use std::env;
use std::fs;
use std::process;
use test_case::test_case;

fn calc(s: String) -> usize {
    let mut codes: Vec<usize> = s.split(",").filter_map(|w| w.parse().ok()).collect();
    let mut ip: usize = 0;
    loop {
        if codes[ip] == 99 {
            break;
        } else if codes[ip] == 1 {
            let store = codes[ip + 3];
            codes[store] = codes[codes[ip + 1]] + codes[codes[ip + 2]];
        } else if codes[ip] == 2 {
            let store = codes[ip + 3];
            codes[store] = codes[codes[ip + 1]] * codes[codes[ip + 2]];
        } else {
            panic!("unexpected instruction pointer position");
        }
        ip += 4;
    }
    codes[0]
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

#[test_case("1,9,10,3,2,3,11,0,99,30,40,50", 3500)]
#[test_case("1,0,0,0,99", 2)]
#[test_case("2,3,0,3,99", 2)]
#[test_case("2,4,4,5,99,0", 2)]
#[test_case("1,1,1,4,99,5,6,0,99", 30)]
fn tests(mass: &str, expected_fuel: usize) {
    let fuel = calc(mass.to_string());
    assert_eq!(fuel, expected_fuel);
}
