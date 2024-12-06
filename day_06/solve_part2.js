var fs = require("fs");

const nextHeading = {
  N: "E",
  E: "S",
  S: "W",
  W: "N",
};

function solve() {
  var lines = fs.readFileSync("input.txt").toString().split("\n");
  var floorplan = [];
  for (i in lines) {
    floorplan = floorplan.concat([lines[i].split("")]);
  }

  var xLim = floorplan[0].length;
  var yLim = floorplan.length;

  var currentX;
  var currentY;

  for (let i = 0; i < yLim; i++) {
    for (let j = 0; j < xLim; j++) {
      if (floorplan[i][j] === "^") {
        currentX = j;
        currentY = i;
      }
    }
  }

  let initialFloorplan = JSON.parse(JSON.stringify(floorplan));
  const test_set = makeTestSet(
    initialFloorplan,
    currentX,
    currentY,
    xLim,
    yLim
  );

  /*for (let i = 0; i < yLim; i++) {
    for (let j = 0; j < xLim; j++) {
      test_set.push([i, j]);
    }
  }*/

  let counter = 0;

  test_set.forEach((location) => {
    let workingFloorplan = JSON.parse(JSON.stringify(floorplan));
    workingFloorplan[location[0]][location[1]] = "#";
    //printFloorplan(workingFloorplan);
    //console.log(location);
    if (testMap(workingFloorplan, currentX, currentY)) {
      counter++;
    }
  });

  console.log(counter);
}

function testMap(testFloorplan, startX, startY) {
  var heading = "N";
  var visited = [];

  var currentX = startX;
  var currentY = startY;

  var xLim = testFloorplan[0].length;
  var yLim = testFloorplan.length;

  do {
    visited.push([currentX, currentY, heading]);
    const target = nextLocation(currentX, currentY, heading);
    if (
      target[0] >= xLim ||
      target[1] >= yLim ||
      target[0] < 0 ||
      target[1] < 0
    ) {
      // Guard left the map, terminate
      return false;
    } else if (testFloorplan[target[1]][target[0]] == "#") {
      // Obstacle found, turn
      heading = nextHeading[heading];
    } else {
      // Move forward
      if (
        visited.find(
          (e) => e[0] === target[0] && e[1] === target[1] && e[2] === heading
        )
      ) {
        return true;
      }
      testFloorplan[currentY][currentX] = "X";
      testFloorplan[target[1]][target[0]] = "^";
      currentX = target[0];
      currentY = target[1];
    }
  } while (true);
}

function makeTestSet(initialFloorplan, currentX, currentY, xLim, yLim) {
  let test_set = [];
  let heading = "N";
  do {
    // printFloorplan(floorplan);
    const target = nextLocation(currentX, currentY, heading);
    if (
      target[0] >= xLim ||
      target[1] >= yLim ||
      target[0] < 0 ||
      target[1] < 0
    ) {
      // Guard left the map, terminate
      break;
    } else if (initialFloorplan[target[1]][target[0]] == "#") {
      // Obstacle found, turn
      heading = nextHeading[heading];
    } else {
      // Move forward
      if (initialFloorplan[target[1]][target[0]] === ".") {
        test_set.push([target[1], target[0]]);
      }
      initialFloorplan[currentY][currentX] = "X";
      initialFloorplan[target[1]][target[0]] = "^";
      currentX = target[0];
      currentY = target[1];
    }
  } while (true);
  return test_set;
}

function nextLocation(currentX, currentY, heading) {
  switch (heading) {
    case "N":
      return [currentX, currentY - 1];
    case "E":
      return [currentX + 1, currentY];
    case "S":
      return [currentX, currentY + 1];
    case "W":
      return [currentX - 1, currentY];
  }
}

function printFloorplan(floorplan) {
  console.log(floorplan.length);
  for (i in floorplan) {
    console.log(floorplan[i].join(""));
  }
  console.log(" ");
  return;
}

solve();
