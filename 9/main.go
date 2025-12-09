package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Point struct {
	x, y int
}

func readFile(filename string) []Point {
	file, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	var coords []Point
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		parts := strings.Split(line, ",")
		x, _ := strconv.Atoi(parts[0])
		y, _ := strconv.Atoi(parts[1])
		coords = append(coords, Point{x, y})
	}
	return coords
}

func toRect(c1, c2 Point) int {
	width := abs(c2.x-c1.x) + 1
	height := abs(c2.y-c1.y) + 1
	return width * height
}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func getNextCells(x, y int, coords map[Point]bool, maxX, maxY int) []Point {
	var nextCells []Point

	// check +x
	for nx := x + 1; nx < maxX; nx++ {
		if coords[Point{nx, y}] {
			nextCells = append(nextCells, Point{nx, y})
			break
		}
	}
	// check -x
	for nx := x - 1; nx >= 0; nx-- {
		if coords[Point{nx, y}] {
			nextCells = append(nextCells, Point{nx, y})
			break
		}
	}
	// check +y
	for ny := y + 1; ny < maxY; ny++ {
		if coords[Point{x, ny}] {
			nextCells = append(nextCells, Point{x, ny})
			break
		}
	}
	// check -y
	for ny := y - 1; ny >= 0; ny-- {
		if coords[Point{x, ny}] {
			nextCells = append(nextCells, Point{x, ny})
			break
		}
	}
	return nextCells
}

func pointInPolygon(x, y int, polygon []Point) bool {
	n := len(polygon)
	inside := false

	j := n - 1
	for i := 0; i < n; i++ {
		xi, yi := polygon[i].x, polygon[i].y
		xj, yj := polygon[j].x, polygon[j].y

		if ((yi > y) != (yj > y)) && (float64(x) < float64(xj-xi)*float64(y-yi)/float64(yj-yi)+float64(xi)) {
			inside = !inside
		}
		j = i
	}
	return inside
}

func p2(data []Point) int {
	maxX, maxY := 0, 0
	for _, p := range data {
		if p.x+1 > maxX {
			maxX = p.x + 1
		}
		if p.y+1 > maxY {
			maxY = p.y + 1
		}
	}

	setOfCoords := make(map[Point]bool)
	for _, p := range data {
		setOfCoords[p] = true
	}

	setFilled := make(map[Point]bool)

	for _, p := range data {
		nextCells := getNextCells(p.x, p.y, setOfCoords, maxX, maxY)
		for _, next := range nextCells {
			if next.x == p.x {
				// vertical fill
				for fy := min(p.y, next.y) + 1; fy < max(p.y, next.y); fy++ {
					setFilled[Point{p.x, fy}] = true
				}
			} else if next.y == p.y {
				// horizontal fill
				for fx := min(p.x, next.x) + 1; fx < max(p.x, next.x); fx++ {
					setFilled[Point{fx, p.y}] = true
				}
			}
		}
	}

	fullShape := make(map[Point]bool)
	for p := range setOfCoords {
		fullShape[p] = true
	}
	for p := range setFilled {
		fullShape[p] = true
	}

	// Build rectangles sorted by area descending
	type rectInfo struct {
		area   int
		coord1 Point
		coord2 Point
	}
	var rectangles []rectInfo
	for i := 0; i < len(data); i++ {
		for j := i + 1; j < len(data); j++ {
			area := toRect(data[i], data[j])
			rectangles = append(rectangles, rectInfo{area, data[i], data[j]})
		}
	}

	// Sort descending by area
	for i := 0; i < len(rectangles)-1; i++ {
		for j := i + 1; j < len(rectangles); j++ {
			if rectangles[j].area > rectangles[i].area {
				rectangles[i], rectangles[j] = rectangles[j], rectangles[i]
			}
		}
	}

	fmt.Println("Total rectangles:", len(rectangles))

	for idx, rect := range rectangles {
		if idx%1000 == 0 {
			fmt.Printf("Checking rectangle %d of %d with area %d\n", idx, len(rectangles), rect.area)
		}

		x1, y1 := rect.coord1.x, rect.coord1.y
		x2, y2 := rect.coord2.x, rect.coord2.y

		corners := []Point{
			{min(x1, x2), min(y1, y2)},
			{min(x1, x2), max(y1, y2)},
			{max(x1, x2), min(y1, y2)},
			{max(x1, x2), max(y1, y2)},
		}

		allCornersInShape := true
		for _, c := range corners {
			if !fullShape[c] {
				// Use 'data' which has vertices in order, not fullShape
				if !pointInPolygon(c.x, c.y, data) {
					allCornersInShape = false
					break
				}
			}
		}

		if !allCornersInShape {
			continue
		}

		// Check all wall points
		var walls []Point
		for x := min(x1, x2); x <= max(x1, x2); x++ {
			walls = append(walls, Point{x, min(y1, y2)})
			walls = append(walls, Point{x, max(y1, y2)})
		}
		for y := min(y1, y2); y <= max(y1, y2); y++ {
			walls = append(walls, Point{min(x1, x2), y})
			walls = append(walls, Point{max(x1, x2), y})
		}

		allWallsInShape := true
		for _, w := range walls {
			if !fullShape[w] {
				// Use 'data' which has vertices in order, not fullShape
				if !pointInPolygon(w.x, w.y, data) {
					allWallsInShape = false
					break
				}
			}
		}

		if allWallsInShape {
			return rect.area
		}
	}

	return 0
}

func main() {
	real := readFile("real")
	fmt.Println("P2:", p2(real))
}
