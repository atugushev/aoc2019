package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
)

func calc_fuel(mass int) int {
	return mass/3 - 2
}

func calc(lines string) int {
	total := 0
	for _, line := range strings.Split(lines, "\n") {
		mass, _ := strconv.Atoi(line)
		total += calc_fuel(mass)
	}
	return total
}

func main() {
	if len(os.Args) != 2 {
		panic("no path given")
	}
	path := os.Args[1]

	buf, err := ioutil.ReadFile(path)
	if err != nil {
		panic(err)
	}
	fmt.Print(calc(string(buf)))
}
