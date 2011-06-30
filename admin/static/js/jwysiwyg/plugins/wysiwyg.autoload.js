/**
 * Autoload plugin
 * 
 * Depends on jWYSIWYG, autoload
 */
(function($) {
if (undefined === $.wysiwyg) {
	throw "wysiwyg.autoload.js depends on $.wysiwyg";
	return false;
}

if (undefined === $.autoload) {
	throw "wysiwyg.autoload.js depends on $.autoload";
	return false;
}

/*
 * Wysiwyg namespace: public properties and methods
 */
$.wysiwyg.autoload = {
	defaults: {
		baseFile:		"jquery.wysiwyg.js",
		cssPath:		"css/",
		controlPath:	"controls/",
		i18nPath:		"i18n/"
	},

	css: function(names) {
		$.autoload.css(names, this.defaults);
	},

	control: function(names, success) {
		$.autoload.js(names, {"baseFile": this.defaults.baseFile, "jsPath": this.defaults.controlPath, "success": success});
	},

	lang: function(names, success) {
		$.autoload.js(names, {"baseFile": this.defaults.baseFile, "jsPath": this.defaults.i18nPath, "success": success});
	}
};

})(jQuery);