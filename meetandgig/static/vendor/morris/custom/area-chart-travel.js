// Morris Area Chart

Morris.Area({
	element: 'area-chart-travel',
	data: [
		{ y: '2012', a: 5, b: 0, c: 0 },
		{ y: '2013', a: 40,  b: 15, c: 5 },
		{ y: '2014', a: 15,  b: 50, c: 25 },
		{ y: '2015', a: 40,  b: 15, c: 7 },
		{ y: '2016', a: 20,  b: 30, c: 35 },
		{ y: '2017', a: 35,  b: 55, c: 20 },
		{ y: '2018', a: 5, b: 10, c: 5 }
	],
	xkey: 'y',
	ykeys: ['a', 'b', 'c'],
	behaveLikeLine: !0,
	pointSize: 0,
	labels: ['Domestic', 'International', 'Earnings'],
	pointStrokeColors: ['#aa0000', '#cc0000', '#ee0000', '#ff3333', '#ff7777'],
	gridLineColor: "#e4e6f2",
	lineColors: ['#aa0000', '#cc0000', '#ee0000', '#ff3333', '#ff7777'],
	gridtextSize: 10,
	fillOpacity: 0.6,
	lineWidth: 0,
	hideHover: "auto",
	resize: true,
	redraw: true,
});

