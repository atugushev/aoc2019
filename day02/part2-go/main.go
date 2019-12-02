package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
)

func calc_first_elem(memory []int) int {
	i := 0
	for {
		opcode := memory[i]
		if opcode == 99 {
			break
		} else if opcode == 1 {
			memory[memory[i+3]] = memory[memory[i+1]] + memory[memory[i+2]]
		} else if opcode == 2 {
			memory[memory[i+3]] = memory[memory[i+1]] * memory[memory[i+2]]
		} else {
			fmt.Fprintf(os.Stderr, "Unexpected opcode=%d at i=%d", opcode, i)
		}
		i += 4
	}
	return memory[0]
}

func calc(lines string) int {
	memory_strs := strings.Split(lines, ",")
	memory := make([]int, len(memory_strs))
	for i, value := range memory_strs {
		memory[i], _ = strconv.Atoi(value)
	}
	for noun := range [99]int{} {
		for verb := range [99]int{} {
			memory_tmp := make([]int, len(memory))
			copy(memory_tmp, memory)
			memory_tmp[1] = noun
			memory_tmp[2] = verb
			if calc_first_elem(memory_tmp) == 19690720 {
				return 100*noun + verb
			}
		}
	}
	panic("magic numbers not found")
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
