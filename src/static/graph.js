document.addEventListener("DOMContentLoaded", async () => {
    const width = 800;
    const height = 600;

    const svg = d3
        .select("#graph")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    const data = await fetch("/api/graph-data").then((res) => res.json());

    const simulation = d3
        .forceSimulation(data.nodes)
        .force("link", d3.forceLink(data.links).id((d) => d.id))
        .force("charge", d3.forceManyBody().strength(-200))
        .force("center", d3.forceCenter(width / 2, height / 2));

    const link = svg
        .selectAll(".link")
        .data(data.links)
        .enter()
        .append("line")
        .attr("class", "link")
        .style("stroke", "#999");

    const node = svg
        .selectAll(".node")
        .data(data.nodes)
        .enter()
        .append("circle")
        .attr("class", "node")
        .attr("r", 10)
        .style("fill", "blue");

    const labels = svg
        .selectAll(".label")
        .data(data.nodes)
        .enter()
        .append("text")
        .attr("class", "label")
        .text((d) => d.name)
        .style("font-size", "12px");

    simulation.on("tick", () => {
        link
            .attr("x1", (d) => d.source.x)
            .attr("y1", (d) => d.source.y)
            .attr("x2", (d) => d.target.x)
            .attr("y2", (d) => d.target.y);

        node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);

        labels
            .attr("x", (d) => d.x + 12)
            .attr("y", (d) => d.y + 4);
    });
});
