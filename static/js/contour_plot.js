// contour_plot.js
// JavaScript code for creating the contour plot using D3.js

// Function to fetch data and create the contour plot
function createContourPlot() {
    // Fetch data from Flask endpoint
    fetch('/contour-data')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Data processing and visualization using D3.js
            const X = data.X
            const Y = data.Y
            const Z = data.Z;

            for (var i = 0; i < Z.length; i++) {
                for (var j = 0; j < Z[i].length; j++) {
                    if (Z[i][j] < -1000000) {
                        Z[i][j] = null;
                    }
                }
            }

            console.log(Z);

            // Log the data to check if it's retrieved correctly
            console.log('X:', X);
            console.log('Y:', Y);
            console.log('Z:', Z);

            // Define the dimensions and margins for the plot
            const margin = { top: 20, right: 20, bottom: 30, left: 40 };
            const width = 800 - margin.left - margin.right;
            const height = 400 - margin.top - margin.bottom;

            // const logZi = Z;

            // console.log("logZi:",logZi)

            // const cleanedZValues = logZi.map(subArray => subArray.filter(value => !isNaN(value)));
            
            // const maxValue = cleanedZValues.reduce((max,subArray)=>{
            //     const subArrayMax = Math.max(...subArray);
            //         return Math.max(max,subArrayMax);

            // },-Infinity);

            // console.log("maxValue",maxValue);

            // const logZ = logZi.map(linha=>linha.map(valor=>valor / maxValue));

            // for(let i =0;i <logZ.length;i++){
            //     for(let j=0;j<logZ[i].length;j++){
            //         if(isNaN(logZ[i][j])){
            //             logZ[i][j] = null;
            //         }
            //     }
            // }
         
            // console.log("logZ:", logZ);

            const ZFiltered = Z.flat().filter(value => value !== null);

            const minn = Math.min(...ZFiltered)
            const maxx = Math.max(...ZFiltered)
            console.log("min:",minn);
            console.log("max:",maxx);

            // Append SVG to the div
        
            // Define scales for x and y axes
            const xScale = d3.scaleLinear()
                .domain(d3.extent(X))
                .range([margin.left,width - margin.right]);

            const yScale = d3.scaleLinear()
                .domain(d3.extent(Y))
                .range([height - margin.bottom, margin.top]);

            const nice = d3.nice(Math.log2(minn), Math.log2(maxx), 11)
            const thresholds = d3.ticks(nice[0], nice[1], 11).map(i => Math.pow(2, i))

            const colorScale = d3.scaleSequentialLog(d3.extent(thresholds), d3.interpolateViridis)
            
            console.log("thresholds: ", thresholds)
            // Define the contour function
            const contours = d3.contours()
                .size([X.length, Y.length])
                .thresholds(thresholds)
                (Z.flat());

            const svg = d3.select("#contour-plot") //Talvez mudar aqui
                .append("svg")
                .attr("width", width)
                .attr("height", height);



            // Log the generated contours
            console.log('----------');
            console.log('Contours:', contours);

            // Create paths for the contours
            svg.selectAll("path")
                .data(contours)
                .enter().append("path")
                .attr("d", d3.geoPath(d3.geoIdentity().scale(width / X.length)))
                .attr("fill", d => colorScale(d.value))
                .attr("stroke", "black");
                

            // Log the generated paths
            console.log('Paths:', svg.selectAll("path").nodes());
           
            // Add x-axis
            svg.append("g")
                .attr("transform", `translate(0, ${height - margin.bottom}) `)
                .call(d3.axisBottom(xScale));

            // Add y-axis
            svg.append("g")
                .attr("transform",`translate(${width - margin.right + 10},${margin.top})`)
                .call(d3.axisLeft(yScale));
            const legendWidth = 20;
            const legendHeight = 200;
            
            const legendSvg = svg.append("g")
                .attr("transform", `translate(${width - margin.right + 10}, ${margin.top})`);
            
            const legendScale = d3.scaleLinear()
                .domain(d3.extent(ZFiltered))
                .range([legendHeight,0]);

            const legendAxis = d3.axisRight(legendScale).ticks(6);

            const legendData = d3.range(minn, maxx, 50);

            legendSvg.selectAll("rect")
            .data(legendData)
            .enter().append("rect")
            .attr("y", d => legendScale(d))
            .attr("height", legendHeight / legendData.length)
            .attr("width", legendWidth)
            .attr("fill", d => colorScale(d));

            legendSvg.append("g")
            .attr("transform", `translate(${legendWidth},0)`)
            .call(legendAxis);
        
            })
        .catch(error => console.error('Error fetching or parsing data:', error));
}