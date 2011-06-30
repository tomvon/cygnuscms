/**
 * Controls: Table plugin
 * 
 * Depends on jWYSIWYG
 */
(function($) {
if (undefined === $.wysiwyg) {
	throw "wysiwyg.table.js depends on $.wysiwyg";
	return false;
}

if (undefined === $.wysiwyg.controls) {
	$.wysiwyg.controls = {};
}

/*
 * Wysiwyg namespace: public properties and methods
 */
$.wysiwyg.controls.table = function(Wysiwyg) {
	Wysiwyg.insertTable = function(colCount, rowCount, filler) {
		if (isNaN(rowCount) || isNaN(colCount) || rowCount === null || colCount === null) {
			return;
		}
		colCount = parseInt(colCount, 10);
		rowCount = parseInt(rowCount, 10);
		if (filler === null) {
			filler = "&nbsp;";
		}
		filler = "<td>" + filler + "</td>";
		var html = ['<table border="1" style="width: 100%;"><tbody>'];
		for (var i = rowCount; i > 0; i--) {
			html.push("<tr>");
			for (var j = colCount; j > 0; j--) {
				html.push(filler);
			}
			html.push("</tr>");
		}
		html.push("</tbody></table>");
		return this.insertHtml(html.join(""));
	};

	var self = Wysiwyg;
	var formTableHtml = '<form class="wysiwyg"><fieldset><legend>Insert table</legend><label>Count of columns: <input type="text" name="colCount" value="3" /></label><label><br />Count of rows: <input type="text" name="rowCount" value="3" /></label><input type="submit" class="button" value="Insert table" /> <input type="reset" value="Cancel" /></fieldset></form>';

	if ($.fn.modal) {
		$.modal(formTableHtml, {
			onShow: function(dialog) {
				$("input:submit", dialog.data).click(function(e) {
					e.preventDefault();
					var rowCount = $('input[name="rowCount"]', dialog.data).val();
					var colCount = $('input[name="colCount"]', dialog.data).val();
					self.insertTable(colCount, rowCount, self.defaults.tableFiller);
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
		var dialog = $(formTableHtml).appendTo("body");
		dialog.dialog({
			modal: true,
			width: self.defaults.formWidth,
			height: self.defaults.formHeight,
			open: function(event, ui) {
				$("input:submit", $(self)).click(function(e) {
					e.preventDefault();
					var rowCount = $('input[name="rowCount"]', dialog).val();
					var colCount = $('input[name="colCount"]', dialog).val();
					self.insertTable(colCount, rowCount, self.defaults.tableFiller);
					$(dialog).dialog("close");
				});
				$("input:reset", $(self)).click(function(e) {
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
		var colCount = prompt("Count of columns", "3");
		var rowCount = prompt("Count of rows", "3");
		self.insertTable(colCount, rowCount, self.defaults.tableFiller);
	}
};

$.wysiwyg.insertTable = function(colCount, rowCount, filler) {
	var self = this.data("wysiwyg");
	self.insertTable(colCount, rowCount, filler);
	return this;
};

})(jQuery);