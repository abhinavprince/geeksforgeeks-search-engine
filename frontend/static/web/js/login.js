$( document ).ready(function() {
$('#cssmenu > ul > li > a').click(function() {
  $('#cssmenu li').removeClass('active');
  $(this).closest('li').addClass('active');	
  var checkElement = $(this).next();
  if((checkElement.is('ul')) && (checkElement.is(':visible'))) {
    $(this).closest('li').removeClass('active');
    checkElement.slideUp('normal');
  }
  if((checkElement.is('ul')) && (!checkElement.is(':visible'))) {
    $('#cssmenu ul ul:visible').slideUp('normal');
    checkElement.slideDown('normal');
  }
  if($(this).closest('li').find('ul').children().length == 0) {
    return true;
  } else {
    return false;	
  }		
});
});


// Login Form
$(function() {
    var button = $('.loginButton2');
    var box = $('.loginBox2');
    var form = $('.loginForm2');
    button.removeAttr('href');
    button.mouseup(function(login) {
        box.toggle();
        button.toggleClass('active');
    });
    form.mouseup(function() { 
        return false;
    });
    $(this).mouseup(function(login) {
        if(!($(login.target).parent('.loginButton2').length > 0)) {
            button.removeClass('active');
            box.hide();
        }
    });
});

$(function() {
    var button1 = $('.loginButton1');
    var box1 = $('.loginBox1');
    var form1 = $('.loginForm1');
    button1.removeAttr('href');
    button1.mouseup(function(login1) {
        box1.toggle();
        button1.toggleClass('active');
    });
    form1.mouseup(function() { 
        return false;
    });
    $(this).mouseup(function(login1) {
        if(!($(login1.target).parent('.loginButton1').length > 0)) {
            button1.removeClass('active');
            box1.hide();
        }
    });
});