/**
 * Controls: Colorpicker plugin
 * 
 * Depends on jWYSIWYG, (farbtastic || other colorpicker plugins)
 */
(function($) {
if (undefined === $.wysiwyg) {
	throw "wysiwyg.colorpicker.js depends on $.wysiwyg";
	return false;
}

if (undefined === $.wysiwyg.controls) {
	$.wysiwyg.controls = {};
}

/*
 * Wysiwyg namespace: public properties and methods
 */
$.wysiwyg.controls.colorpicker = function(Wysiwyg) {
	var self = Wysiwyg;
	var colorpickerHtml = '<form class="wysiwyg"><fieldset><legend>Colorpicker</legend><label>Color: <input type="text" name="color" value="#123456"/></label><div></div><input type="submit" class="button" value="Apply"/> <input type="reset" value="Cancel"/></fieldset></form>';

	if ($.modal) {
		var elements = $(colorpickerHtml);

		if ($.farbtastic) {
			$(elements.find("div")).farbtastic(elements.find("input:text"));
		}

		$.modal(elements.html(), {
			onShow: function(dialog) {
				$("input:submit", dialog.data).click(function(e) {
					e.preventDefault();
					var color = $('input[name="color"]', dialog.data).val();
					self.editorDoc.execCommand('ForeColor', false, color);
					$.modal.close();
				});
				$("input:reset", dialog.data).click(function(e) {
					e.preventDefault();
					$.modal.close();
				});
			},
			maxWidth: self.defaults.formWidth,
			maxHeight: self.defaults.formHeight,
			overlayClose: true
		});
	}
	else if ($.fn.dialog) {
		var elements = $(colorpickerHtml);

		if ($.farbtastic) {
			$(elements.find("div")).farbtastic(elements.find("input:text"));
		}

		var dialog = elements.appendTo("body");
		dialog.dialog({
			modal: true,
			width: self.defaults.formWidth,
			height: self.defaults.formHeight,
			open: function(event, ui) {
				$("input:submit", elements).click(function(e) {
					e.preventDefault();
					var color = $('input[name="color"]', dialog).val();
					self.editorDoc.execCommand('ForeColor', false, color);
					$(dialog).dialog("close");
				});
				$("input:reset", elements).click(function(e) {
					e.preventDefault();
					$(dialog).dialog("close");
				});
			},
			close: function(event, ui){
				$(self).dialog("destroy");
			}
		});
	}
	else {
		if ($.farbtastic) {
			var elements = $("<div/>")
				.css({"position": "absolute",
					"left": "50%", "top": "50%", "background": "rgb(0, 0, 0)",
					"margin-top": -1 * Math.round(self.defaults.formHeight / 2),
					"margin-left": -1 * Math.round(self.defaults.formWidth / 2)})
				.html(colorpickerHtml);
			$(elements.find("div")).farbtastic(elements.find("input:text"));
			$("input:submit", elements).click(function(event) {
				event.preventDefault();
				var color = $('input[name="color"]', elements).val();
				self.editorDoc.execCommand('ForeColor', false, color);
				$(elements).remove();
			});
			$("input:reset", elements).click(function(event) {
				event.preventDefault();
				$(elements).remove();
			});
			$("body").append(elements);
		}
	}
};

})(jQuery);