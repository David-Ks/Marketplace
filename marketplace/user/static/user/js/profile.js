window.addEventListener('load', () => {
	let stars = $('div.stars i.rat');
	let rating = $('#cuurentRat')[0];
	let ids = $('input#ids');
	let refreshBtn = $('button#refresh');

	let currentRating = rating.value;


	function ifActualStar(currentRating) {
		if(currentRating >= 0) {
			stars.each((id) => {
				let elem = $(`.rat#${id+1}`);
				if(id + 1 <= currentRating) {
					elem.addClass('yes');
				} else {
					if(elem.hasClass('yes')) {
						elem.removeClass('yes');
					}
				}
			});
		}
	}

	ifActualStar(currentRating);

	stars.each((id) => {
		let elem = $(`.rat#${id+1}`);

		elem.on('click', (elem) => {
			currentRating = +elem.currentTarget.id;
			rating.setAttribute('value', currentRating);
		});

		elem.hover((hoverElem) => {
			id = hoverElem.currentTarget.id;
			ifActualStar(id);
		}, () => {
			ifActualStar(currentRating);
		});
	});

	refreshBtn[0].onclick = function() {
		idsList = [];
		ids.each((id, elem) => {
			idsList.push(elem.value);
		});
		let data = {
			action: 'refresh',
			ids: idsList.toString(),
			csrfmiddlewaretoken: csrftoken
		}
		$.post(window.location.href.toString(), data, (response) => {
			let status = response.response;
			for(let i=0; i<status.length; i++) {
				let st = status[i].status;
				if(st == 1) {
					$(`td#for-status-${i}`).text('Պատրաստվում է');
				} else if(st == 2) {
					$(`td#for-status-${i}`).text('Ստուգվում է');
				} else if(st == 3) {
					$(`td#for-status-${i}`).text('Ճանապարհին է');
				} else {
					$(`td#for-status-${i}`).text('Կատարված է');
				}
			}
		});
	};
});