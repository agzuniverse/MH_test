//Place all JS code inside this
$(document).ready(function(){


  $('.datepicker').pickadate({
        selectMonths: true, // Creates a dropdown to control month
        selectYears: 100, // Creates a dropdown of 15 years to control year,
        today: 'Today',
        clear: 'Clear',
        close: 'Ok',
        format:'yyyy-mm-dd',
        closeOnSelect: true // Close upon selecting a date,
      });
    //Used for responsive navbar
    $('.button-collapse').sideNav({
        menuWidth: 200,
        edge: 'left',
        closeOnClick: true,
        draggable: true
      }
    );  

    //Animate navbar to solid black on scroll
    $(document).scroll(function(){
        $('nav').css('background-color','rgba(0,0,0,'+$(document).scrollTop()/100+')');
    });

    //Password confirmation check
    $('#passconfirm').blur(function(){
        if($('#pass').val()!=$('#passconfirm').val()){
            $('#passconfirm').addClass('invalid');
        }
    });
    
    //Checks if all fields are valid before form is submitted
    $('#submit-reg-form').click(function(e){
        let c=false;
        $('#regform :input').each(function(){
            if($(this).hasClass('valid')==false){
                c=true;
                e.preventDefault();
            }
        });
        if(c){
            Materialize.toast('You have not filled in all the details correctly!',3000,'rounded');
        }
    });

    //Initialize swipeable tabs
    //$('.tabs').tabs({swipeable: true});

    //Carousel slideshow
    $('.carousel').carousel({fullWidth:true});
    //setInterval(function(){
    //    $('.carousel').carousel('next');
    //},3000);

});
