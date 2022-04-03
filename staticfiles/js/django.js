$(function(){
    $("#search-button-toggle").click(function(){ 
        $("#search-navbar").toggle();
        if( $("#search-navbar").css('display') == 'flex') {
            $("#search-arrow").css({transform: "rotate(180deg)"});
        } else {
            $("#search-arrow").css({transform: "rotate(0deg)"});
        }
    });

    $('.navbar-burger').click(function() {
        $('#navbar-menu, .navbar-burger').toggleClass('is-active');
    });

    $('#advanced-search-toggle').click(function() {
        $('#advanced-search').toggle();
    });

    $('#books_per_page').on('change', function() {
      // $num = this.value;
      $.ajax({
        url: 'change-books-per-page/',
        type: 'get', //send it through get method
        data: { 
          bpp: this.value,
        },
        success: function(response) {
          location.reload();
        },
        error: function(xhr) {
          alert(xhr.responseText);
        }
      });
    });
});

document.addEventListener('DOMContentLoaded', () => {
  (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
    $notification = $delete.parentNode;
    $delete.addEventListener('click', () => {
      $notification.parentNode.removeChild($notification);
    });
  });
});