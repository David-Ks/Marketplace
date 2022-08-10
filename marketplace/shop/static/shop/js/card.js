window.addEventListener('load', () => {
	let cardMinusBtns = $('div.count button.math:first-child');
	let cardPlusBtns = $('div.count button.math:last-child');
	let cardBuyBtn = $('button.buy-btn');
	let cardSaveBtn = $('div.card button.save');

	let viewCartBtnCount = $('nav div#viewCartBtnCount');
	let viewSavesBtnCount = $('nav div#viewSavesBtnCount');


	cardMinusBtns.each((id, elem) => {
		$(elem).click((el) => {
			let input = $(el.currentTarget).next()[0];
			let pl = 1;
			if($(input).hasClass('kg')) pl = 0.25;
			if(input.value > pl) {
				input.value = +input.value - pl;
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
			}
		});
	});


	cardSaveBtn.each((id, elem) => {
		let $elem = $(elem);
		$elem.click(() => {
			if(!$elem.hasClass('SAVED')) {
				let data = {
					action: 'add_to_saves',
					barcode: elem.id,
					csrfmiddlewaretoken: csrftoken
				}
				$.post('/products/', data, (response) => {
					$elem.addClass('SAVED');
					cardUnsaveBtn = $('div.card button.SAVED');

					if(+viewSavesBtnCount.text() == 0) {
						viewSavesBtnCount.css('display', 'block');
					}
					viewSavesBtnCount.text(+viewSavesBtnCount.text() + 1);
				});
			} else {
					let data = {
					action: 'remove_saves_item',
					barcode: elem.id,
					csrfmiddlewaretoken: csrftoken
				}
				$.post('/products/', data, (response) => {
					$elem.removeClass('SAVED');
					cardSaveBtn = $('div.card button.save:not(.SAVED)');

					if(+viewSavesBtnCount.text() == 1) {
						viewSavesBtnCount.css('display', 'none');
					}
					viewSavesBtnCount.text(+viewSavesBtnCount.text() - 1);
				});
			}
		});
	});

	cardBuyBtn.each((id, elem) => {
		let $elem = $(elem);
		$elem.click(() => {
			let data = {
				action: 'add_to_cart',
				count: $(`input.count-input#c${elem.id}`)[0].value,
				barcode: elem.value,
				csrfmiddlewaretoken: csrftoken
			}

			$.post('/products/', data, () => {
				if(viewCartBtnCount.text() == 0) {
					viewCartBtnCount.css('display', 'block');
				}
				viewCartBtnCount.text(+viewCartBtnCount.text() + 1);

				$elem.html('<i class="fi fi-rr-check"></i>');
				window.setTimeout(() => {
					$elem.html('<i class="fi fi-rr-shopping-cart-add"></i>');
				}, 1000);
			});
		});
	});
});