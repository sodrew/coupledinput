/* Javascript for CoupledInputXBlock. */
function CoupledInputXBlock(runtime, element) {

    var $element = $(element);
    var need_refresh = false;

    function save_and_update(element, funcId, jsonData){
        // Make an AJAX request to save the response
        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, funcId),
            data: JSON.stringify(jsonData),
            success: function (respData) {
                var el = $element.find('#'+funcId);
                el.text(respData.message);
                if(respData.message == 'Saved!'){
                    need_refresh = true;
                }
                el.css("color", respData.color);
                el.css("margin-left", "4px");
            }
        });
    }

    $element.find('#submit_response').click(function () {
        var data = {
            "response_one": $element.find('#response_one').val(),
            "response_two": $element.find('#response_two').val(),
        };

        save_and_update(element, 'save_response', data);
    });

    $element.find('#submit_names').click(function () {
        var data = {
            "response_one": $element.find('#response_one').val(),
            "response_two": $element.find('#response_two').val(),
        };

        save_and_update(element, 'save_names', data);
    });

    $element.find('#submit_studio').click(function () {
        var data = {
            "prompt": $element.find('#prompt').val(),
            "show_names": $element.find('#show_names').is(':checked'),
            "hide_one": $element.find('#hide_one').is(':checked'),
            "hide_two": $element.find('#hide_two').is(':checked'),
            "show_reversed": $element.find('#show_reversed').is(':checked'),
            "show_abbrev": $element.find('#show_abbrev').is(':checked'),
        };

        save_and_update(element, 'save_studio', data);
    });

    $element.find('#export_csv').click(function (ev) {
        ev.preventDefault();
        window.location = runtime.handlerUrl(element,
                                             'export_csv');
    });

    function check_show_names_cb(name_click, abbrev_click){
        var show_names = $element.find('#show_names');
        var show_names_state = $element.find('#show_names').is(':checked');
        var show_abbrev = $element.find('#show_abbrev');
        var show_abbrev_state = $element.find('#show_abbrev').is(':checked')
        var prompt_div = $element.find('#prompt_div');

        if(name_click){
          if(show_names_state){
              prompt_div.hide();
              show_abbrev.prop('checked', false);
          }else{
              prompt_div.show();
          }
        }

        if(abbrev_click && show_abbrev_state){
            show_names.prop('checked', false);
            prompt_div.show();
        }

    }

    $element.find('#show_names').click(function () {
        check_show_names_cb(true, false);
    });

    $element.find('#show_abbrev').click(function () {
        check_show_names_cb(false, true);
    });

    function check_before_refresh(){
        if(need_refresh){
            need_refresh = false;
            location.reload();
        }
    }

    // Listen for the "Cancel" button click event in Studio
    // when editing to know when to refresh
    $('.action-cancel').on('click', function () {
        check_before_refresh();
    });

    $(function ($) {
        /* Here's where you'd do things on page load. */
        check_show_names_cb();

        // this is to enable required fields
        // $(window).bind("beforeunload", function(e) {
        //     // check if this is normal web

        //     // if there are unsaved changes, then highlight red

        //     // return non value
        //     return true;
        // });
    });
}
