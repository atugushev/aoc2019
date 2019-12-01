package main

import "testing"

func TestCalc(t *testing.T) {
	params := []struct {
		fuel     string
		expected int
	}{
		{"14", 2},
		{"1969", 966},
		{"100756", 50346},
	}

	for _, param := range params {
		fuel := calc(param.fuel)
		if fuel != param.expected {
			t.Errorf("Unexpected fuel: %d, expected: %d", fuel, param.expected)
		}
	}
}
