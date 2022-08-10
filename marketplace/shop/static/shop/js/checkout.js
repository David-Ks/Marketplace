window.addEventListener('load', () => {
	let prices = $('span#price');
	let total = $('strong#total');

	let totalSum = 0;

	prices.each((id, elem) => {
		let count = $(elem).children('.count-view');
		let price = $(elem).children('.price-view');

		totalSum += (+price.text() * +count.text());
	});

	if(totalSum >= 10000) {
		console.log($('li.delivery'));
		$('li.delivery').removeClass('d-flex').addClass('display-none');
	} else {
		console.log('cgtes');
		totalSum += 500;
	}

	total.text(`${totalSum}` + ' (դր)');
});