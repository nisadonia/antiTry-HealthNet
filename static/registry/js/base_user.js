if (!registry.has('forms.user'))
    registry.module('forms.user');

registry.forms['user'] = (function(){

    /*
        This can be done by registering a User UUID to use and then querying a specific URL via AJAX to verify user can
        do such things. Seriously. <3 AJAX.
     */
    var hooked = false;
    var csrf = $('[name="csrfmiddlewaretoken"]').val();

    var originals = {};
    var changed = {};

    const editables = $('input.editable');
    var userUuid = null;

    function getVerifyUrl(userUuid) {
        return '/verify/' + userUuid;
    }

    function getUpdateUrl(userUuid) {
        return '/user/' + userUuid;
    }

    function initEditables(canEdit) {
        // Add click listener to make fields readable
        if(canEdit) {
            editables.on('click', function () {
                $(this).prop('readonly', false);
            });

            // Add "blur" listeners such that when focus is lost they are made readonly again
            editables.on('blur', function () {
                $(this).prop('readonly', true);
            });

            // When a value has changed mark it for transition.
            editables.on('change', function () {
                var type = $(this).data('field');
                var value = $(this).val();

                // Reset to original if desired
                if (value === originals[type]) {
                    if (type in changed)
                        delete changed[type];

                    return;
                }

                changed[type] = $(this).val();
            });

            // Fill in original values
            editables.each(function () {
                originals[$(this).data('field')] = $(this).val();
            });

            editables.parsley();

            $('a.hn-tab').on('click', updateUser);
            console.log("User can edit");
        } else {
            editables.addClass('no-input');
            console.log("User cannot edit");
        }
    }

    function hookEditability(userId) {
        if (hooked)
            throw new Error('Attempt to reassign editability!');

        hooked = true;

        editables.prop('readonly', true);

        $.ajax({
            url: getVerifyUrl(userId),
            type: "GET",
            data: {},
            cache: false,
            dataType: "json",
            headers: {'X-CSRFToken': csrf},
            success: function(resp) {
                initEditables(resp['can_edit']);
                userUuid = resp['user_id'];
            },
            failure: function(resp) {
                console.log('failure');
                console.dir(resp);
            }
        });
    }

    function clearChanged() {
        for (var prop in changed) {
            if(!changed.hasOwnProperty(prop))
                continue;

            if(prop in originals)
                originals[prop] = changed[prop];
        }

        changed = {};
    }

    function revertChanged() {
        for (var prop in originals) {
            if (!originals.hasOwnProperty(prop))
                continue;

            if (prop in changed) {
                editables.filter(function () {
                    return $(this).data('field') === prop;
                }).each(function () {
                    $(this).val(originals[prop]);
                });
            }
        }

        changed = {};
    }

    function updateUser() {
        if (!hooked || userUuid == null || Object.size(changed) <= 0)
            return;

        vex.dialog.confirm({
            message: "Do you want to submit the current changes to the user profile?",
            callback: function (value) {
                if (value) {
                    $.ajax({
                        url: getUpdateUrl(userUuid),
                        type: "PATCH",
                        data: changed,
                        cache: false,
                        dataType: "json",
                        headers: {'X-CSRFToken': csrf},
                        success: function (resp) {
                            console.log("resp: ");
                            console.dir(resp);
                        },
                        failure: function (resp) {
                            console.log('failure');
                        }
                    });
                    clearChanged();
                } else {
                    revertChanged();
                    clearChanged();
                }
            }
        });
    }

    return {
        'hook': hookEditability,
        'updateUser': updateUser
    };
})();

Object.preventExtensions(registry.forms.user);

$(document).ready(function(){
    //  When user clicks on tab, this code will be executed
    $("#tab-links").find("li").click(function () {
        //  First remove class "active" from currently active tab
        $("#tab-links").find("li").removeClass('active');

        //  Now add class "active" to the selected/clicked tab
        $(this).addClass("active");

        //  Hide all tab content
        $(".tab").hide();

        //  Here we get the href value of the selected tab
        var selected_tab = $(this).find("a").attr("href");

        //  Show the selected tab content
        $(selected_tab).fadeIn();

        //  At the end, we add return false so that the click on the link is not executed
        return true;
    });

    $("#innertab-links").find("li").click(function () {
        //  First remove class "active" from currently active tab
        $("#innertab-links").find("li").removeClass('active');

        //  Now add class "active" to the selected/clicked tab
        $(this).addClass("active");

        //  Hide all tab content
        $(".innertab").hide();

        //  Here we get the href value of the selected tab
        var selected_tab = $(this).find("a").attr("href");

        //  Show the selected tab content
        $(selected_tab).fadeIn();

        //  At the end, we add return false so that the click on the link is not executed
        return true;
    });


    $("#checkAll").change(function () {
        $("input:checkbox").prop('checked', $(this).prop("checked"));
    });

    var inbox = $("#inbox");

    // Highlight a whole row from inbox table
    inbox.find("tr").not(':first').hover(
      function () {
        $(this).children().css("backgroundColor","#f3fef7");
      },
      function () {
        $(this).children().css("backgroundColor","#e3eee7");
      }
    );

        // Highlight a whole row from inbox table
    $("#patient").find("tr").not(':first').hover(
      function () {
        $(this).children().css("backgroundColor","#f3fef7");
      },
      function () {
        $(this).children().css("backgroundColor","#e3eee7");
      }
    );

    $('#patientSearchBar').keyup(function()
	{
		searchTable($(this).val());
	});

    $("#newMessage").click(function () {

        var div = $("#msg-create-form-html").clone();
        div.css("display", "block");
        $("#id_title").css("width", "80%");

        vex.open().append(div)

    });

    inbox.find("tr").not(':first').click(function () {
        //  Hide all tab content

        var selected_tab = $(this).attr("href");
        var uuid = $(this).data('message-id');

        $.ajax({
            url: 'msg/' + uuid,
            type: 'GET',
            data: {},
            success: function (response) {

                var data = response;

                var sender = data.sender["name"];
                var date = moment(data["date"]).format('MMMM Do YYYY [at] h:mm:ss a');
                var title = data["title"];
                var content = registry.escapeHtml(data["content"]).replace(/(?:\r\n|\r|\n)/g, '<br />');

                $("#message_sender").text(sender);
                $("#message_date").text(date);
                $("#message_title").text(title);
                $("#message_content").html(content);

                $(".tab").hide();
                //  Show the selected tab content
                $(selected_tab).fadeIn();
            }
        });

        return true;
    });

});

function searchTable(inputVal)
{

	var table = $('#patient');
	table.find('tr').each(function(index, row)
	{
		var allCells = $(row).find('td');
		if(allCells.length > 0)
		{
			var found = false;

			allCells.each(function(index, td)
			{
				var regExp = new RegExp(inputVal, 'i');
				if(regExp.test($(td).text()))
				{
					found = true;
					return false;
				}
			});
			if(found == true)$(row).show();
            else{
                $(row).hide();
                //$('#patient').append(notfound);
            }
        }
	});
}

$(window).bind('beforeunload', registry.forms.user.updateUser);

$("#buttons").click(function() {
        //  Hide all tab content
        $(".tab").hide();

        //  Here we get the href value of the selected tab
        var selected_tab = $(this).find("a").attr("href");

        //  Show the selected tab content
        $(selected_tab).fadeIn();

        //  At the end, we add return false so that the click on the link is not executed
        return true;
});

$("#presbuttons").click(function() {
        //  Hide all tab content
        $(".tab").hide();

        //  Here we get the href value of the selected tab
        var selected_tab = $(this).find("a").attr("href");

        //  Show the selected tab content
        $(selected_tab).fadeIn();

        //  At the end, we add return false so that the click on the link is not executed
        return true;
});

$("#button").click(function() {
        //  Hide all tab content
        $(".tab").hide();

        //  Here we get the href value of the selected tab
        var selected_tab = $(this).find("a").attr("href");

        //  Show the selected tab content
        $(selected_tab).fadeIn();

        //  At the end, we add return false so that the click on the link is not executed
        return true;
});
