// plotly.js here
// we are going to do a cartesian plot

function makeRequest(url, method, data, callback) {
  var xhr = new XMLHttpRequest();

  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) {
      callback(JSON.parse(xhr.responseText));
    }
  };

  xhr.open(method, url + "?" + new URLSearchParams(data).toString(), true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send();
}

class Display {
  constructor(divId) {
    this.father = document.getElementById(divId);
  }

  destruct() {
    this.father.innerHTML = "";
  }

  repar() {
    this.father.innerHTML = ` 
        <div id="plotly" style=" 
                position: absolute;
                width: 100%; 
                height: 100%;"
        >
        </div>;`;
  }

  generateRandomColor(opacity = 1) {
    // Generate random values for red, green, and blue components
    var red = Math.floor(Math.random() * 256);
    var green = Math.floor(Math.random() * 256);
    var blue = Math.floor(Math.random() * 256);

    // Construct the CSS color string using RGB format
    var color =
      "rgba(" + red + ", " + green + ", " + blue + ", " + opacity + ")";

    return color;
  }

  render(data) {
    this.destruct();

    var x = [];
    var y = [];

    for (const [key, [X, Y]] of Object.entries(data.coordinate_list)) {
      x.push(X);
      y.push(Y);
    }

    var points = {
      x: x,
      y: y,
      mode: "markers",
      type: "scatter",
      name: "Pontos",
      marker: {
        color: "rgba(0, 0, 0, 0.75)",
        size: 10,
      },
    };

    var traces = [points];

    for (const [key, train] of Object.entries(data.trains_infos)) {
      x = [];
      y = [];

      for (const [pathKey, [X, Y]] of Object.entries(train.solution)) {
        x.push(X);
        y.push(Y);
      }

      let color = this.generateRandomColor();

      data.trains_infos[key].color = color;

      traces.push({
        x: x,
        y: y,
        mode: "lines",
        type: "scatter",
        name: "Tren " + key,
        marker: {
          color: color,
          size: 10,
        },
      });
    }

    var layout = {
      autosize: true,
      responsive: true,

      xaxis: {
        showgrid: false,
        zeroline: false,
      },
    };

    this.repar();
    Plotly.newPlot("plotly", traces, layout);
  }
}

display = new Display("i00e6");

EventHandler = {
  getSetup: () => {
    let nPlano = document.getElementById("ig71d").value;
    let nPontos = document.getElementById("iefjh").value;
    let seed = document.getElementById("iys3d").value;

    if (nPlano == "" || nPlano == null) {
      alert('O campo "Tamanho de plano" não pode estar vazio');
    } else if (nPlano == "" || nPlano == null) {
      alert('O campo "Numero de pontos" não pode estar vazio');
    } else if (nPlano == "" || nPlano == null) {
      alert('O campo "Seed" não pode estar vazio');
    } else
      return [
        true,
        {
          nPlano: nPlano,
          nPontos: nPontos,
          seed: seed,
        },
      ];

    return [false, null];
  },

  HillClimb: () => {
    [exito, data] = EventHandler.getSetup();

    if (exito) {
      makeRequest("../hillclimb/", "GET", data, (res) => {
        display.render(res);
      });
    }
  },
  AlternateHillClimb: () => {
    [exito, data] = EventHandler.getSetup();

    attempts = document.getElementById("iwtzr").value;

    if (attempts == "" || attempts == null) {
      alert('O campo "Tentativas" não pode estar vazio');
      exito = false;
    }

    if (exito) {
      makeRequest("../hillclimb/", "GET", data, (res) => {
        display.render(res);
      });
    }
  },

  SimulatedTempering: () => {
    [exito, data] = EventHandler.getSetup();

    initial_temperature = document.getElementById("iqejc").value;
    cooling_rate = document.getElementById("isq56").value;
    iterations = document.getElementById("iwtzr").value;

    if (attempts == "" || attempts == null) {
      alert('O campo "Tentativas" não pode estar vazio');
      exito = false;
    }

    if (exito) {
      makeRequest("../hillclimb/", "GET", data, (res) => {
        display.render(res);
      });
    }
  },
};

document
  .getElementById("ibqbh")
  .addEventListener("click", EventHandler.HillClimb);

document
  .getElementById("iqce3")
  .addEventListener("click", EventHandler.AlternateHillClimb);

const x = [1, 2, 3, 4, 3, 2, 1];
const y = [10, 15, 13, 17, 8, 12, 5];

var trace1 = {
  x: x,
  y: y,
  mode: "markers",
  type: "scatter",
  // color
  marker: {
    color: "rgb(255, 0, 0)",
    size: 10,
  },
};

// we are going to connect the dots

const x_line = [];
const y_line = [];

// we want to connect ALL dots, as this is a TSP algorithm
for (let i = 0; i < x.length; i++) {
  for (let j = 0; j < x.length; j++) {
    if (i != j) {
      x_line.push(x[i]);
      y_line.push(y[i]);
      x_line.push(x[j]);
      y_line.push(y[j]);
      x_line.push(null);
      y_line.push(null);
    }
  }
}

var trace2 = {
  x: x_line,
  y: y_line,
  mode: "lines",
  type: "scatter",
  // color
  marker: {
    color: "rgb(0, 0, 255)",
    size: 10,
  },
};

var data = [trace2, trace1];

// layout to automatically resize the plot
var layout = {
  autosize: true,
  responsive: true,

  xaxis: {
    showgrid: false,
    zeroline: false,
  },
};

Plotly.newPlot("plotly", data, layout);
