$(document).ready(function(){
    $("#size-tab").click(function(){
      $(".colors, .eraser").hide();
        $(".razmer").toggle();
    });

    $("#color-tab").click(function(){
    $(".razmer, .eraser").hide();
    $(".colors").toggle();
    });



    $("#big-size, #medium-size, #small-size").click(function(){
      $(".razmer").hide();
    });


    $("#black-btn, #red-btn, #green-btn, #blue-btn, #yellow-btn, #purple-btn").click(function(){
      $(".colors").hide(250);
    });



    $("#eraser-tab, #save-tab, #delete-tab").click(function(){
      $(this).toggleClass("activiran");
    });

    $("#save-tab, #size-tab, #color-tab, #delete-tab").click(function(){
      $("#eraser-tab").removeClass("activiran")
    });

    $("#eraser-tab, #size-tab, #color-tab, #delete-tab").click(function(){
      $("#save-tab").removeClass("activiran");
    });
    $("#eraser-tab, #size-tab, #color-tab, #save-tab").click(function(){
      $("#delete-tab").removeClass("activiran");
    });


    $("#save-tab").click(function(){
      $(".colors, .razmer").hide()
    });
    $("#eraser-tab").click(function(){
      $(".razmer, .colors").hide()
    });
    $("#delete-tab").click(function(){
      $(".razmer, .colors").hide()
    });

    $("#delete-tab").click(function(){
      $(".popup, .popup-overlay").fadeIn();
    })
    $("#close-popup").click(function(){
      $(".popup, .popup-overlay").fadeOut();
    });
    $("#delete-popup").click(function(){
      $(".popup, .popup-overlay").fadeOut();
    });

    $("#close-popup, #delete-popup").click(function(){
      $("#delete-tab").removeClass("activiran");
    });


});

