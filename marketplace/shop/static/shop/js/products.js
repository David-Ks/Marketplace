window.addEventListener("load", () => {
	let catInputs = $('input.cat-input');
	let priceSearchBtn = $('a#priceSearch');
	let location = window.location.search;
	let minPrice = $('input#min');
	let maxPrice = $('input#max');


	const params = new URLSearchParams(location);

	if (params.has('cats')) {
		catInputs.each((id, el) => {
			if (params.getAll('cats').includes(parseInt(el.id).toString())) {
				el.checked = true;
			}
		});
	}
	if (params.has('min')) {
		minPrice[0].value = params.get('min');
	}
	if (params.has('max')) {
		maxPrice[0].value = params.get('max');
	}

	if (location.length == 0) {
		location += '?';
	} else if (location[location.length - 1] != '&') {
		location += '&';
	}

	$('a#priceSearch').click((el) => {
		let min = minPrice[0].value;
		let max = maxPrice[0].value;

		if (params.has('min')) params.delete('min');
		if (params.has('max')) params.delete('max');
		if (params.has('page')) {
			params.set('page', 1);
		}
		
		if (+min > +max && min && max) {
			minPrice[0].value = 1;
		}
		if (min) {
			params.set('min', min);
		}
		if (max) {
			params.set('max', max);
		}
		$(el)[0].currentTarget.href = "?" + params.toString();
		$(el).click();
	});
});