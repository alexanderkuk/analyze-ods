

var CHANNELS = d3.select('#channels');
var CHANNELS_CANVAS = CHANNELS.select('.canvas');
var CHANNELS_PROFILE = CHANNELS.select('.profile');

var USERS = d3.select('#users');
var USERS_CANVAS = USERS.select('.canvas');
var USERS_PROFILE = USERS.select('.profile');

var MESSAGES_BY_TIME = d3.select('#messages-by-time');
var MESSAGES_BY_TIME_CANVAS = MESSAGES_BY_TIME.select('.canvas');

var MESSAGES_BY_CHANNELS = d3.select('#messages-by-channels');
var MESSAGES_BY_CHANNELS_CANVAS = MESSAGES_BY_CHANNELS.select('.canvas');

var USERS_BY_TIME = d3.select('#users-by-time');
var USERS_BY_TIME_CANVAS = USERS_BY_TIME.select('.canvas');

var TOOLTIP = d3.select('body').append('div')
    .attr('class', 'tooltip')
    .classed('hidden', true);


var LG = 4
var MD = 3
var SM = 2
var XS = 1

var WIDTHS = {};
WIDTHS[LG] = 95;
WIDTHS[MD] = 80;
WIDTHS[SM] = 60;
WIDTHS[XS] = 60;

MONTHS = [
    'Январь',
    'Февраль',
    'Март',
    'Апрель',
    'Май',
    'Июнь',
    'Июль',
    'Август',
    'Сентябрь',
    'Октябрь',
    'Ноябрь',
    'Декабрь',
]

var OTHER = 'other';


function getLayout() {
    // http://stackoverflow.com/questions/3437786/get-the-size-of-the-screen-current-web-page-and-browser-window
    var element = document.documentElement;
    var body = document.getElementsByTagName('body')[0]
    var width = window.innerWidth || element.clientWidth || body.clientWidth;

    if (width) {
	// http://getbootstrap.com/css/#grid-options
	if (width >= 1200) {
	    return LG;
	} else if (width >= 992) {
	    return MD;
	} else if (width >= 768) {
	    return SM;
	} else {
	    return XS;
	}
    } else {
	return LG;
    }
}


var formatDate = d3.time.format('%Y-%m-%d');
var parseDate = formatDate.parse;


function vizChannelProfile(profile) {
    CHANNELS_PROFILE.select('.name').text('#' + profile['name']);
    CHANNELS_PROFILE.select('.created').text(formatDate(profile['created']));
    CHANNELS_PROFILE.select('.creator').text('@' + profile['creator']);
    CHANNELS_PROFILE.select('.purpose').text(profile['purpose']);
}


function formatRuDateTick(date) {
    var month = date.getMonth();
    if (month == 0) {
	return date.getFullYear();
    } else {
	return MONTHS[month];
    }
}


function vizChannels() {
    var layout = getLayout();
    var width = WIDTHS[layout];
    if (layout <= SM) {
	width *= 12;
    } else {
	width *= 6;
    }
    var height = 350;

    var margin = {top: 30, right: 20, bottom: 100, left: 100},
    width = width - margin.left - margin.right,
    height = height - margin.top - margin.bottom;

    var x = d3.time.scale()
	.range([0, width]);

    var y = d3.scale.ordinal()
	.rangePoints([height, 0]);

    var r = d3.scale.sqrt()
	.range([2, 20]);

    var color = d3.scale.category10();

    var xAxis = d3.svg.axis()
	.scale(x)
	.orient('bottom')
	.tickFormat(formatRuDateTick);

    var yAxis = d3.svg.axis()
	.scale(y)
	.orient('left')
	.tickFormat(function(d) {
	    if (d == OTHER) {
		return 'Другие';
	    } else {
		return d;
	    }
	});

    CHANNELS_CANVAS.select('svg').remove()
    var svg = CHANNELS_CANVAS.append('svg')
	.attr('width', width + margin.left + margin.right)
	.attr('height', height + margin.top + margin.bottom)
	.append('g')
	.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');    

    d3.json('data/channels.json', function(error, data) {
	if (error) {
	    throw error;
	}
	
	var records = data.records;
	records.forEach(function(d) {
	    d.created = parseDate(d.created);
	});
	records.sort(function(a, b) {
	    return b.messages - a.messages;
	});

	x.domain(d3.extent(records, function(d) {
	    return d.created;
	}));
	var order = data.order;
	var size = order.push(OTHER);
	y.domain(order);
	r.domain(d3.extent(records, function(d) {
	    return d.messages;
	}));

	svg.append('g')
	    .attr('class', 'x axis')
	    .attr('transform', 'translate(0,' + (height + 40) + ')')
	    .call(xAxis)
	    .append('text')
	    .attr('x', width)
	    .attr('y', -6)
	    .style('text-anchor', 'end')
	    .text('Дата создания');

	svg.append('g')
	    .attr('class', 'y axis')
	    .call(yAxis)

	svg.selectAll('.dot')
	    .data(records)
	    .enter().append('circle')
	    .attr('class', 'dot')
	    .attr('cx', function(d) {
		return x(d.created);
	    })
	    .attr('cy', function(d) {
		var creator = d.creator;
		if (order.indexOf(creator) == -1) {
		    creator = OTHER;
		}
		var jitter = (Math.random() - 0.5) * height / size;
		return y(creator) + jitter;
	    })
	    .attr('r', function(d) {
		return r(d.messages);
	    })
	    .style('fill', function(d) {
		return color(d.creator);
	    })
	    .on('mouseover', function(d) {
		vizChannelProfile(d);

		var dot = d3.select(this);
		dot.classed('active', true);
		var cx = +dot.attr('cx');
		var cy = +dot.attr('cy');
		var r = +dot.attr('r');
		tooltip.attr('x', cx + r + 2);
		tooltip.attr('y', cy);
		tooltip.text(d.name)
		tooltip.classed('hidden', false)

		CHANNELS_PROFILE.classed('hidden', false);
	    })
	    .on('mouseout', function(d) {
		d3.select(this).classed('active', false);
		tooltip.classed('hidden', true);
		CHANNELS_PROFILE.classed('hidden', true);
	    });

	// to make tooltip z-index max
	var tooltip = svg.append('text')
	    .attr('class', 'tooltip hidden')
	    .text('tooltip')
    });
}


function vizUserProfile(profile) {
    USERS_PROFILE.select('.name').text('@' + profile['name']);
    USERS_PROFILE.select('.joined dd').text(formatDate(profile['joined']));
    var value = profile['welcome_message'];
    var container = USERS_PROFILE.select('.welcome-message');
    if (value != null) {
	container.classed('hidden', false)
	container.select('dd').text(value);
    } else {
	container.classed('hidden', true)
    }

    var data = profile['channel_messages'];
    var container = USERS_PROFILE.select('.channel-messages dd');
    container.select('ol').remove()
    container = container.append('ol');
    data.forEach(function(d) {
	var channel = d[0];
	var messages = d[1];
	container.append('li')
	    .text(messages + ' — ' + channel);
    });
}


function vizUsers() {
    var layout = getLayout();
    var width = WIDTHS[layout];
    if (layout <= SM) {
	width *= 12;
    } else {
	width *= 6;
    }
    var height = width;

    var margin = {top: 10, right: 10, bottom: 10, left: 10},
    width = width - margin.left - margin.right,
    height = height - margin.top - margin.bottom;

    var x = d3.scale.linear()
	.range([0, width]);

    var y = d3.scale.linear()
	.range([height, 0]);

    var r = d3.scale.sqrt()
	.range([2, 10]);

    var color = d3.scale.category20();

    USERS_CANVAS.select('svg').remove();
    var svg = USERS_CANVAS.append('svg')
	.attr('width', width + margin.left + margin.right)
	.attr('height', height + margin.top + margin.bottom)
	.append('g')
	.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');    

    d3.json('data/users.json', function(error, data) {
	if (error) {
	    throw error;
	}

	data.forEach(function(d) {
	    d.joined = parseDate(d.joined);
	});
	data.sort(function(a, b) {
	    return b.messages - a.messages;
	});

	x.domain(d3.extent(data, function(d) {
	    return d.x;
	}));
	y.domain(d3.extent(data, function(d) {
	    return d.y;
	}));
	r.domain(d3.extent(data, function(d) {
	    return d.messages;
	}));

	svg.selectAll('.dot')
	    .data(data)
	    .enter().append('circle')
	    .attr('class', 'dot')
	    .attr('cx', function(d) {
		return x(d.x);
	    })
	    .attr('cy', function(d) {
		return y(d.y);
	    })
	    .attr('r', function(d) {
		return r(d.messages);
	    })
	    .style('fill', function(d) {
		return color(d.cluster);
	    })
	    .on('mouseover', function(d) {
		vizUserProfile(d);

		var dot = d3.select(this);
		dot.classed('active', true);
		var cx = +dot.attr('cx');
		var cy = +dot.attr('cy');
		var r = +dot.attr('r');
		tooltip.attr('x', cx + r + 2);
		tooltip.attr('y', cy);
		tooltip.text(d.name)
		tooltip.classed('hidden', false)

		USERS_PROFILE.classed('hidden', false);
	    })
	    .on('mouseout', function(d) {
		d3.select(this).classed('active', false);
		tooltip.classed('hidden', true);
		USERS_PROFILE.classed('hidden', true);
	    })

	var tooltip = svg.append('text')
	    .attr('class', 'tooltip hidden')
	    .text('tooltip')

    });
}


function vizMessagesByTime() {
    var layout = getLayout();
    var width = WIDTHS[layout];
    if (layout <= SM) {
	width *= 12;
    } else {
	width *= 6;
    }
    var height = 350;

    var margin = {top: 20, right: 100, bottom: 30, left: 50},
    width = width - margin.left - margin.right,
    height = height - margin.top - margin.bottom;

    var x = d3.time.scale()
	.range([0, width]);

    var ylim = 5000;    // bots goes to infinity
    var y = d3.scale.linear()
	.range([height, 0])
	.domain([0, ylim]);

    var color = d3.scale.category10();

    var xAxis = d3.svg.axis()
	.scale(x)
	.orient('bottom')
	.tickFormat(formatRuDateTick);

    var yAxis = d3.svg.axis()
	.scale(y)
	.orient('left');

    var line = d3.svg.line()
	.x(function(d) {
	    return x(d.date);
	})
	.y(function(d) {
	    return y(d.messages);
	});

    MESSAGES_BY_TIME_CANVAS.select('svg').remove()
    var svg = MESSAGES_BY_TIME_CANVAS.append('svg')
	.attr('width', width + margin.left + margin.right)
	.attr('height', height + margin.top + margin.bottom)
	.append('g')
	.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');    

    d3.json('data/messages_by_time.json', function(error, dump) {
	if (error) {
	    throw error;
	}

	var channels = dump.records;
	var texts = dump.tooltips;
	var tooltips = [];
	for (var channel in texts) {
	    var dates = texts[channel];
	    for (var date in dates) {
		var text = dates[date];
		var messages = channels[channel][date];
		date = parseDate(date);
		tooltips.push({
		    channel: channel,
		    date: date,
		    messages: messages,
		    text: text
		});
	    }
	}
	
	var dates = []
	var data = []
	var order = [OTHER, 'bots', '_random_flood', 'career']
	for (var index in order) {
	    var channel = order[index];
	    var records = [];
	    var series = channels[channel];
	    for (var date in series) {
		var messages = series[date];
		date = parseDate(date);
		dates.push(date);
		records.push({
		    date: date,
		    messages: messages,
		});
	    }
	    records.sort(function(a, b) {
		return a.date - b.date;
	    });
	    data.push({
		channel: channel,
		records: records
	    });
	}

	x.domain(d3.extent(dates));

	svg.append('g')
	    .attr('class', 'x axis')
	    .attr('transform', 'translate(0,' + height + ')')
	    .call(xAxis);

	svg.append('g')
	    .attr('class', 'y axis')
	    .call(yAxis)
	    .append('text')
	    .attr('transform', 'rotate(-90)')
	    .attr('y', 6)
	    .attr('dy', '0.71em')
	    .style('text-anchor', 'end')
	    .text('Число сообщений в неделю');

	var channel = svg.selectAll('.channel')
	    .data(data)
	    .enter().append('g')
	    .attr('class', 'channel');

	channel.append('path')
	    .attr('class', 'line')
	    .attr('d', function(d) {
		return line(d.records);
	    })
	    .style('stroke', function(d) {
		return color(d.channel);
	    });

	channel.append('text')
	    .datum(function(d) {
		var records = d.records;
		var size = records.length;
		var last = records[size - 1];
		return {
		    channel: d.channel,
		    last: last
		};
	    })
	    .attr('transform', function(d) {
		var messages = d.last.messages;
		if (messages >= ylim) {
		    messages = ylim;
		}
		return 'translate(' + x(d.last.date) + ',' + y(messages) + ')';
	    })
	    .attr('x', 5)
	    .attr('dy', '0.35em')
	    .style('fill', function(d) {
		return color(d.channel);
	    })
	    .text(function(d) {
		var name = d.channel;
		if (name == OTHER) {
		    name = 'Другие';
		}
		return name;
	    });

	svg.selectAll('.dot')
	    .data(tooltips)
	    .enter().append('circle')
	    .attr('class', 'annotation')
	    .attr('cx', function(d) {
		return x(d.date);
	    })
	    .attr('cy', function(d) {
		return y(d.messages);
	    })
	    .attr('r', 3)
	    .style('fill', function(d) {
		return color(d.channel);
	    })
	    .on('mouseover', function(d) {
		d3.select(this).classed('active', true);
		TOOLTIP.html(d.text)	
		    .style('left', (d3.event.pageX + 5) + 'px')		
		    .style('top', (d3.event.pageY - 5) + 'px')
		    .classed('hidden', false);

	    })
	    .on('mouseout', function(d) {
		d3.select(this).classed('active', false);
		TOOLTIP.classed('hidden', true);
	    });

    });
}


function vizMessagesByChannels() {
    var layout = getLayout();
    var width = WIDTHS[layout];
    var columns;
    var rows;
    if (layout <= SM) {
	width *= 12;
	columns = 4;
	rows = 10;
    } else {
	width *= 10;
	columns = 5;
	rows = 8
    }
    columns = 7
    rows = 5
    var offset = 20
    width -= offset;
    var columnWidth = width / columns;
    var rowHeight = 70;
    columnWidth = 100;
    rowHeight = 50;
    var height = rowHeight * rows;

    var margin = {top: 5, right: 5, bottom: 5, left: 5};
    facetWidth = columnWidth - margin.left - margin.right,
    facetHeight = rowHeight - margin.top - margin.bottom;

    MESSAGES_BY_CHANNELS_CANVAS.select('svg').remove()
    var svg = MESSAGES_BY_CHANNELS_CANVAS.append('svg')
	.attr('width', width)
	.attr('height', height)
	.attr('transform', 'translate(' + offset + ',0)');

    d3.json('data/messages_by_channels.json', function(error, dump) {
	if (error) {
	    throw error;
	}

	var channels = dump.order;
	var table = dump.records;
	var texts = dump.tooltips;

	var tooltips = {};
	for (var channel in texts) {
	    var dates = texts[channel];
	    var records = [];
	    for (var date in dates) {
		var text = dates[date];
		var messages = table[channel][date];
		date = parseDate(date);
		records.push({
		    channel: channel,
		    date: date,
		    messages: messages,
		    text: text
		});
	    }
	    tooltips[channel] = records;
	}

	var dates = [];
	var data = {};
	for (var channel in table) {
	    var series = table[channel];
	    var records = [];
	    for (var date in series) {
		var messages = series[date];
		date = parseDate(date);
		dates.push(date);
		records.push({
		    date: date,
		    messages: messages
		});
	    }
	    records.sort(function(a, b) {
		return a.date - b.date;
	    });
	    data[channel] = records;
	}

	var xlim = d3.extent(dates);
	for (var column = 0; column < columns; ++column) {
	    for (var row = 0; row < rows; ++row) {
		var index = row * columns + column;
		var channel = channels[index];
		var records = data[channel];

		var x = d3.time.scale()
		    .range([0, facetWidth])
		    .domain(xlim);

		var ymax = d3.max(records, function(d) {
		    return d.messages;
		});
		var y = d3.scale.linear()
		    .range([facetHeight, 0])
		    .domain([0, ymax]);

		var xAxis = d3.svg.axis()
		    .scale(x)
		    .orient('bottom')
		    .tickValues([
			parseDate('2016-01-01'),
		    ])


		var yAxis = d3.svg.axis()
		    .scale(y)
		    .orient('left')
		    .tickValues([0, ymax]);

		var line = d3.svg.line()
		    .x(function(d) {
			return x(d.date);
		    })
		    .y(function(d) {
			return y(d.messages);
		    });
	
		var left = column * columnWidth + margin.left + offset;
		var top = row * rowHeight + margin.top;
		var canvas = svg
		    .append('g')
		    .attr('transform',
			  'translate(' + left + ',' + top + ')');

		// if (row == rows - 1) {
		//     canvas.append('g')
		// 	.attr('class', 'x axis')
		// 	.attr('transform', 'translate(0,' + facetHeight + ')')
		// 	.call(xAxis);
		// }

		// canvas.append('g')
		//     .attr('class', 'y axis')
		//     .call(yAxis);

		canvas.append('path')
		    .datum(records)
		    .attr('class', 'line')
		    .attr('d', line);

		// canvas.append('text')
		//     .attr('class', 'legend')
		//     .attr('x', facetWidth / 2)
		//     .attr('y', 6)
		//     .style('text-anchor', 'middle')
		//     .text(channel);

		if (channel in tooltips) {
		    canvas.selectAll('.dot')
			.data(tooltips[channel])
			.enter().append('circle')
			.attr('class', 'annotation')
			.attr('cx', function(d) {
			    return x(d.date);
			})
			.attr('cy', function(d) {
			    return y(d.messages);
			})
			.attr('r', 3)
		    	.on('mouseover', function(d) {
			    d3.select(this).classed('active', true);
			    TOOLTIP.html(d.text)	
				.style('left', (d3.event.pageX + 5) + 'px')		
				.style('top', (d3.event.pageY - 5) + 'px')
				.classed('hidden', false);
			})
			.on('mouseout', function(d) {
			    d3.select(this).classed('active', false);
			    TOOLTIP.classed('hidden', true);
			});

		}
	    }
	}
    });
}


function vizUsersByTime() {
    var layout = getLayout();
    var width = WIDTHS[layout];
    if (layout <= SM) {
	width *= 12;
    } else {
	width *= 6;
    }
    var height = 350;

    var margin = {top: 20, right: 20, bottom: 30, left: 30},
    width = width - margin.left - margin.right,
    height = height - margin.top - margin.bottom;

    var x = d3.time.scale()
	.range([0, width]);

    var y = d3.scale.linear()
	.range([height, 0]);

    var xAxis = d3.svg.axis()
	.scale(x)
	.orient('bottom')
	.tickFormat(formatRuDateTick);

    var yAxis = d3.svg.axis()
	.scale(y)
	.orient('left');

    var line = d3.svg.line()
	.x(function(d) {
	    return x(d.date);
	})
	.y(function(d) {
	    return y(d.users);
	});
    
    USERS_BY_TIME_CANVAS.select('svg').remove()
    var svg = USERS_BY_TIME_CANVAS.append('svg')
	.attr('width', width + margin.left + margin.right)
	.attr('height', height + margin.top + margin.bottom)
	.append('g')
	.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');    

    d3.json('data/users_by_time.json', function(error, data) {
    	if (error) {
    	    throw error;
    	}

    	var table = data.records;
    	var tooltips = [];
    	var dates = data.tooltips;
    	for (var date in dates) {
    	    var text = dates[date];
    	    var users = table[date];
    	    date = parseDate(date);
    	    tooltips.push({
    		date: date,
    		users: users,
    		text: text
    	    });
    	}
	
    	var records = [];
    	for (var date in table) {
    	    var users = table[date];
    	    date = parseDate(date);
    	    records.push({
    		date: date,
    		users: users,
    	    });
    	}
    	records.sort(function(a, b) {
    	    return a.date - b.date;
    	});

	x.domain(d3.extent(records, function(d) {
	    return d.date;
	}));
	y.domain(d3.extent(records, function(d) {
	    return d.users;
	}));

	svg.append('g')
	    .attr('class', 'x axis')
	    .attr('transform', 'translate(0,' + height + ')')
	    .call(xAxis);

	svg.append('g')
	    .attr('class', 'y axis')
	    .call(yAxis)
	    .append('text')
	    .attr('transform', 'rotate(-90)')
	    .attr('y', 6)
	    .attr('dy', '0.71em')
	    .style('text-anchor', 'end')
	    .text('Число регистраций в неделю');

	svg.append('path')
	    .datum(records)
	    .attr('class', 'line')
	    .attr('d', line);

	svg.selectAll('.dot')
	    .data(tooltips)
	    .enter().append('circle')
	    .attr('class', 'annotation')
	    .attr('cx', function(d) {
		return x(d.date);
	    })
	    .attr('cy', function(d) {
		return y(d.users);
	    })
	    .attr('r', 3)
	    .on('mouseover', function(d) {
		d3.select(this).classed('active', true);
		TOOLTIP.html(d.text)	
		    .style('left', (d3.event.pageX + 5) + 'px')		
		    .style('top', (d3.event.pageY - 5) + 'px')
		    .classed('hidden', false);
	    })
	    .on('mouseout', function(d) {
		d3.select(this).classed('active', false);
		TOOLTIP.classed('hidden', true);
	    });

	var tooltip = svg.append('text')
	    .attr('class', 'tooltip hidden')
	    .text('tooltip');

    });

}


function viz() {
    vizChannels();
    vizUsers();
    vizMessagesByTime();
    vizMessagesByChannels();
    vizUsersByTime();
}


viz()
d3.select(window).on('resize', viz);
