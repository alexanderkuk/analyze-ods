
var CHANNELS = d3.select('#channels');
var CHANNELS_CANVAS = CHANNELS.select('.canvas');
var CHANNELS_PROFILE = CHANNELS.select('.profile');

var USERS = d3.select('#users');
var USERS_CANVAS = USERS.select('.canvas');
var USERS_SEARCH = USERS.select('#search');
var USERS_PROFILE = USERS.select('.profile');

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
var SILVER = '#e3e3e3';

var formatDate = d3.time.format('%Y-%m-%d');
var parseDate = formatDate.parse;

var START = parseDate('2015-02-12');
var STOP = parseDate('2017-09-12');


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


function vizChannelMessages(profile, container) {
    var layout = getLayout();
    var width = WIDTHS[layout];
    if (layout <= SM) {
	width *= 8;  		// * 12
    } else {
	width *= 4;
    }
    var height = 200;

    var margin = {top: 10, right: 10, bottom: 20, left: 30},
    width = width - margin.left - margin.right,
    height = height - margin.top - margin.bottom;

    var x = d3.time.scale()
	.range([0, width]);

    var y = d3.scale.linear()
	.range([height, 0]);

    var xAxis = d3.svg.axis()
	.scale(x)
	.orient('bottom')
	.tickFormat(function(date) {
	    var month = date.getMonth();
	    if (month == 0) {
		return date.getFullYear();
	    }
	});

    var yAxis = d3.svg.axis()
	.scale(y)
    	.orient('left');

    var line = d3.svg.line()
	.defined(function(d) {
	    return d;
	})
	.x(function(d) {
	    return x(d.date);
	})
	.y(function(d) {
	    return y(d.messages);
	});

    var area = d3.svg.area()
	.defined(function(d) {
	    return d;
	})
	.x(function(d) {
	    return x(d.date);
	})
	.y0(height)
	.y1(function(d) {
	    return y(d.messages);
	});

    if (container) {
	container.select('svg').remove();
    }
    var svg = container.append('svg')
	.attr('width', width + margin.left + margin.right)
	.attr('height', height + margin.top + margin.bottom)
	.append('g')
	.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');
    
    var data = [];
    var week_messages = profile.week_messages;
    for (var date in week_messages) {
	data.push({
	    date: parseDate(date),
	    messages: week_messages[date]
	})
    }
    data.sort(function(a, b) {
	return a.date - b.date;
    });

    x.domain([START, STOP]);
    var max = d3.max(data, function(d) {
	return d.messages
    });
    y.domain([0, max]);
    yAxis.tickValues([0, max]);

    svg.append('path')
       .datum(data)
       .attr('class', 'area')
       .attr('d', area);
    
    svg.append('path')
	.datum(data)
	.attr('class', 'line')
	.attr('d', line);


    svg.append('g')
	.attr('class', 'x axis')
	.attr('transform', 'translate(0,' + height + ')')
	.call(xAxis)

    var text = svg.append('g')
	.attr('class', 'y axis')
	.call(yAxis)
	.append('text')
    	.attr('transform', 'rotate(-90)')
    	.attr('y', 15)
	.style('text-anchor', 'end')
	.text('Сообщений в неделю');
}


function vizChannelProfile(profile) {
    CHANNELS_PROFILE.select('.name').text('#' + profile.name);
    CHANNELS_PROFILE.select('.created').text(formatDate(profile.created));
    CHANNELS_PROFILE.select('.creator').text('@' + profile.creator);
    CHANNELS_PROFILE.select('.purpose').text(profile.purpose);
    var messages = CHANNELS_PROFILE.select('.messages')
    vizChannelMessages(profile, messages);
}


function vizChannels() {
    var layout = getLayout();
    var width = WIDTHS[layout];
    if (layout <= SM) {
	width *= 12;
    } else {
	width *= 8;
    }
    var height = 400;

    var margin = {top: 30, right: 50, bottom: 100, left: 100},
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
	.tickFormat(function(date) {
	    var month = date.getMonth();
	    if (month == 0) {
		return date.getFullYear();
	    } else {
		return MONTHS[month];
	    }
	});

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


function vizUserMessages(profile, container) {
    var layout = getLayout();
    var width = WIDTHS[layout];
    if (layout <= SM) {
	width *= 8;  		// * 12
    } else {
	width *= 4;
    }
    var height = 200;

    var margin = {top: 10, right: 10, bottom: 20, left: 30},
    width = width - margin.left - margin.right,
    height = height - margin.top - margin.bottom;

    var x = d3.time.scale()
	.range([0, width]);

    var y = d3.scale.linear()
	.range([height, 0]);

    var xAxis = d3.svg.axis()
	.scale(x)
	.orient('bottom')
	.tickFormat(function(date) {
	    var month = date.getMonth();
	    if (month == 0) {
		return date.getFullYear();
	    }
	});

    var yAxis = d3.svg.axis()
	.scale(y)
    	.orient('left');

    var stack = d3.layout.stack();

    if (container) {
	container.select('svg').remove();
    }
    var svg = container.append('svg')
	.attr('width', width + margin.left + margin.right)
	.attr('height', height + margin.top + margin.bottom)
	.append('g')
	.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');    

    var months = profile.months.map(parseDate);
    var channels = profile.channels;

    var data = [];
    channels.forEach(function(d) {
	var row = [];
	d.messages.forEach(function(count, index) {
	    row.push({
		x: months[index],
		y: count,
		color: d.color
	    });
	})
	data.push(row);
    })

    var totals = [];
    months.forEach(function() {
	totals.push(0);
    })
    channels.forEach(function(d) {
	d.messages.forEach(function(count, index) {
	    totals[index] += count;
	});
    });
    var max = d3.max(totals);

    x.domain([START, STOP]);
    y.domain([0, max]);
    yAxis.tickValues([0, max]);

    svg.selectAll('.serie')
    	.data(stack(data))
    	.enter().append('g')
    	.attr('class', 'serie')
      	.selectAll('rect')
      	.data(function(d) {
    	    return d;
    	})
      	.enter().append('rect')
    	.attr('fill', function(d) {
    	    return d.color;
    	})
    	.attr('stroke', function(d) {
    	    return d.color;
    	})
    	.attr('x', function(d) {
    	    return x(d.x);
    	})
    	.attr('y', function(d) {
    	    return y(d.y0) - height + y(d.y) - 1;
    	})
    	.attr('height', function(d) {
    	    return height - y(d.y);
    	})
    	.attr('width', 11);

    svg.append('g')
	.attr('class', 'x axis')
	.attr('transform', 'translate(0,' + height + ')')
	.call(xAxis)

    var text = svg.append('g')
	.attr('class', 'y axis')
	.call(yAxis)
	.append('text')
    	.attr('transform', 'rotate(-90)')
    	.attr('y', 15)
	.style('text-anchor', 'end')
	.text('Сообщений в месяц');

    if (container) {
	container.select('.legend').remove();
    }
    var channel = container.append('div')
	.attr('class', 'legend')
	.selectAll('.channel')
	.data(channels)
	.enter().append('span')
	.attr('class', 'channel');

    channel.append('div')
	.attr('class', 'box')
	.style('background', function(d) {
	    var color = d3.rgb(d.color);
	    return 'rgba(' + color.r + ', ' + color.g + ', ' + color.b + ', ' + 0.7 + ')';
	})
	.style('border-color', function(d) {
	    return d.color;
	});
    
    channel.append('span')
	.text(function(d) {
	var messages = 0;
	d.messages.forEach(function(x) {
	    messages += x;
	});
	var name = d.name;
	if (name == OTHER) {
	    name = 'Другие каналы';
	}
	return d.name + ' — ' + messages;
	});
}


function vizUserProfile(profile) {
    USERS_PROFILE.select('.name').text('@' + profile.name);

    var container = USERS_PROFILE.select('.messages');
    vizUserMessages(profile, container);
    
    var value = profile.welcome_message;
    var container = USERS_PROFILE.select('.welcome-message');
    if (value != null) {
	container.classed('hidden', false)
	container.text('#welcome: ' + value);
    } else {
	container.classed('hidden', true)
    }
}


function vizUsers() {
    var layout = getLayout();
    var width = WIDTHS[layout];
    if (layout <= SM) {
	width *= 12;
    } else {
	width *= 7;
    }
    var height = width;

    var margin = {top: 10, right: 50, bottom: 10, left: 10},
    width = width - margin.left - margin.right,
    height = height - margin.top - margin.bottom;

    var x = d3.scale.linear()
	.range([0, width]);

    var y = d3.scale.linear()
	.range([height, 0]);

    var r = d3.scale.log()
	.range([1, 6]);

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

	x.domain(d3.extent(data, function(d) {
	    return d.x;
	}));
	y.domain(d3.extent(data, function(d) {
	    return d.y;
	}));
	r.domain(d3.extent(data, function(d) {
	    return d.messages;
	}));

	data.forEach(function(d) {
	    d.joined = parseDate(d.joined);
	    d.channel = d.channels[0].name;

	    d.radius = r(d.messages);
	    d.cx = x(d.x);
	    d.cy = y(d.y);
	    d.x = d.cx;
	    d.y = d.cy;
	});
	data.sort(function(a, b) {
	    return b.radius - a.radius;
	});

	var dots = svg.selectAll('.dot')
	    .data(data)
	    .enter().append('circle')
	    .attr('class', 'dot')
	    .attr('cx', function(d) {
		return d.cx;
	    })
	    .attr('cy', function(d) {
		return d.cy;
	    })
	    .attr('r', function(d) {
		return d.radius;
	    })
	    .style('fill', function(d) {
		return d.color;
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

	var tree = d3.geom.quadtree(data);
	var max = d3.max(data, function(d) {
	    return d.radius;
	});
	var padding = 1;
	
	function step(d) {
	    var r = d.radius + max + padding
	    var _x1 = d.x - r;
	    var _x2 = d.x + r;
	    var _y1 = d.y - r;
	    var _y2 = d.y + r;

	    tree.visit(function(tree, x1, y1, x2, y2) {
		var other = tree.point
		if (other && (other !== d)) {
		    var x = d.x - other.x;
		    var y = d.y - other.y;
		    var l = Math.sqrt(x * x + y * y);
		    var r = d.radius + other.radius + padding;
		    if (l < r) {
			l = (l - r) / l * 0.1;
			d.x -= x *= l;
			d.y -= y *= l;
			other.x += x;
			other.y += y;
		    }
		}
		return x1 > _x2 || x2 < _x1 || y1 > _y2 || y2 < _y1;
	    });
	}

	function tick(e) {
  	    dots
		.each(step)
		.attr('cx', function(d) {
		    return d.x;
		})
		.attr('cy', function(d) {
		    return d.y;
		});
	}

	var force = d3.layout.force()
	    .nodes(data)
	    .size([width, height])
	    .gravity(0)
	    .charge(0)
	    .on('tick', tick);

	force.start();
	for (var i = 0; i < 3; ++i) force.tick();
	force.stop();

	var tooltip = svg.append('text')
	    .attr('class', 'tooltip hidden')
	    .text('tooltip')

	USERS_SEARCH.on('input', function() {
	    var text = this.value.trim();
	    svg.selectAll('.dot')
		.data(data)
		.style('fill', function(d) {
		    var name = d.name.startsWith(text);
		    var channel = d.channel.startsWith(text);
		    if (name || channel) {
		    	return d.color;
		    } else {
		    	return SILVER;
		    }
		});
	});
    });
}


function viz() {
    vizChannels();
    vizUsers();
}


viz();
d3.select(window).on('resize', viz);
