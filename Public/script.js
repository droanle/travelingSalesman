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

    document.getElementById("t0").value = "";
    document.getElementById("t1").value = "";
    document.getElementById("t2").value = "";
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

      var text =
        "Solucão: " +
        data.trains_infos[key].solution_full +
        "  Custo: " +
        data.trains_infos[key].solution_value;

      document.getElementById("t" + key).innerHTML = text;
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
      data["attempts"] = attempts;
      makeRequest("../hillclimb/alternating", "GET", data, (res) => {
        display.render(res);
      });
    }
  },

  SimulatedTempering: () => {
    [exito, data] = EventHandler.getSetup();

    initial_temperature = document.getElementById("iqejc").value;
    cooling_rate = document.getElementById("isq56").value;
    iterations = document.getElementById("iwtzr").value;

    if (initial_temperature == "" || initial_temperature == null) {
      alert('O campo "initial_temperature" não pode estar vazio');
      exito = false;
    } else if (cooling_rate == "" || cooling_rate == null) {
      alert('O campo "cooling_rate" não pode estar vazio');
      exito = false;
    } else if (iterations == "" || iterations == null) {
      alert('O campo "iterations" não pode estar vazio');
      exito = false;
    }

    if (exito) {
      data["initial_temperature"] = initial_temperature;
      data["cooling_rate"] = cooling_rate;
      data["iterations"] = iterations;

      makeRequest("../simulatedseasoning", "GET", data, (res) => {
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

document
  .getElementById("idb1n")
  .addEventListener("click", EventHandler.SimulatedTempering);
