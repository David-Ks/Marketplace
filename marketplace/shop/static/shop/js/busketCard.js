window.addEventListener('load', () => {
	let cardMinusBtns = $('div.count button.math:first-child');
	let cardPlusBtns = $('div.count button.math:last-child');
	let productPrices = $('span.productPrice');
	let total = $('td.total-price span');
	let deleteBtn = $('button.trash');
	let viewCartBtnCount = $('nav div#viewCartBtnCount');
	let checkOutBtn = $('button.chackout');

	productPrices.each((id, elem) => {
		$(elem).text(+$(`span.productStartPrice#${+id+1}`).text() * +$(`input.price-${+id+1}`)[0].value);
	});

	updateTotal();

	cardMinusBtns.each((id, elem) => {
		$(elem).click((el) => {
			let input = $(el.currentTarget).next()[0];
			let pl = 1;
			if($(input).hasClass('kg')) pl = 0.25;

			if(input.value > pl) {
				input.value = +input.value - pl;

				let productStartPrice = $(`span.productStartPrice#${input.id}`);
				let productPrice = $(`span#productPrice-${input.id}`);

				productPrice.text(+input.value * +productStartPrice.text());
				updateTotal()
			}
		});
	});

	cardPlusBtns.each((id, elem) => {
		$(elem).click((el) => {
			let input = $(el.currentTarget).prev()[0];
			let pl = 1;
			if($(input).hasClass('kg')) pl = 0.25;

			if(+input.value < +$(`input.max-count#${elem.id}`)[0].value) {
				input.value = +input.value + pl;

				let productStartPrice = $(`span.productStartPrice#${input.id}`);
				let productPrice = $(`span#productPrice-${input.id}`);

				productPrice.text(+input.value * +productStartPrice.text());
				updateTotal();
			}
		});
	});

	deleteBtn.each((id, elem) => {
		$(elem).click((el) => {
			$(`#del${el.currentTarget.id}`).remove();
			productPrices = $('span.productPrice');
			updateTotal();

			let data = {
				action: 'delete',
				barcode: el.currentTarget.value,
				csrfmiddlewaretoken: csrftoken
			}

			$.post(window.location.href.toString(), data, () => {
				if(viewCartBtnCount.length != 0) {
					viewCartBtnCount = $('nav div#viewCartBtnCount');
					if(+viewCartBtnCount.text() == 1) {
						$('nav button#navCartBtn').html('<i class="fi fi-rr-shopping-cart color-green"></i>');
					}
				}
				viewCartBtnCount.text(+viewCartBtnCount.text() - 1);
			});
		})
	});

	function updateTotal() {
		let sum = 0;
		productPrices.each((id, elem) => {
			sum += +elem.innerText;
		});
		$(total).text(sum);
	}
});