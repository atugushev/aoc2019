use std::fs;
use test_case::test_case;

fn calc(s: String) -> i32 {
    let mut total = 0;
    for line in s.lines() {
        let mass: i32 = line.parse().unwrap();
        total += mass / 3 - 2;
    }
    return total;
}

fn main() {
    let path = std::env::args().nth(1).expect("no path given");
    let content = fs::read_to_string(path).unwrap();
    println!("{}", calc(content));
}

#[test_case("12", 2)]
#[test_case("14", 2)]
#[test_case("1969", 654)]
#[test_case("100756", 33583)]
fn tests(mass: &'static str, expected_fuel: i32) {
    let fuel = calc(mass.to_string());
    assert_eq!(fuel, expected_fuel);
}
