// hides navigation when scrolling down 
var scrolled;
var lastscroll = 0;
var delta = 5;
var navbarHeight = $('header').outerHeight();

$(window).scroll(function(event){
    scrolled = true;
});

setInterval(function() {
    if (scrolled) {
        hasScrolled();
        scrolled = false;
    }
}, 250);

function hasScrolled() {
    var scrolltop = $(this).scrollTop();
    
    // to optimize performance, checks if scroll is greater than delta
    if(Math.abs(lastscroll - scrolltop) <= delta)
        return;
    
    // show and hide nav on scroll down and up
    if (scrolltop > lastscroll && scrolltop > navbarHeight){
        // scroll down
        $('header').removeClass('nav-down').addClass('nav-up');
    } else {
        // scroll up
        if(scrolltop + $(window).height() < $(document).height()) {
            $('header').removeClass('nav-up').addClass('nav-down');
        }
    }
    
    lastScrollTop = scrolltop;
}