var options = {
	chart: {
		type: 'donut',
		height: 250,
	},
	legend: {
		position: "bottom",
		offsetY: 10,
	},
	dataLabels: {
		enabled: false
  },
	labels: ['Buy', 'Sell', 'Keep'],
	series: [20, 70, 30],
	stroke: {
		width: 0,
	},
	colors: ['#aa0000', '#cc0000', '#ee0000', '#ff3333', '#ff7777'],
}
var chart = new ApexCharts(
	document.querySelector("#donut-volume-currency"),
	options
);
chart.render();