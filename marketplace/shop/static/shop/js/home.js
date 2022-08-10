window.addEventListener('load', () => {
	let body = $('body');
	let mainImg = $('section.main img');
	let starsCount = $('input#stars');

	let scale = 1;
	let scrollBefore = 0;

	starsCount.each((id, elem) => {
		let ratingWithStars = $(`div.ratingWithStars#${id}`)[0];
		star = '<i class="fi fi-rr-star"></i>';
		ratingWithStars.innerHTML = star.repeat(elem.value);
		console.log(ratingWithStars);
	});


	$("body").scroll(function () {
		let scrolled = $("body").scrollTop();

		if(scrolled < 450) {
			mainImg.css('opacity', 0.2);
		    if(scrollBefore > scrolled){
		        scrollBefore = scrolled;
		        if(scale > 1) {
		    		scale -= 0.01;
		        }
		    }else{
		        scrollBefore = scrolled;
		        if(scale < 1.5) {
					scale += 0.01;
		        }
		    }
			mainImg.css('transform', `scale(${scale})`);
		} else {
			mainImg.css('opacity', 0);
		}

	});
});