package main

import "testing"

func TestCalc(t *testing.T) {
	params := []struct {
		memory   []int
		expected int
	}{
		{[]int{1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50}, 3500},
		{[]int{1, 0, 0, 0, 99}, 2},
		{[]int{2, 3, 0, 3, 99}, 2},
		{[]int{2, 4, 4, 5, 99, 0}, 2},
		{[]int{1, 1, 1, 4, 99, 5, 6, 0, 99}, 30},
	}

	for _, param := range params {
		output := calc_first_elem(param.memory)
		if output != param.expected {
			t.Errorf("Unexpected output: %d, expected: %d", output, param.expected)
		}
	}
}
