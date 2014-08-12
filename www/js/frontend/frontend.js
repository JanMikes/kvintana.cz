$(function(){
	$("a[href$='.jpg'],a[href$='.png'],a[href$='.gif'], .fancy a, a.fancy").fancybox();

	$(".homepage-slider").slideshow({
		width      : 886,
		height     : 282,
		transition : 'SquareRandom'
	});
});
