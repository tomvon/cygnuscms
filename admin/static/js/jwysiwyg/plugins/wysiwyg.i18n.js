/**
 * Internationalization plugin
 * 
 * Depends on jWYSIWYG
 */
(function($) {
if (undefined === $.wysiwyg) {
	throw "wysiwyg.i18n.js depends on $.wysiwyg";
	return false;
}

/*
 * Wysiwyg namespace: public properties and methods
 */
$.wysiwyg.i18n = {
	defaults: {
		lang: "en", // change to your language
		wysiwygLang: "en" // default WYSIWYG language
	},
	lang: {},
	options: {},

	init: function(Wysiwyg, lang) {
		if (undefined === lang) {
			lang = this.defaults.lang;
		}

		if ((lang !== this.defaults.wysiwygLang) && (undefined === $.wysiwyg.i18n.lang[lang])) {
			if (!$.wysiwyg.autoload) {
				throw "wysiwyg.i18n.js depends on $.wysiwyg.autoload";
				return false;
			}
			
			$.wysiwyg.autoload.lang("lang." + lang + ".js", {success: (function(Wysiwyg, lang) {
//				console.log("Language file is loaded");
				$.wysiwyg.i18n.init(Wysiwyg, lang);
			})(Wysiwyg, lang)});
		}
		
		this.options.lang = lang;
	},

	t: function(phrase, lang) {
		if (undefined === lang) {
			lang = this.options.lang;
		}

		if ((lang !== this.defaults.wysiwygLang) && this.lang[lang] && this.lang[lang][phrase]) {
			return this.lang[lang][phrase];
		}
		
		return phrase;
	}
};

})(jQuery);