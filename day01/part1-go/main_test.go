package main

import "testing"

func TestCalc(t *testing.T) {
	params := []struct {
		fuel     string
		expected int
	}{
		{"12", 2},
		{"14", 2},
		{"1969", 654},
		{"100756", 33583},
	}

	for _, param := range params {
		fuel := calc(param.fuel)
		if fuel != param.expected {
			t.Errorf("Unexpected fuel: %d, expected: %d", fuel, param.expected)
		}
	}
}
