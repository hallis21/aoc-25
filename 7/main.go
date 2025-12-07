package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func readFile(filename string) []string {
	file, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	var lines []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, strings.TrimSpace(scanner.Text()))
	}
	return lines
}

type Point struct {
	x, y int
}

func p1() {
	fmt.Println("Part 1")
}

func p2(data []string) int {
	// Find starting position "S" in first line
	startX := strings.Index(data[0], "S")
	beams := []Point{{startX, 0}}

	for level := 0; level < len(data)-1; level++ {
		fmt.Printf("%d %d\n", level, len(beams))
		var newBeams []Point

		for _, beam := range beams {
			x, y := beam.x, beam.y

			if y+1 < len(data) {
				below := data[y+1][x]
				if below == '.' {
					newBeams = append(newBeams, Point{x, y + 1})
				} else if below == '^' {
					// Splitter: beam goes left and right
					newBeams = append(newBeams, Point{x - 1, y + 1})
					newBeams = append(newBeams, Point{x + 1, y + 1})
				}
			}
		}

		beams = newBeams
	}

	return len(beams)
}

func main() {
	p1()
	real := readFile("real")
	fmt.Println("Real:", p2(real))
}
