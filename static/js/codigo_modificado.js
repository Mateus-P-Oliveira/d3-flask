// Define a função grid
function createGrid(width, height, x, y, value) {
    console.log("sdsdsdsdsd")
    const q = 4; // O nível de detalhe, por exemplo, amostra a cada 4 pixels em x e y.
    const x0 = -q / 2, x1 = width + 28 + q;
    const y0 = -q / 2, y1 = height + q;
    const n = Math.ceil((x1 - x0) / q);
    const m = Math.ceil((y1 - y0) / q);
    const grid = new Array(n * m);
    for (let j = 0; j < m; ++j) {
        for (let i = 0; i < n; ++i) {
            grid[j * n + i] = value(x.invert(i * q + x0), y.invert(j * q + y0));
        }
    }
    grid.x = -q;
    grid.y = -q;
    grid.k = q;
    grid.n = n;
    grid.m = m;
    console.log(grid.m);
    console.log(grid.n);
    return grid;
}

// Define a função transform
function transform({ type, value, coordinates }, grid) {
    return {
        type,
        value,
        coordinates: coordinates.map(rings => {
            return rings.map(points => {
                return points.map(([x, y]) => ([
                    grid.x + grid.k * x,
                    grid.y + grid.k * y
                ]));
            });
        })
    };
}

// Calcula os contornos usando D3.js
function calculateContours(grid, thresholds) {
    console.log("~~~~~~~~~")
    return d3.contours()
        .size([grid.n, grid.m])
        .thresholds(thresholds)
        (grid)
        .map(transform);
}

function value(x, y) {
    return x * x + y * y;
}

// Função para criar o gráfico de contorno usando D3.js
function createContourPlot() {
    fetch('/contour-data')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
    .then(data =>{ 
    const X = data.X;
    const Y = data.Y;
    const Z = data.Z;

    // Defina as dimensões e margens para o gráfico
    const margin = { top: 20, right: 20, bottom: 30, left: 40 };
    const width = 600 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;
    
    // Selecione o elemento SVG
    const svg = d3.select("#contour-plot")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // Defina as escalas para os eixos x e y
    const xScale = d3.scaleLinear()
        .domain([d3.min(X), d3.max(X)])
        .range([0, width]);

    const yScale = d3.scaleLinear()
        .domain([d3.min(Y), d3.max(Y)])
        .range([height, 0]);


    value(X,Y);
    // Calcula os contornos
    createGrid(width,height,xScale,yScale,value);
    console.log("---------")
    const contours = calculateContours(Z, d3.range(-1, 1, 0.1));

    // Crie os caminhos para os contornos
    svg.selectAll("path")
        .data(contours)
        .enter().append("path")
        .attr("d", d3.geoPath().projection(d3.geoIdentity().scale(width / X.length)))
        .attr("fill", "none")
        .attr("stroke", "black");

    // Adicione o eixo x
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(xScale));

    // Adicione o eixo y
    svg.append("g")
        .call(d3.axisLeft(yScale));
    })
   
    .catch(error => console.error('Error fetching or parsing data:', error));
}





// Define a função grid

function value(x, y) {
    return x * x + y * y;
}
// Define a função grid
const grid = (width, height, xScale, yScale, value) => {
    const q = 4; // O nível de detalhe, por exemplo, amostra a cada 4 pixels em x e y.
    const x0 = -q / 2, x1 = width + 28 + q;
    const y0 = -q / 2, y1 = height + q;
    const n = Math.ceil((x1 - x0) / q);
    const m = Math.ceil((y1 - y0) / q);
    const grid = new Array(n * m);
    for (let j = 0; j < m; ++j) {
      for (let i = 0; i < n; ++i) {
        // Convertendo coordenadas de tela para coordenadas de dados usando as escalas x e y
        const xData = xScale.invert(i * q + x0);
        const yData = yScale.invert(j * q + y0);
        grid[j * n + i] = value(xData, yData);
      }
    }
    grid.x = -q;
    grid.y = -q;
    grid.k = q;
    grid.n = n;
    grid.m = m;
    return grid;
  };
  

  
  
  // Define a função transform
  const transform = ({ type, value, coordinates }, grid) => {
    return {
      type,
      value,
      coordinates: coordinates.map(rings => {
        return rings.map(points => {
          return points.map(([x, y]) => ([
            grid.x + grid.k * x,
            grid.y + grid.k * y
          ]));
        });
      })
    };
  };
  
  // Função para criar o gráfico de contorno usando D3.js
  function createContourPlot() {
    fetch('/contour-data')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => { 
            const X = data.X;
            const Y = data.Y;
            const Z = data.Z;
  
            // Defina as dimensões e margens para o gráfico
            const margin = { top: 20, right: 20, bottom: 30, left: 40 };
            const width = 600 - margin.left - margin.right;
            const height = 400 - margin.top - margin.bottom;
            
            // Selecione o elemento SVG
            const svg = d3.select("#contour-plot")
                .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  
            // Defina as escalas para os eixos x e y
            const xScale = d3.scaleLinear()
                .domain([d3.min(X), d3.max(X)])
                .range([0, width]);
  
            const yScale = d3.scaleLinear()
                .domain([d3.min(Y), d3.max(Y)])
                .range([height, 0]);
  
            // Cria o grid
            console.log(width)
            console.log(height)
            console.log(xScale)
            console.log(yScale)
            console.log(value)
            const gridData = grid(width, height, xScale, yScale, value);
            console.log(gridData)
            console.log(gridData.m)
            console.log(gridData.n)
            // Calcula os contornos
            const contours = d3.contours()
                                .size([gridData.n, gridData.m])
                                .thresholds(d3.range(-1, 1, 0.1))
                              (gridData)
                              .map(contour => transform(contour, gridData));
  
            // Crie os caminhos para os contornos
            svg.selectAll("path")
                .data(contours)
                .enter().append("path")
                .attr("d", d3.geoPath().projection(d3.geoIdentity().scale(width / X.length)))
                .attr("fill", "none")
                .attr("stroke", "black");
  
            // Adicione o eixo x
            svg.append("g")
                .attr("transform", "translate(0," + height + ")")
                .call(d3.axisBottom(xScale));
  
            // Adicione o eixo y
            svg.append("g")
                .call(d3.axisLeft(yScale));
//------------
                Plotly.plot({
                    color: {scheme: "Magma", type: "log", legend: true, width: 300, label: "Value", tickFormat: ","},
                    marks: [
                        Plot.contour({
                            x1: d3.min(X),
                            x2: d3.max(X),
                            y1: d3.min(Y),
                            y2: d3.max(Y),
                            fill: value,
                            stroke: "#fff",
                            strokeOpacity: 0.5,
                            thresholds: d3.range(1, 20).map(n => 2 ** n)
                        })
                    ]
                });
    
        })

        //--------
        .catch(error => console.error('Error fetching or parsing data:', error));
  }
  
