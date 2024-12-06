var fs = require("fs");
const { join } = require("path");

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

  var heading = "N";

  const nextHeading = {
    N: "E",
    E: "S",
    S: "W",
    W: "N",
  };

  let counter = 1;

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
    } else if (floorplan[target[1]][target[0]] == "#") {
      // Obstacle found, turn
      heading = nextHeading[heading];
    } else {
      // Move forward
      if (floorplan[target[1]][target[0]] === ".") {
        counter += 1;
      }
      floorplan[currentY][currentX] = "X";
      floorplan[target[1]][target[0]] = "^";
      currentX = target[0];
      currentY = target[1];
    }
  } while (true);
  console.log(counter);
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
  return;
}

solve();
