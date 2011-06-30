/**
 * Controls: Image plugin
 * 
 * Depends on jWYSIWYG
 */
(function($) {
if (undefined === $.wysiwyg) {
	throw "wysiwyg.image.js depends on $.wysiwyg";
	return false;
}

if (undefined === $.wysiwyg.controls) {
	$.wysiwyg.controls = {};
}

/*
 * Wysiwyg namespace: public properties and methods
 */
$.wysiwyg.controls.image = function(Wysiwyg) {
	var self = Wysiwyg;
	var formImageHtml = '<form class="wysiwyg"><fieldset><legend>Insert Image</legend><label>Image URL: <input type="text" name="url" value="http://"/></label><label>Image Title: <input type="text" name="imagetitle" value=""/></label><label>Image Description: <input type="text" name="description" value=""/></label><input type="submit" class="button" value="Insert Image"/> <input type="reset" value="Cancel"/></fieldset></form>';

	if ($.modal) {
		$.modal(formImageHtml, {
			onShow: function(dialog) {
				$("input:submit", dialog.data).click(function(e) {
					e.preventDefault();
					var szURL = $('input[name="url"]', dialog.data).val();
					var title = $('input[name="imagetitle"]', dialog.data).val();
					var description = $('input[name="description"]', dialog.data).val();
					var img = '<img src="' + szURL + '" title="' + title + '" alt="' + description + '"/>';
					self.insertHtml(img);
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
		var dialog = $(formImageHtml).appendTo("body");
		dialog.dialog({
			modal: true,
			width: self.defaults.formWidth,
			height: self.defaults.formHeight,
				open: function(ev, ui) {
					$("input:submit", $(self)).click(function(e) {
					e.preventDefault();
					var szURL = $('input[name="url"]', dialog).val();
					var title = $('input[name="imagetitle"]', dialog).val();
					var description = $('input[name="description"]', dialog).val();
					var img="<img src='" + szURL + "' title='" + title + "' alt='" + description + "' />";
					self.insertHtml(img);
					$(dialog).dialog("close");
				});
				$("input:reset", $(self)).click(function(e) {
					e.preventDefault();
					$(dialog).dialog("close");
				});
			},
			close: function(ev, ui){
				$(self).dialog("destroy");
			}
		});
	}
	else {
		if ($.browser.msie) {
			self.focus();
			self.editorDoc.execCommand("insertImage", true, null);
		}
		else {
			var szURL = prompt("URL", "http://");
			if (szURL && szURL.length > 0) {
				self.editorDoc.execCommand("insertImage", false, szURL);
			}
		}
	}
};

$.wysiwyg.insertImage = function(szURL, attributes) {
	var self = this.data("wysiwyg");

	if (!szURL || szURL.length === 0) {
		return this;
	}
	
	if ($.browser.msie) {
		self.focus();
	}
	if (attributes) {
		self.editorDoc.execCommand("insertImage", false, "#jwysiwyg#");
		var img = self.getElementByAttributeValue("img", "src", "#jwysiwyg#");

		if (img) {
			img.src = szURL;

			for (var attribute in attributes) {
				img.setAttribute(attribute, attributes[attribute]);
			}
		}
	}
	else {
		self.editorDoc.execCommand("insertImage", false, szURL);
	}
	return this;
};

})(jQuery);