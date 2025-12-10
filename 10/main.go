package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type LineData struct {
	buttons   [][]int
	nJoltage  int
	targetJol []int
}

func readInput(filename string) []LineData {
	file, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	var data []LineData
	scanner := bufio.NewScanner(file)
	buttonRe := regexp.MustCompile(`\(([^)]+)\)`)
	bracketRe := regexp.MustCompile(`\{([^}]+)\}`)

	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())

		// Parse buttons: (3) (1,3) (2) etc - between ] and {
		startIdx := strings.Index(line, "]") + 1
		endIdx := strings.Index(line, "{")
		buttonsStr := line[startIdx:endIdx]

		var buttons [][]int
		for _, match := range buttonRe.FindAllStringSubmatch(buttonsStr, -1) {
			numStrs := strings.Split(match[1], ",")
			var nums []int
			for _, s := range numStrs {
				n, _ := strconv.Atoi(strings.TrimSpace(s))
				nums = append(nums, n)
			}
			buttons = append(buttons, nums)
		}

		// Parse brackets: {3,5,4,7}
		bracketMatch := bracketRe.FindStringSubmatch(line)
		var targetJol []int
		for _, s := range strings.Split(bracketMatch[1], ",") {
			n, _ := strconv.Atoi(strings.TrimSpace(s))
			targetJol = append(targetJol, n)
		}

		data = append(data, LineData{
			buttons:   buttons,
			nJoltage:  len(targetJol),
			targetJol: targetJol,
		})
	}
	return data
}

func sliceToKey(s []int) string {
	var parts []string
	for _, v := range s {
		parts = append(parts, strconv.Itoa(v))
	}
	return strings.Join(parts, ",")
}

func slicesEqual(a, b []int) bool {
	if len(a) != len(b) {
		return false
	}
	for i := range a {
		if a[i] != b[i] {
			return false
		}
	}
	return true
}

func p2(data []LineData) int {
	solutions := 0

	for i, line := range data {
		fmt.Printf("Processing line %d/%d\n", i+1, len(data))

		// Find max target value to bound our search
		maxTarget := 0
		for _, t := range line.targetJol {
			if t > maxTarget {
				maxTarget = t
			}
		}

		nButtons := len(line.buttons)
		minPresses := -1

		// Recursive search with pruning
		var search func(buttonIdx int, joltage []int, presses int)
		search = func(buttonIdx int, joltage []int, presses int) {
			// Prune if we already found a better solution
			if minPresses != -1 && presses >= minPresses {
				return
			}

			// Check if we've reached the target
			if slicesEqual(joltage, line.targetJol) {
				if minPresses == -1 || presses < minPresses {
					minPresses = presses
				}
				return
			}

			// If we've assigned all buttons, stop
			if buttonIdx >= nButtons {
				return
			}

			// Try pressing this button 0 to maxPossible times
			button := line.buttons[buttonIdx]

			// Calculate max times we can press this button without exceeding any target
			maxPresses := maxTarget
			for _, idx := range button {
				remaining := line.targetJol[idx] - joltage[idx]
				if remaining < maxPresses {
					maxPresses = remaining
				}
			}

			for count := 0; count <= maxPresses; count++ {
				// Apply this many presses
				newJoltage := make([]int, line.nJoltage)
				copy(newJoltage, joltage)
				for _, idx := range button {
					newJoltage[idx] += count
				}

				// Check if any exceeded (shouldn't happen with maxPresses calc, but be safe)
				exceeded := false
				for j := 0; j < line.nJoltage; j++ {
					if newJoltage[j] > line.targetJol[j] {
						exceeded = true
						break
					}
				}
				if exceeded {
					break
				}

				search(buttonIdx+1, newJoltage, presses+count)
			}
		}

		initialJoltage := make([]int, line.nJoltage)
		search(0, initialJoltage, 0)

		if minPresses != -1 {
			solutions += minPresses
		}
	}

	return solutions
}

func main() {
	test := readInput("test")
	fmt.Println("P2 TEST:", p2(test)) // should be 33
}
